import pandas as pd

# Read the CSV file
file_path = r'C:\Users\gyroc\Desktop\x_train.csv'
df = pd.read_csv(file_path)

# Print the DataFrame
print(df)
print(df.index)