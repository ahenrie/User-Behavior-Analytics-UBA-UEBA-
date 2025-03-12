from sklearn.ensemble import IsolationForest
import joblib
import pandas as pd

class IsolationForestModel:
    def __init__(self, model_path="isolation_forest.pkl", contamination=0.1):
        self.model_path = model_path
        self.model = IsolationForest(
            n_estimators=100,
            max_samples="auto",
            random_state=42,
            contamination=contamination
        )

    def train(self, df: pd.DataFrame):
        """Train Isolation Forest model on preprocessed data."""
        print("Training Isolation Forest model...")

        # Drop non-numeric columns
        non_numeric_cols = df.select_dtypes(exclude=['number']).columns
        numeric_df = df.drop(columns=non_numeric_cols)

        self.model.fit(numeric_df)
        joblib.dump(self.model, self.model_path)
        print("Model saved successfully.")

    def predict(self, df: pd.DataFrame):
        """Predict anomalies in new log data."""
        print("Predicting anomalies...")

        # Drop non-numeric columns (match training logic)
        non_numeric_cols = df.select_dtypes(exclude=['number']).columns
        numeric_df = df.drop(columns=non_numeric_cols)

        predictions = self.model.predict(numeric_df)  # -1 = Anomaly, 1 = Normal
        anomaly_scores = self.model.decision_function(numeric_df)  # Lower = More anomalous
        return predictions, anomaly_scores

    def load_model(self):
        """Load a pre-trained model."""
        print("Loading Isolation Forest model...")
        self.model = joblib.load(self.model_path)
