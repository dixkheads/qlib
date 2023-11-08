import pandas as pd
import json
from tqdm import tqdm
import os
import json

# Directory where your JSON files are located (assuming they're all in the 'data' folder).
data_folder = 'data/original'

# Initialize an empty list to store the combined data.
data_list = []

# Iterate over the JSON files in the 'data' folder and append their contents to 'combined_data'.
for filename in os.listdir(data_folder):
    if filename.endswith(".json"):
        json_file = os.path.join(data_folder, filename)
        with open(json_file, 'r') as file:
            data = json.load(file)
            df_tmp = pd.DataFrame(data['data'])
            print(df_tmp)
            data_list.append(df_tmp)

# Create a DataFrame from the list of dictionaries.
df = pd.concat(data_list, ignore_index=True)

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

# Convert the 'published' column to datetime while handling non-datetime values by setting them to NaT.
filtered_df['published'] = pd.to_datetime(filtered_df['published'], errors='coerce', utc=True)

# Filter the DataFrame to keep only rows with valid datetime values in the 'published' column.
filtered_df = filtered_df[filtered_df['published'].notna()]

# Group the DataFrame by the "published" date and count distinct values in the "stock" column.
daily_stock_counts = filtered_df.groupby(filtered_df['published'].dt.date)['stock'].nunique()

# Create a bar plot to show the number of distinct stocks for each day.
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(daily_stock_counts.index, daily_stock_counts)

import matplotlib.dates as mdates

# Set the x-axis tick locator and formatter to show only the start date and end date.
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=[1, 30]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

# Rotate the x-axis tick labels for better readability.
plt.xticks(rotation=45)

plt.xlabel('Date')
plt.ylabel('Distinct Stock Count')
plt.title('Distinct Stock Count per Day')
plt.tight_layout()

plt.show()

num_entries = filtered_df.shape[0]
print(f"Number of entries in filtered_df: {num_entries}")

# Convert the 'published' column to datetime while handling non-datetime values by setting them to NaT.
filtered_df['published'] = pd.to_datetime(filtered_df['published'], errors='coerce')

# Filter the DataFrame to keep only rows with valid datetime values in the 'published' column.
filtered_df = filtered_df.dropna(subset=['published'])

# Group the DataFrame by 'published', 'stock', and 'prediction' and count occurrences.
count_df = filtered_df.groupby(['published', 'stock', 'prediction']).size().unstack(fill_value=0)

# Rename columns to represent prediction values.
count_df.columns = ['prediction_-1', 'prediction_0', 'prediction_1']

# Reset the index to make 'published' and 'stock' as regular columns.
count_df = count_df.reset_index()

# Assuming 'count_df' contains the count of each prediction value for each stock on each day.

# Rename the 'published' column to 'date' and retain only the year-month-day information.
count_df['date'] = count_df['published'].dt.strftime('%Y-%m-%d')

# Drop the original 'published' column.
count_df = count_df.drop(columns='published')

count_df = count_df.groupby(['date', 'stock']).sum().reset_index()

# Assuming 'count_df' is the DataFrame with prediction counts and 'dftxt' is another DataFrame containing 'Ticker'.

# Get the top 20 stocks with the highest occurrences in count_df
top_20_stocks = count_df['stock'].value_counts().nlargest(20).index.tolist()

# Save the top 20 stocks to a text file named top20.txt with additional columns
with open('top20.txt', 'w') as file:
    file.write("Stock\tStart_date\tEnd_date\n")  # Write header

    # Write data for each stock
    for stock in top_20_stocks:
        file.write(f"{stock}\t2008-08-07\t2099-12-31\n")

# Now, 'count_df' has the 'date' column with year-month-day information.

# Convert 'date' column in 'count_df' to the same datetime format.
count_df['date'] = pd.to_datetime(count_df['date'])

# Calculate the frequency of each stock in count_df
stock_frequency = count_df['stock'].value_counts()

# Select the top 20 stocks by frequency
top_20_stocks = stock_frequency.head(20)

# Plot the frequency of the top 20 stocks
plt.figure(figsize=(10, 6))
top_20_stocks.plot(kind='bar')
plt.title('Frequency of Top 20 Stocks')
plt.xlabel('Stock')
plt.ylabel('Frequency')
plt.show()

# Get a list of all unique dates and stocks.
all_dates = count_df['date'].unique()
all_stocks = dftxt['Ticker'].unique()

# Create an empty DataFrame to store missing combinations of dates and stocks.
missing_data = pd.DataFrame(columns=['date', 'stock', 'prediction_-1', 'prediction_0', 'prediction_1'])

# Set up tqdm for the progress bar
pbar = tqdm(total=len(all_dates) * len(all_stocks))

# Loop through all unique dates and stocks to check for missing entries.
for date in all_dates:
    for stock in all_stocks:
        pbar.update(1)  # Update progress bar
        if not ((count_df['date'] == date) & (count_df['stock'] == stock)).any():
            # If the combination of date and stock is missing, add a row with zero values.
            missing_data = pd.concat([missing_data, pd.DataFrame({'date': [date], 'stock': [stock], 'prediction_-1': [0], 'prediction_0': [0], 'prediction_1': [0]})])

pbar.close()  # Close the progress bar
# Combine the missing data with the original count_df.
count_df = pd.concat([count_df, missing_data])

# Reset the index of the updated count_df.
count_df = count_df.reset_index(drop=True)

# count_df[['prediction_-1', 'prediction_0', 'prediction_1']] = 0

# Assuming 'count_df' is the DataFrame you want to save

# Replace 'gyroc' with your actual username
username = 'gyroc'

# Define the file path to the desktop
file_path = fr"C:\Users\{username}\Desktop\count_df.csv"

# Save 'count_df' as a CSV file on the desktop
count_df.to_csv(file_path, index=False)


# count_df['volume'] = (count_df['prediction_1'] - count_df['prediction_-1'])#  * 10000000 + 20000000
#
# print(count_df.head())
#
# # Get a list of all unique stocks.
# all_stocks = dftxt['Ticker'].unique()
#
# # Set up tqdm for the progress bar
# pbar = tqdm(total=len(all_stocks))
#
# # Loop through each stock in count_df and save to separate CSV files
# for stock in all_stocks:
#     stock_data = count_df[count_df['stock'] == stock]
#
#     if not stock_data.empty:
#         stock_data.to_csv(f"data/threeway_csv/{stock}.csv", index=False)
#
#     pbar.update(1)  # Update progress bar
#
# pbar.close()  # Close the progress bar

# python scripts/dump_bin.py dump_all --csv_path  ~/.qlib/qlib_data/threeway_csv --qlib_dir ~/.qlib/qlib_data/threeway_us_data --date_field_name date --exclude_fields stock


