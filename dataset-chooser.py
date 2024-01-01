import json
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Function to read and shuffle JSONL files
def read_and_shuffle_jsonl(file_path):
    """
    Reads a JSONL file, extracts relevant data, and shuffles it.
    :param file_path: Path to the JSONL file.
    :return: Shuffled DataFrame with extracted data.
    """
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                json_data = json.loads(line)
                for message in json_data['messages']:
                    if message['role'] == 'assistant':
                        data.append({'category': message['content'], 'data': json_data})
    except json.JSONDecodeError as e:
        print(f"Error reading file {file_path}: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return pd.DataFrame(data).sample(frac=1)

# Function to load and shuffle data from a directory
def load_and_shuffle_data(directory):
    """
    Loads and shuffles data from JSONL files in a given directory.
    :param directory: Directory containing JSONL files.
    :return: DataFrame with all data combined and shuffled.
    """
    dataframes = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(read_and_shuffle_jsonl, os.path.join(directory, file))
                   for file in os.listdir(directory) if file.endswith('.jsonl')]
        for future in futures:
            result = future.result()
            if not result.empty:
                dataframes.append(result)
    return pd.concat(dataframes, ignore_index=True)

# Main script execution
if __name__ == "__main__":
    # Replace with the path to your JSONL files directory
    jsonl_files_directory = config.get('Paths', 'jsonl_directory')
    all_data_df = load_and_shuffle_data(jsonl_files_directory)

    # Define your category weights here
    category_weights = json.loads(config.get('Weights', 'category_weights'))

    total_examples = int(config.get('Settings', 'total_examples'))
    selected_data = []

    for category, weight in category_weights.items():
        num_samples = int(total_examples * weight)
        category_data = all_data_df[all_data_df['category'] == category]
        sampled_data = category_data.sample(n=num_samples, replace=True)
        selected_data.append(sampled_data)

    final_dataset = pd.concat(selected_data).sample(frac=1).reset_index(drop=True)

    # Saving the final dataset to a JSONL file
    output_file = config.get('Paths', 'output_file')
    with open(output_file, 'w') as file:
        for _, row in final_dataset.iterrows():
            json.dump(row['data'], file)
            file.write('\n')

    print(f"Dataset created with {len(final_dataset)} examples and saved to {output_file}")
