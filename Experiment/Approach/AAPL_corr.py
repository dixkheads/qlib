import pandas as pd
import matplotlib.pyplot as plt

# Read count_df.csv from the desktop
username = 'gyroc'
count_df = pd.read_csv(fr"C:\Users\{username}\Desktop\count_df.csv")

# Read AAPL.csv
AAPL = pd.read_csv("data/AAPL_tmp/AAPL.csv")

# Add a new column 'change' to AAPL DataFrame
AAPL['change'] = (AAPL['Close'] / AAPL['Open'])

# Filter count_df for stock == 'AAPL'
count_df_AAPL = count_df[count_df['stock'] == 'AAPL']

# Convert 'date' columns to datetime for both DataFrames
count_df_AAPL['date'] = pd.to_datetime(count_df_AAPL['date'])
AAPL['date'] = pd.to_datetime(AAPL['Date'])

# Merge count_df and AAPL on 'date'
combined_df = pd.merge(count_df_AAPL, AAPL, on='date', how='inner')
combined_df.to_csv('cvn.df', index=False)
print(combined_df)

# Display Pearson correlation matrix for the combined DataFrame
pearson_corr = combined_df.corr(method='pearson')
print("Pearson Correlation Matrix:")
print(pearson_corr)

# Plotting the Pearson correlation matrix
plt.figure(figsize=(8, 6))
plt.imshow(pearson_corr, cmap='coolwarm', interpolation='none')
plt.colorbar()
plt.title('Pearson Correlation Matrix')
plt.xticks(range(len(pearson_corr.columns)), pearson_corr.columns, rotation='vertical')
plt.yticks(range(len(pearson_corr.columns)), pearson_corr.columns)
plt.show()