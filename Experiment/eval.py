import pandas as pd
from tqdm import tqdm
from transformers import BertTokenizer, BertModel
import torch

# Check if a GPU is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Define the file paths
input_file_path = 'combined_data.csv'
output_file_path = 'bert_embeddings_data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file_path)

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
model = model.to(device)

# Function to generate BERT embeddings for a given text
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = inputs.to(device)
    outputs = model(**inputs)
    # Extract embeddings from the second-to-last layer (index -2)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().cpu().numpy()
    return embeddings

# Create new columns for BERT embeddings
embeddings_col_names = [f'bert_embedding_{i}' for i in range(768)]  # 768 is the size of BERT embeddings
for col_name in embeddings_col_names:
    df[col_name] = 0.0

# Use tqdm to track progress
tqdm.pandas(desc="Generating BERT embeddings", unit="entry")
df['text'].progress_apply(lambda x: get_bert_embedding(x))

# Save the DataFrame with BERT embeddings to a new CSV file
df.to_csv(output_file_path, index=False)

print(f"BERT embeddings generated and saved to {output_file_path}")
