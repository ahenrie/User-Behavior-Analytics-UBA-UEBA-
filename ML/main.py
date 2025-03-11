from src.cleaner import CleanedDF
from src.pikl_maker import IsolationForestModel
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # Clean CSV
    #cleaned_data = CleanedDF('data/fakelogs.csv')
    #cleaned_data.preprocess()
    #cleaned_data.print_info()

    # Train model using the CleanedDF
    newModel = IsolationForestModel('models/isolation_forest.pkl')
    #newModel.train(cleaned_data.df)
    newModel.load_model()

    # Bring in bad logs with some bad exe names
    bad_data = CleanedDF('data/badLogs.csv')
    bad_data.preprocess()

    # Predict
    predictions, anomaly_scores = newModel.predict(bad_data.df)
    bad_data.df["Anomaly"] = predictions
    anomalies = bad_data.df[bad_data.df["Anomaly"] == -1]

    # Re-add the OriginalExe column.
    anomalies["Exe"] = bad_data.df.loc[anomalies.index, "OriginalExe"]

    suspicious_exes = anomalies["Exe"].value_counts()

    print("🚨 Suspicious Executables:")
    print(suspicious_exes)
    print("\nAnomalous Rows:\n")
    print(anomalies)

    # Plot anomaly scores as a scatter plot with anomaly highlighting
    normal_indices = np.where(predictions == 1)[0]
    anomaly_indices = np.where(predictions == -1)[0]

    plt.scatter(normal_indices, anomaly_scores[normal_indices], label="Normal", color="blue", s=10)
    plt.scatter(anomaly_indices, anomaly_scores[anomaly_indices], label="Anomaly", color="red", s=20)

    plt.title("Anomaly Scores Scatter Plot with Highlighted Anomalies")
    plt.xlabel("Data Point Index")
    plt.ylabel("Anomaly Score")
    plt.legend()
    plt.show()
