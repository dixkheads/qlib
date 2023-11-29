# {Summary of {stock} in your dict}.
# Given the random finance related texts scrapped from web on a certain date, respond in the following json format. DO NOT respond anything other than json:
# {Summary: Summarize the text in regards to {stock} in a sentence,
# Impact: Explain how part of the text may be impacting/relevant to {stock} in a sentence,
# Keywords: [10 Keywords of the news in regards to {stock}].}
# The news is as follows: {text}
#
# write me a python program that reads in combined_data_top3.csv, and for each entry in the data_top3, split it into multiple entries by segmenting its text column into segments of 10,000 tokens or less. Then for each segmented entry call gpt-3.5-turbo-1106 with the following prompt and store each response immediately after each GPT3.5 turbo call to a single json file as Data/Summary/{date}_{a random uuid}.json:
# {Summary of {stock} in your dict}. Given the random finance related texts scrapped from web on a certain date, respond in the following json format. DO NOT respond anything other than json:
# {Summary: Summarize the text in regards to {stock} in a sentence,
# Impact: Explain how part of the text may be impacting/relevant to {stock} in a sentence,
# Keywords: [10 Keywords of the news in regards to {stock}].}
# The news is as follows: {text}

import pandas as pd
import openai
import uuid
import json
import time
import datetime
import nltk
import os
from tqdm import tqdm

# Set your OpenAI API key here
openai.api_key = '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'

key_set = ['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', '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']

# Read the combined_data_top3.csv file
df = pd.read_csv('combined_data_top3.csv')

gpt_prompt_template = '{csum}. Given the random texts that may relate to {stock} scrapped from web that may be ' \
                      'related to {stock} on a certain date, respond in the following json format. REMEMBER THERE SHOULD BE COMMAS BETWEEN FIELDS AND DO NOT respond ' \
                      'anything other than json:{{"Summary": "Summarize the text in regards to {stock} in two sentences",' \
                      '"Impact": "Explain how part(s) of the text may directly/indirectly impacting/relevant to {stock} in two sentences. If there is no direct impact consider indirect impact such as technology industry in general or the rivals of {stock}",' \
                      '"Keywords": [10 Keywords of the news in regards to {stock}]}}\nThe news is as follows: \n{text}'


max_retries = 10

company_summary = {
  "AAPL": "Apple Inc. (AAPL) is a multinational technology company known for its innovative products such as the "
          "iPhone, Mac, and iPad. It is a major player in the consumer electronics and software industries, "
          "with a focus on design and user experience. Industry: Technology. Founded: April 1, 1976. Positive "
          "Factors: Strong brand reputation, Innovative product lineup, Robust ecosystem (iOS, macOS), "
          "Healthy financials, Global market presence, Strong customer loyalty, Growing services segment, Successful "
          "retail strategy (Apple Stores), Diverse revenue streams, Strategic partnerships. Negative Factors: "
          "Dependency on iPhone sales, High product pricing, Intense competition in the tech industry, Reliance on "
          "manufacturing in China, Potential impact of global economic downturns, Risks associated with supply chain "
          "management, Legal challenges and patent disputes, Consumer preferences shifting to other brands, "
          "Vulnerability to cybersecurity threats, Challenges in entering new emerging markets.",
  "AMZN": "Amazon.com Inc. (AMZN) is a global e-commerce and cloud computing giant. Founded by Jeff Bezos, "
          "the company has expanded its business to include various services such as online retail, streaming, "
          "and artificial intelligence through its virtual assistant, Alexa. Industry: E-commerce, Cloud Computing. "
          "Founded: July 5, 1994. Positive Factors: Dominant position in e-commerce, Highly diversified business "
          "segments, Successful Prime membership program, Continuous innovation (e.g., Amazon Web Services), "
          "Global logistics and delivery network, Strong financial performance, Growing presence in entertainment ("
          "Amazon Studios), Expansion into healthcare (Amazon Pharmacy), Strategic acquisitions (e.g., Whole Foods), "
          "Investments in cutting-edge technologies. Negative Factors: Antitrust scrutiny and regulatory challenges, "
          "Labor practices and employee relations controversies, Dependency on third-party sellers, Increasing "
          "competition in the cloud computing space, Environmental impact concerns, Potential impact of economic "
          "downturns on consumer spending, Challenges in international expansion, Risks associated with data security "
          "and privacy, Dependency on AWS for a significant portion of profits, Potential backlash from "
          "brick-and-mortar retailers.",
  "FB": "Facebook, Inc. (FB) is a social media and technology company founded by Mark Zuckerberg. It is widely known "
        "for its social networking platform, Facebook, and owns popular services like Instagram and WhatsApp. The "
        "company has played a significant role in shaping the way people connect and share information online. "
        "Industry: Social Media, Technology. Founded: February 4, 2004. Positive Factors: Dominant position in social "
        "media, High user engagement across platforms, Successful acquisitions (Instagram, WhatsApp), "
        "Strong advertising revenue model, Continuous product innovation, Global user base, Investments in virtual "
        "reality (Oculus), Strategic partnerships with content creators, Growing presence in e-commerce (Facebook "
        "Marketplace), Commitment to user privacy and safety. Negative Factors: Data privacy controversies and "
        "regulatory scrutiny, Concerns about misinformation and fake news, Competition from emerging social media "
        "platforms, Impact of changes in advertising algorithms, User fatigue and potential decline in engagement, "
        "Legal challenges and antitrust investigations, Dependency on advertising for revenue, Challenges in "
        "addressing content moderation issues, Potential user backlash against new features, Risks associated with "
        "entry into new business segments."
}

