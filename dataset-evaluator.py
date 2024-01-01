import json
import pandas as pd
from rich.console import Console
from rich.table import Table
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Function to read JSONL file and convert to DataFrame
def read_jsonl_to_dataframe(file_path):
    """
    Reads a JSONL file and converts it to a DataFrame.
    :param file_path: Path to the JSONL file.
    :return: DataFrame with assistant responses.
    """
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                json_data = json.loads(line)
                if 'messages' in json_data:
                    for message in json_data['messages']:
                        if message['role'] == 'assistant':
                            data.append(message['content'])
    except json.JSONDecodeError as e:
        print(f"Error reading file {file_path}: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return pd.DataFrame(data, columns=['assistant_response'])

# Function to generate and return report DataFrame
def generate_report(file_path):
    """
    Generates a report from a DataFrame.
    :param file_path: Path to the JSONL file.
    :return: DataFrame with report data.
    """
    df = read_jsonl_to_dataframe(file_path)
    report = df['assistant_response'].value_counts().reset_index()
    report.columns = ['Assistant Response', 'Count']
    report['Percentage'] = (report['Count'] / report['Count'].sum()) * 100
    return report

# Function to display report using rich library
def display_report_with_rich(report_df):
    """
    Displays a report DataFrame in a formatted table using the rich library.
    :param report_df: DataFrame containing report data.
    """
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Assistant Response", style="dim", width=100)
    table.add_column("Count", justify="right")
    table.add_column("Percentage", justify="right")

    for _, row in report_df.iterrows():
        table.add_row(row['Assistant Response'], str(row['Count']), f"{row['Percentage']:.2f}%")

    console.print(table)

# Main script execution
if __name__ == "__main__":
    # Replace with the path to your final JSONL file
    final_jsonl_file = config.get('Paths', 'output_file')

    # Generate the report
    report_df = generate_report(final_jsonl_file)

    # Display the report in the console using Rich library
    display_report_with_rich(report_df)
