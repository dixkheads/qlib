import pandas as pd

# Replace 'gyroc' with your actual username
username = 'gyroc'

# Define the file paths to the CSV files on the desktop
baseline_path = fr"C:\Users\{username}\Desktop\FI_baseline.csv"
adv_path = fr"C:\Users\{username}\Desktop\FI_adv.csv"

# Read the CSV files into DataFrames
baseline_df = pd.read_csv(baseline_path)
adv_df = pd.read_csv(adv_path)

# Extract 'feature' columns from both DataFrames
baseline_features = set(baseline_df['feature'])
adv_features = set(adv_df['feature'])

# Find the differences between the 'feature' columns
unique_to_baseline = baseline_features - adv_features
unique_to_adv = adv_features - baseline_features

# Display the unique features in each file
print("Unique features in FI_baseline.csv:", unique_to_baseline)
print("Unique features in FI_adv.csv:", unique_to_adv)
