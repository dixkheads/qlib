import pandas as pd
import json

# Replace '2018_01_scored_one_tenth.json' with the actual path to your JSON file.
json_file = 'data/2018_01_scored_selected.json'

# Read the JSON file into a Python list of dictionaries.
with open(json_file, 'r') as file:
    data = json.load(file)

# Extract the 'data' key from the dictionary.
data_list = data['data']

# Create a DataFrame from the list of dictionaries.
df = pd.DataFrame(data_list)

# Display the first few rows of the DataFrame.
print(df.columns)

# If your JSON keys have '=' instead of ':', you should replace them like this:
# df = pd.DataFrame(data)

# Assuming "title" and "text" are the columns you want to remove.
# columns_to_remove = ["title", "text"]

# Use the drop method to remove the specified columns.
# df = df.drop(columns=columns_to_remove)

# Display the first few rows of the DataFrame.
print(df.head())

# Replace 'all.txt' with the actual path to your text file.
txt_file = 'data/all.txt'

# Define the column names for the DataFrame.
column_names = ['Ticker', 'StartDate', 'EndDate']

# Read the tab-separated text file into a DataFrame.
dftxt = pd.read_csv(txt_file, sep='\t', names=column_names, parse_dates=['StartDate', 'EndDate'])

# Display the DataFrame.
print(dftxt)

filtered_df = df[df['stock'].isin(dftxt['Ticker'])]

import matplotlib.pyplot as plt

# Assuming you have a filtered DataFrame named filtered_df
filtered_df['prediction'].hist(bins=3)  # Adjust the number of bins as needed

# Add labels and title
plt.xlabel('Prediction')
plt.ylabel('Frequency')
plt.title('Prediction Histogram')

# Show the histogram
plt.show()

# Assuming you have a filtered DataFrame named filtered_df with a "published" column.
# You've already loaded and filtered the data as you mentioned.

# Convert the "published" column to a datetime object.
filtered_df['published'] = pd.to_datetime(filtered_df['published'])

# Group the DataFrame by the "published" date and count distinct values in the "stock" column.
daily_stock_counts = filtered_df.groupby(filtered_df['published'].dt.date)['stock'].nunique()

# Create a bar plot to show the number of distinct stocks for each day.
daily_stock_counts.plot(kind='bar', figsize=(12, 6))
plt.xlabel('Date')
plt.ylabel('Distinct Stock Count')
plt.title('Distinct Stock Count per Day')
plt.show()


