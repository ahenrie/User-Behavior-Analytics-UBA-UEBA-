import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve, auc
import joblib
import matplotlib.pyplot as plt

class IsolationForestModel:
    def __init__(self, df: pd.DataFrame, contamination: float = 0.01, n_estimators: int = 100):
        """
        Initialize the Isolation Forest model.

        :param df: Preprocessed DataFrame (excluding raw timestamps)
        :param contamination: Expected proportion of anomalies in the data
        :param n_estimators: Number of trees in the Isolation Forest
        """
        self.df = df
        self.model = IsolationForest(n_estimators=n_estimators, contamination=contamination, random_state=42)

    def train(self):
        """
        Converting Period to year and month: The MonthYear column is converted into two separate columns: Year and Month. This way, they are represented as integers, which can be processed by the model.
        Drop the MonthYear column: After extracting the year and month, drop the MonthYear column to prevent any issues during model training.
        """
        # Convert Period to numeric representation: year and month
        if 'MonthYear' in self.df.columns:
            self.df['Year'] = self.df['MonthYear'].dt.year
            self.df['Month'] = self.df['MonthYear'].dt.month
            self.df.drop(columns=['MonthYear'], inplace=True)

        # Ensure only numerical columns and encoded categorical features are used
        # Drop any remaining non-numeric columns (e.g., datetime, original categorical columns)
        columns_to_use = self.df.select_dtypes(include=["number"]).columns
        X_train = self.df[columns_to_use]

        # Fit the model
        self.model.fit(X_train)

    def predict(self, new_data: pd.DataFrame):
        """
        Predict anomalies in new incoming logs.

        :param new_data: DataFrame with the same structure as training data.
        :return: DataFrame with an added 'Anomaly' column (-1 = anomaly, 1 = normal).
        """
        new_data["Anomaly"] = self.model.predict(new_data)
        return new_data

    def save_model(self, filename="isolation_forest.pkl"):
        """
        Save the trained model to a file.
        """
        joblib.dump(self.model, filename)
        print(f"Model saved to {filename}.")

    def load_model(self, filename="isolation_forest.pkl"):
        """
        Load a trained model from a file.
        """
        self.model = joblib.load(filename)
        print(f"Model loaded from {filename}.")