# Define the path for the Progress.txt file
progress_file_path = "Data/Summary/progress.txt"
# Define a function to log progress

# Define a function to check if UUID is in progress
def is_uuid_in_progress(uuid):
    with open(progress_file_path, 'r') as progress_file:
        for line in progress_file:
            progress_uuid, _ = line.strip().split(',')
            if progress_uuid == uuid:
                return True
    return False

def log_progress(uuid, timestamp):
    with open(progress_file_path, 'a') as progress_file:
        progress_file.write(f"{uuid},{timestamp}\n")
def get_latest_json_date():
    # Get a list of all JSON files in the 'Data/Summary/' directory
    json_files = [f for f in os.listdir('Data/Summary/') if f.endswith('.json')]

    if not json_files:
        # If no JSON files are found, return None
        return None

    # Sort the JSON files by modification time
    latest_json_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join('Data/Summary/', f)))

    # Extract the date from the latest JSON file
    date_str = latest_json_file.split('_')[0]
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
# Function to call GPT-3.5 Turbo and store the response to a JSON file
def call_gpt3_and_store_response(stock, text, date, uuid_in=uuid.uuid4(), retry_count=0):
    if retry_count >= max_retries:
        print(f"Max retries reached. Skipping entry: {date} - {stock}")
        return

    prompt = gpt_prompt_template.format(stock=stock, text=text, csum=company_summary[stock])
    print(prompt)

    # Call GPT-3 Chat
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are an experienced equity analyst at SIG focusing on technology market."},
                {"role": "user", "content": prompt}
            ]
        )

        # Try to decode the JSON response
        try:
            # Assuming response["choices"][0]["message"]["content"] contains the entire response string
            full_response = response["choices"][0]["message"]["content"]

            # Find the index of the first open curly bracket
            start_index = full_response.find('{')

            # Find the index of the last close curly bracket
            end_index = full_response.rfind('}')

            # Extract the content between the first open curly bracket and the last close curly bracket
            extracted_content = full_response[start_index : end_index + 1].strip()
            # Decode the JSON response
            response_content = json.loads(extracted_content)
            # Print the raw content for troubleshooting
            # print("Raw content of the response:", response["choices"][0]["message"]["content"])

            # Extract relevant information from the decoded JSON response
            gpt_response = {
                "Summary": response_content.get("Summary", ""),
                "Impact": response_content.get("Impact", ""),
                "Keywords": response_content.get("Keywords", []),
                "date": date,
                "stock": stock
            }

            print(gpt_response)
            # Save the response to a JSON file
            date_folder = os.path.join("Data/Summary", date)

            # Check if the folder for the date already exists
            if not os.path.exists(date_folder):
                os.makedirs(date_folder)

            # Create a unique filename with a random UUID
            filename = os.path.join(date_folder, f"{uuid_in}.json")

            with open(filename, 'w') as json_file:
                json.dump(gpt_response, json_file)

            # Log progress to Progress.txt
            log_progress(uuid_in, time.strftime("%Y-%m-%d %H:%M:%S"))

        except json.JSONDecodeError:
            print(f"Error decoding JSON. Retrying{retry_count}...")
            # Print the output
            print(f'The output is: {response["choices"][0]["message"]["content"]}')

            # If there's an error, store the response in a text file
            error_filename = f"Data/Summary/Error/{date}_{uuid_in}.txt"
            with open(error_filename, 'w') as error_file:
                error_file.write(response["choices"][0]["message"]["content"])
            time.sleep(5)  # Wait for 5 seconds before retrying
            call_gpt3_and_store_response(stock, text, date, uuid_in=uuid_in, retry_count=retry_count + 2)

    except openai.error.OpenAIError as e:
        print(f"Error calling GPT-3 Chat: {e}")

        if openai.api_key == key_set[0]:
            openai.api_key = key_set[1]
        else:
            openai.api_key = key_set[0]

        # If there's an error, you may want to retry after waiting for a short period
        print(f"Retrying after a brief wait{retry_count}...")
        time.sleep(5)  # Wait for 5 seconds before retrying
        call_gpt3_and_store_response(stock, text, date, uuid_in=uuid_in, retry_count=retry_count + 1)

