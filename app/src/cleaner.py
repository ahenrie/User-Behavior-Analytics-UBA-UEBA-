import pandas as pd
import joblib
import re
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

class CleanedDF:
    def __init__(self, file_path: str, scaler_path="models/scaler.pkl", encoder_path="models/encoder.pkl"):
        """Initialize the class with file path and paths to saved encoders/scalers."""
        self.file_path = file_path
        self.scaler_path = scaler_path
        self.encoder_path = encoder_path
        self.df = self._load_data()  # Load data upon initialization

    def _load_data(self) -> pd.DataFrame:
        """Load CSV file into a Pandas DataFrame with proper data handling."""
        try:
            print("Loading data...")
            df = pd.read_csv(self.file_path, low_memory=False)  # Read CSV file
        except Exception as e:
            print(f"Error loading file: {e}")
            return pd.DataFrame()  # Return empty DataFrame if there's an error

        # Extract the first executable name from the "Message" column if it exists
        if "Message" in df:
            df["Exe"] = df["Message"].apply(self._extract_exe)

        print("Data loaded and executables extracted.")
        return df

    @staticmethod
    def _extract_exe(message: str) -> str:
        """Extract first executable name from a log message if present."""
        if isinstance(message, str):
            match = re.search(r'([a-zA-Z0-9_]+\.exe)', message)  # Regex to find .exe filenames
            return match.group(1) if match else None  # Return found filename or None
        return None

    def preprocess(self):
        """Preprocess the dataset: clean missing values, encode categorical data, and normalize numeric data."""
        if self.df.empty:
            print("No data to preprocess.")
            return

        ############# Convert EventTime to a proper datetime format #############
        if "EventTime" in self.df:
            self.df["EventTime"] = pd.to_datetime(self.df["EventTime"], errors="coerce")

            # Convert datetime to UNIX timestamp (seconds since 1970)
            self.df["Timestamp"] = self.df["EventTime"].apply(lambda x: x.timestamp() if pd.notnull(x) else None)

            # Drop original EventTime column as it's redundant after conversion
            self.df.drop(columns=["EventTime"], inplace=True)

        # Extract time-based features from the timestamp
        self.df["DayOfWeek"] = self.df["Timestamp"].apply(lambda x: pd.to_datetime(x, unit='s').dayofweek if pd.notnull(x) else None)
        self.df["Month"] = self.df["Timestamp"].apply(lambda x: pd.to_datetime(x, unit='s').month if pd.notnull(x) else None)
        self.df["Year"] = self.df["Timestamp"].apply(lambda x: pd.to_datetime(x, unit='s').year if pd.notnull(x) else None)

        # Ensure time-based features are treated as numerical
        self.df[["Timestamp", "DayOfWeek", "Month", "Year"]] = self.df[["Timestamp", "DayOfWeek", "Month", "Year"]].apply(pd.to_numeric)

        ############# Define numerical and categorical columns #############
        numerical_columns = ["SeverityValue", "ProcessID", "ThreadID", "EventID"]
        categorical_columns = ["EventType", "Exe", "SourceName", "AccountName", "AccountType", "Severity"]

        # Convert numerical columns to float and handle missing values
        for col in numerical_columns:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")  # Convert to numeric
            self.df[col] = self.df[col].fillna(self.df[col].median())  # Fill missing values with median

        # Convert categorical columns to string and handle missing values
        for col in categorical_columns:
            self.df[col] = self.df[col].fillna("Unknown").astype(str)  # Replace missing values with "Unknown"

        # Drop LogonType column
        if "LogonType" in self.df.columns:
            self.df = self.df.drop(columns=["LogonType"])
            print("[INFO] Dropped LogonType column.")

        """
        # One-hot encode EXE names (additional feature engineering)
        print("[INFO] Encoding EXE names...")
        one_hot_cols = ["Exe"]
        one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

        # Transform EXE column into one-hot encoded format
        encoded_data = one_hot_encoder.fit_transform(self.df[one_hot_cols])
        encoded_df = pd.DataFrame(encoded_data, columns=one_hot_encoder.get_feature_names_out(one_hot_cols))

        # Drop original 'Exe' column and merge the new encoded dataframe
        self.df = self.df.drop(columns=one_hot_cols).reset_index(drop=True)
        self.df = pd.concat([self.df, encoded_df], axis=1)

        # Save one-hot encoder for later use
        joblib.dump(one_hot_encoder, self.encoder_path)
        """
        # One-hot encode EXE names (additional feature engineering)
        print("[INFO] Encoding EXE names...")
        one_hot_cols = ["Exe"]
        one_hot_encoder = None

        # Load existing encoder if available; otherwise, fit a new one
        try:
            one_hot_encoder = joblib.load(self.encoder_path)
            print("Loaded existing one-hot encoder.")
        except FileNotFoundError:
            print("No existing one-hot encoder found. Fitting a new one.")
            one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
            one_hot_encoder.fit(self.df[one_hot_cols])  # Fit encoder
            joblib.dump(one_hot_encoder, self.encoder_path)  # Save encoder

        # Store original 'Exe' column before encoding
        original_exe = self.df["Exe"].copy()

        # Transform EXE column into one-hot encoded format
        encoded_data = one_hot_encoder.transform(self.df[one_hot_cols])
        encoded_df = pd.DataFrame(encoded_data, columns=one_hot_encoder.get_feature_names_out(one_hot_cols))

        # Check for unseen categories by comparing columns
        seen_exes = set(one_hot_encoder.get_feature_names_out(one_hot_cols))
        current_exes = set(encoded_df.columns)
        unseen_exes = current_exes - seen_exes

        # Create a new column to indicate unseen Exes
        self.df["UnseenExe"] = self.df["Exe"].apply(lambda x: f"Exe_{x}" in unseen_exes)

        # Drop original 'Exe' column and merge the new encoded dataframe
        self.df = self.df.drop(columns=one_hot_cols).reset_index(drop=True)
        self.df = pd.concat([self.df, encoded_df], axis=1)


        # Label encode ordinal categorical features
        label_cols = ["AccountName", "AccountType", "Severity"]
        label_encoder = LabelEncoder()

        for col in label_cols:
            self.df[col] = label_encoder.fit_transform(self.df[col])  # Convert categorical labels to numeric

        print("[INFO] Categorical encoding complete.")

        # Normalize numerical features
        print("[INFO] Normalizing numerical features...")
        scaled_features = numerical_columns + label_cols
        scaler = StandardScaler()

        # Load existing scaler if available; otherwise, fit a new one
        try:
            scaler = joblib.load(self.scaler_path)
            print("Loaded existing scaler.")
        except FileNotFoundError:
            print("No existing scaler found. Fitting a new one.")
            scaler.fit(self.df[scaled_features])  # Fit scaler
            joblib.dump(scaler, self.scaler_path)  # Save scaler

        # Apply transformation
        self.df[scaled_features] = scaler.transform(self.df[scaled_features])

        # Drop columns with dtype 'object'
        object_columns = self.df.select_dtypes(include=['object']).columns
        self.df = self.df.drop(columns=object_columns)

        # Add the original 'Exe' column back to the DataFrame.
        self.df["OriginalExe"] = original_exe

        print("Preprocessing complete.")

    def print_info(self):
        """Print DataFrame structure and first few rows."""
        print(self.df.info())
        print(self.df.dtypes.to_string())


