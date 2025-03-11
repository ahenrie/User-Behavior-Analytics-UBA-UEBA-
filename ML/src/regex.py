import re
import pandas as pd

def extract_exe(message: str) -> str:
    """Extract the first executable name (ending in .exe) from a log message."""
    if isinstance(message, str):
        # A more lenient regex that allows for extra spaces or other potential issues
        match = re.search(r'([a-zA-Z0-9_]+\.exe)', message)
        if match:
            return match.group(1)
        else:
            return None
    return None


def main():
    df = pd.read_csv('data/badLogs.csv')
    # Apply extract_exe to each row in the 'Message' column
    df["Exe"] = df["Message"].apply(extract_exe)

    # Print unique values from the 'Exe' column to see what was extracted
    print(df["Exe"].unique())

if __name__ == "__main__":
    main()
