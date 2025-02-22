import pandas as pd

csv_file = "../test.csv"
df = pd.read_csv(csv_file)

# Check the first few rows of the DataFrame
print("First few rows of the CSV:")
print(df.head())

# Check the column names
print("\nColumn names:")
print(df.columns)

# Check the data types of the columns
print("\nData types of columns:")
print(df.dtypes)

# Check for any missing values
print("\nMissing values in the DataFrame:")
print(df.isnull().sum())

# Check the number of rows and columns
print("\nShape of the DataFrame:")
print(df.shape)

# Verify that the date column has been properly parsed as a datetime object
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime and handle errors
    print("\nDate column after conversion to datetime:")
    print(df['Date'].head())

# Check for any specific log entries or patterns
# For example, you can print a specific sample row based on a condition
sample_row = df[df['Severity'] == 'High']  # Replace with a condition you'd like to test
print("\nSample rows where severity is High:")
print(sample_row.head())