"""
import pandas as pd
import joblib
import re
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder

class CleanedDF:
    def __init__(self, file_path: str, scaler_path="models/scaler.pkl", encoder_path="models/encoder.pkl"):
        #Initialize the class with file path and paths to saved encoders/scalers.
        self.file_path = file_path
        self.scaler_path = scaler_path
        self.encoder_path = encoder_path
        self.df = self._load_data()  # Load data upon initialization

    def _load_data(self) -> pd.DataFrame:
        #Load CSV file into a Pandas DataFrame with proper data handling.
        try:
            print("Loading data...")
            df = pd.read_csv(self.file_path, low_memory=False)  # Read CSV file
        except Exception as e:
            print(f"Error loading file: {e}")
            return pd.DataFrame()  # Return empty DataFrame if there's an error

        # Extract the first executable name from the "Message" column if it exists
        if "Message" in df:
            df["Exe"] = df["Message"].apply(self._extract_exe)

        print("Data loaded and executables extracted.")
        return df

    @staticmethod
    def _extract_exe(message: str) -> str:
        #Extract first executable name from a log message if present.
        if isinstance(message, str):
            match = re.search(r'([a-zA-Z0-9_]+\.exe)', message)  # Regex to find .exe filenames
            return match.group(1) if match else None  # Return found filename or None
        return None

    def preprocess(self):
        #Preprocess the dataset: clean missing values, encode categorical data, and normalize numeric data.
        if self.df.empty:
            print("No data to preprocess.")
            return

        ############# Convert EventTime to a proper datetime format #############
        if "EventTime" in self.df:
            self.df["EventTime"] = pd.to_datetime(self.df["EventTime"], errors="coerce")

            # Convert datetime to UNIX timestamp (seconds since 1970)
            self.df["Timestamp"] = self.df["EventTime"].apply(lambda x: x.timestamp() if pd.notnull(x) else None)

            # Drop original EventTime column as it's redundant after conversion
            self.df.drop(columns=["EventTime"], inplace=True)

        # Extract time-based features from the timestamp
        self.df["DayOfWeek"] = self.df["Timestamp"].apply(lambda x: pd.to_datetime(x, unit='s').dayofweek if pd.notnull(x) else None)
        self.df["Month"] = self.df["Timestamp"].apply(lambda x: pd.to_datetime(x, unit='s').month if pd.notnull(x) else None)
        self.df["Year"] = self.df["Timestamp"].apply(lambda x: pd.to_datetime(x, unit='s').year if pd.notnull(x) else None)

        # Ensure time-based features are treated as numerical
        self.df[["Timestamp", "DayOfWeek", "Month", "Year"]] = self.df[["Timestamp", "DayOfWeek", "Month", "Year"]].apply(pd.to_numeric)

        ############# Define numerical and categorical columns #############
        numerical_columns = ["SeverityValue", "ProcessID", "ThreadID", "EventID"]
        categorical_columns = ["EventType", "Exe", "SourceName", "AccountName", "AccountType", "Severity"]

        # Convert numerical columns to float and handle missing values
        for col in numerical_columns:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")  # Convert to numeric
            self.df[col] = self.df[col].fillna(self.df[col].median())  # Fill missing values with median

        # Convert categorical columns to string and handle missing values
        for col in categorical_columns:
            self.df[col] = self.df[col].fillna("Unknown").astype(str)  # Replace missing values with "Unknown"

        # One-hot encode EXE names (additional feature engineering)
        print("[INFO] Encoding EXE names...")
        one_hot_cols = ["Exe"]
        one_hot_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

        # Transform EXE column into one-hot encoded format
        encoded_data = one_hot_encoder.fit_transform(self.df[one_hot_cols])
        encoded_df = pd.DataFrame(encoded_data, columns=one_hot_encoder.get_feature_names_out(one_hot_cols))

        # Drop original 'Exe' column and merge the new encoded dataframe
        self.df = self.df.drop(columns=one_hot_cols).reset_index(drop=True)
        self.df = pd.concat([self.df, encoded_df], axis=1)

        # Save one-hot encoder for later use
        joblib.dump(one_hot_encoder, self.encoder_path)

        # Label encode ordinal categorical features
        label_cols = ["AccountName", "AccountType", "Severity"]
        label_encoder = LabelEncoder()

        for col in label_cols:
            self.df[col] = label_encoder.fit_transform(self.df[col])  # Convert categorical labels to numeric

        print("[INFO] Categorical encoding complete.")

        # Normalize numerical features
        print("[INFO] Normalizing numerical features...")
        scaled_features = numerical_columns + label_cols
        scaler = StandardScaler()

        # Load existing scaler if available; otherwise, fit a new one
        try:
            scaler = joblib.load(self.scaler_path)
            print("Loaded existing scaler.")
        except FileNotFoundError:
            print("No existing scaler found. Fitting a new one.")
            scaler.fit(self.df[scaled_features])  # Fit scaler
            joblib.dump(scaler, self.scaler_path)  # Save scaler

        # Apply transformation
        self.df[scaled_features] = scaler.transform(self.df[scaled_features])

        # Drop columns with dtype 'object'
        object_columns = self.df.select_dtypes(include=['object']).columns
        self.df = self.df.drop(columns=object_columns)

        print("Preprocessing complete.")

    def print_info(self):
        #Print DataFrame structure and first few rows.
        print(self.df.info())
        print(self.df.dtypes.to_string())
"""