nltk.download('punkt')
# Get the date from the latest stored JSON file
last_stored_date = get_latest_json_date()

# Calculate the next date to start the calling loop
start_date = last_stored_date + datetime.timedelta(days=1) if last_stored_date else datetime.date.today()

# Define the path for the CSV file
segments_csv_path = "Data/Segment_10000.csv"

# Check if the CSV file already exists
if os.path.exists(segments_csv_path):
    # If the CSV file exists, read the segments from it
    df_segments = pd.read_csv(segments_csv_path)

    # # Filter segments based on the start_date
    # df_segments = df_segments[df_segments['date'] >= start_date]

    # Iterate over the filtered segments and call GPT-3.5 Turbo
    for index, row in tqdm(df_segments.iterrows(), total=len(df_segments), desc="Processing Segments"):
        stock = row['stock']
        segment_text = row['segment']
        date = row['date']
        uuid = row['uuid']

        # Check if the UUID is already in progress
        if not is_uuid_in_progress(uuid):
            call_gpt3_and_store_response(stock, segment_text, date, uuid_in=uuid)
        else:
            print(f"Skipping {uuid} as it is already in progress.")

else:
    # If the CSV file doesn't exist, create it
    segments_data = []

    for index, row in tqdm(df.iterrows(), total=len(df), desc="Storing Segments"):
        stock = row['stock']
        text = row['text']
        date = row['date']

        # Check if the entry's date is after the start date
        entry_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        if entry_date >= start_date:
            # Tokenize the text using NLTK
            tokens = nltk.word_tokenize(text)

            # Segment the tokens into segments of 10,000 tokens or less
            segment_size = 7000
            segments = [tokens[i:i + segment_size] for i in range(0, len(tokens), segment_size)]

            # Store each segment in the list
            for segment in segments:
                segment_text = ' '.join(segment)
                segments_data.append({'stock': stock, 'date': date, 'segment': segment_text, 'uuid': str(uuid.uuid4())})

    # Create a DataFrame from the segments_data list
    df_segments = pd.DataFrame(segments_data)

    # Save the DataFrame to the CSV file
    df_segments.to_csv(segments_csv_path, index=False)

