import pandas as pd
import json

# Replace '2018_01_scored_one_tenth.json' with the actual path to your JSON file.
json_file = '2018_01_scored_one_tenth.json'

# Read the JSON file into a Python list of dictionaries.
with open(json_file, 'r') as file:
    data = json.load(file)

# Create a DataFrame from the list of dictionaries.
df = pd.DataFrame(data)

# If your JSON keys have '=' instead of ':', you should replace them like this:
# df = pd.DataFrame(data)

# Display the first few rows of the DataFrame.
print(df.head())

# Replace 'all.txt' with the actual path to your text file.
txt_file = 'all.txt'

# Define the column names for the DataFrame.
column_names = ['Ticker', 'StartDate', 'EndDate']

# Read the tab-separated text file into a DataFrame.
dftxt = pd.read_csv(txt_file, sep='\t', names=column_names, parse_dates=['StartDate', 'EndDate'])

# Display the DataFrame.
print(df)