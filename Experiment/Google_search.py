import os
import json
import datetime
from googlesearch import search

# Directory to store results
results_dir = "Data/News/GCS"

# Check if the directory exists, if not, create it
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Log file for progress
progress_file = "Data/News/GCS/progress.txt"

# Check if the progress file exists, if not, create it
if not os.path.exists(progress_file):
    with open(progress_file, 'w'):
        pass

# Dates range from January 1, 2023, to October 31, 2023
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 10, 31)

# Stocks to search for
stocks = ["apple", "amazon", "meta"]

# Function to perform a Google search and save results
def perform_search_and_save(date, stock):
    query = f"{stock} financial news"
    results = []

    # Perform the Google search
    for result in search(query, num=5, stop=5, pause=2):
        results.append(result)

    # Save the results to a JSON file
    result_data = {
        "Date": date.strftime("%Y-%m-%d"),
        "Stock": stock,
        "Results": results
    }

    result_dir = os.path.join(results_dir, date.strftime("%Y%m%d"))
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    result_filename = os.path.join(result_dir, f"{stock}.json")

    with open(result_filename, 'w') as json_file:
        json.dump(result_data, json_file)

    # Log the date and stock combination to progress file
    with open(progress_file, 'a') as progress:
        progress.write(f"{date.strftime('%Y-%m-%d')} - {stock}\n")

# Loop through the date range and stocks
current_date = start_date
while current_date <= end_date:
    for stock in stocks:
        # Check if the combination has already appeared in the progress file
        progress_combination = f"{current_date.strftime('%Y-%m-%d')} - {stock}\n"
        with open(progress_file, 'r') as progress:
            if progress_combination in progress.readlines():
                continue  # Skip if already processed

        # Perform search and save results
        perform_search_and_save(current_date, stock)

    # Move to the next date
    current_date += datetime.timedelta(days=1)
