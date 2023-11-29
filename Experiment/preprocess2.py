import pandas as pd
from tqdm import tqdm

# Use tqdm.pandas() to enable progress_apply for pandas operations
tqdm.pandas()

# Read in the filtered DataFrame with tqdm
df_filtered = pd.read_csv('filtered_data_top3.csv')

# Convert the 'published' column to datetime format with tqdm
df_filtered['published'] = df_filtered['published'].progress_apply(pd.to_datetime, errors='coerce')

# Create a new 'date' column that stores only the date from the 'published' column with tqdm
df_filtered['date'] = df_filtered['published'].progress_apply(lambda x: x.date())

# Drop the 'published' column
df_filtered = df_filtered.drop(columns=['published'])


# Group by 'date' and 'stock', then concatenate the 'text' column within each group with tqdm
df_combined = df_filtered.groupby(['date', 'stock'])['text'].progress_apply(lambda x: ' '.join(x)).reset_index()

# Save the combined DataFrame to a CSV file without tqdm
df_combined.to_csv('combined_data_top3.csv', index=False)


print('Combined data has been successfully saved to combined_data.csv.')
