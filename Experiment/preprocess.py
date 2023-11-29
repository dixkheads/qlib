import os
import json
import pandas as pd
from tqdm import tqdm

# Function to check if keywords are contained in the text
import re

def contains_keywords(text, keywords):
    # Adding word boundary (\b) checks to ensure matching standalone words
    return any(re.search(rf'\b{re.escape(keyword)}\b', text, flags=re.IGNORECASE) for keyword in keywords)

# Create NASDAQ100 list from the provided table with keywords
nasdaq100_data = [
    ('AAPL', 'Apple', '2008-08-07', '2099-12-31', ['Apple', 'iPhone', 'Mac', 'iOS', 'iPad', 'MacBook', 'iMac', 'iTunes', 'iCloud', 'Watch']),
    ('FB', 'Facebook', '2008-08-07', '2099-12-31', ['Facebook', 'Meta', 'Instagram', 'WhatsApp', 'Messenger', 'Oculus', 'FB Live', 'FB Marketplace', 'FB Portal', 'FB Gaming']),
    ('AMZN', 'Amazon', '2008-08-07', '2099-12-31', ['Amazon', 'AWS', 'Prime', 'Kindle', 'Echo', 'Alexa', 'Whole Foods', 'Twitch', 'Audible', 'Ring']),
]

# Directory path where JSON files are stored
data_directory = 'Data/News'

# List to store filtered data
filtered_data = []

# Traverse subdirectories and files in the directory
for root, dirs, files in os.walk(data_directory):
    for filename in tqdm(files, desc="Processing Files", unit="file"):
        if filename.endswith('.json'):
            file_path = os.path.join(root, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    json_data = json.load(file)

                    # Check if the required fields are present in the JSON
                    if 'published' in json_data and 'text' in json_data:
                        published_date = json_data['published']
                        text_content = json_data['text']

                        # Check which NASDAQ100 stocks are present in the text
                        for stock_code, _, _, _, keywords in nasdaq100_data:
                            if contains_keywords(text_content, keywords):
                                filtered_data.append({'published': published_date, 'text': text_content, 'stock': stock_code})

                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {file_path}")

# Create a DataFrame from the filtered data
df_filtered = pd.DataFrame(filtered_data)

# Convert the 'published' column to datetime format
df_filtered['published'] = pd.to_datetime(df_filtered['published'], errors='coerce')

# Drop rows with missing dates
df_filtered = df_filtered.dropna(subset=['published'])

# Sort the DataFrame by date
df_filtered = df_filtered.sort_values(by='published')

# Save the DataFrame to a CSV file
df_filtered.to_csv('filtered_data_top3.csv', index=False)

print('Filtered data has been successfully saved to filtered_data.csv.')
