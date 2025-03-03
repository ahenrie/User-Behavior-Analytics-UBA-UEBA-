import pandas as pd
import re
import time
from optparse import Values
from sklearn.preprocessing import StandardScaler

class CleanedDF:
    def __init__(self, filePath: str):
        self.filePath = filePath
        self.df = self.exeExtraction()

    """
    Method to extract executables from the messages.
    """
    def exeExtraction(self) -> pd.DataFrame:
        try:
            print("Attempting to build dataframe...")
            df = pd.read_csv(self.filePath)
        except FileNotFoundError:
            print(f"Error: The file {self.filePath} was not found.")
            return pd.DataFrame()  # Return an empty DataFrame on error
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            return pd.DataFrame()  # Return an empty DataFrame on error
        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

        df['Exe'] = None  # Initialize the 'Exe' column
        pattern = r'(?:^|\\)(\w+\.exe)'  # Regex pattern to find .exe files

        # Iterate over the DataFrame rows
        for index, row in df.iterrows():
            message = row.get("Message")  # Use get to avoid KeyError
            if isinstance(message, str):
                exe = re.findall(pattern, message)
                if exe:
                    df.at[index, 'Exe'] = exe[0]  # Assign the first match

        print("Dataframe created and executable feature extracted.")
        return df  # Return the modified DataFrame

    """
    Data preprocessing:
        1. Convert categorical variables into numerical representations
        2. Normalize time
        3. Handle missing Values
        4. Additional feature extraction
    """
    def preprocessing(self):
        #### Missing Values
        # Categorical Values
        categorical_features = ["AccountName", "SourceName", "LogonType", "EventType", "Exe"]
        self.df[categorical_features] = self.df[categorical_features].fillna("Unknown")

        # Numerical Values
        numerical_columns = ["SeverityValue", "ProcessID", "ThreadID"]
        self.df[numerical_columns] = self.df[numerical_columns].fillna(self.df[numerical_columns].median())

        # Drop rows without timestamps (wont happen but good practice)
        self.df = self.df.dropna(subset=["EventTime"])

        #### Convert timestamps into usable features
        # Convert EventTime and EventReceivedTime to datetime
        self.df["EventTime"] = pd.to_datetime(self.df["EventTime"], format="%Y-%m-%d %H:%M:%S")
        self.df["EventReceivedTime"] = pd.to_datetime(self.df["EventReceivedTime"], format="%Y-%m-%d %H:%M:%S")

        # Extract features from EventTime
        self.df["Hour"] = self.df["EventTime"].dt.hour
        self.df["DayOfWeek"] = self.df["EventTime"].dt.dayofweek  # Monday=0, Sunday=6
        self.df["MonthYear"] = self.df["EventTime"].dt.to_period("M")

        # Remove the original EventTime and EventReceivedTime columns as they are no longer needed
        self.df.drop(columns=["EventTime", "EventReceivedTime"], inplace=True)

        #### Encoding categorical Values
        # Frequency Encoding for High-Cardinality Features
        for col in ["AccountName", "SourceName"]:
            freq = self.df[col].value_counts(normalize=True)
            self.df[col + "_Freq"] = self.df[col].map(freq)

        # One-Hot Encoding for Low-Cardinality Features
        self.df = pd.get_dummies(self.df, columns=["LogonType", "EventType"], drop_first=True)

        ### Normalize numerical features to bring them into a similar range
        scaler = StandardScaler()
        scaled_features = ["SeverityValue", "ProcessID", "ThreadID", "Hour", "DayOfWeek"]
        self.df[scaled_features] = scaler.fit_transform(self.df[scaled_features])

        # Drop no longer needed columns (after encodings)
        self.df.drop(columns=["Date", "AccountName", "SourceName"], inplace=True)

    """
    Print some info about the df
    """
    def printInfo(self):
        print(self.df.info())
        print(self.df.head())
        print(self.df.tail())
