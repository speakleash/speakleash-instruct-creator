"""
Instructions creator based on polqa dataset

Removed test subset in Pull Request #15
"""

import json
import os
import random

import pandas as pd
import ast

try:
    from utils.functions import download_file, get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

# Mandatory dataset information fields for json objects
source_name = f"ipipan-{os.path.basename(__file__).replace('.py', '')}"
source_url = 'https://huggingface.co/datasets/ipipan/polqa'
source_description = 'Pary pytanie-odpowiedź powstały na bazie zestawu danych PolQA. Dataset składa się z pytań oraz ' \
                     'ręcznie anotowanych fragmentów z odpowiedziami. Autor zestawu danych to Instytu Podstaw ' \
                     'Informatyki Polskiej Akademii Nauk.'
script_name = os.path.basename(__file__)

# Get the path to the currently executing python script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define directories name for downloaded and output files
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

# Create directory for downloading data from server / link
os.makedirs(data_dir, exist_ok=True)

# Create directory (if does not exists) for created instructions json files
os.makedirs(output_dir, exist_ok=True)


def downloader(file: str) -> tuple:
    """
    Download a CSV file and return its file path and corresponding JSON file path.

    :param file: The name of the file to download
    :return: A tuple containing path do downloaded file and output JSON file.
    """
    file_path = download_file(
            f"https://huggingface.co/datasets/ipipan/polqa/resolve/main/data/{file}.csv?download=true",
            data_dir,
            f"ipipan_polqa_{file}.csv"
    )
    json_path = os.path.join(output_dir, f"ipipan_polqa_{file}.json")
    return file_path, json_path


def parse_answers(answers: str) -> list:
    """
    Parse a string of answers into a list of answers.

    :param answers: A string containing answers, possibly enclosed in square brackets and separated by commas.
    :return: A list of answers extracted from the input string.
    """
    return ast.literal_eval(answers)


def create_instruction(file_path: str, json_path: str) -> None:
    """
    Create instructions in JSON format from a CSV file and save them in a JSON file.

    :param instruction: The instruction text to be included in the JSON output file..
    :param file_path: The path to the downloaded CSV file.
    :param json_path: The path to the output JSON file.
    """

    instructions = []
    added_pair = []
    added_pairs_counter = 0
    new_counter = 0

    data = pd.read_csv(file_path, usecols=['question', 'passage_text', 'relevant', 'answers'], converters={'answers': parse_answers})
    data['first_answer'] = data['answers'].apply(lambda x: x[0] if x else None)
    print(data.head())

    # Iterate through rows and pick defined ones
    for index, row in data.iterrows():
        question = row['question']
        answer = row['first_answer']
        if row['relevant']:
            new_counter += 1
        pair = (question, answer)
        if row['relevant'] and pair not in added_pair:
            added_pair.append(pair)
            added_pairs_counter += 1
            instructions.append({
                    'id': added_pairs_counter,
                    "instruct": row['question'],
                    "input": row['passage_text'],
                    "output": row['first_answer'],
                    "source_name": source_name,
                    "source_url": source_url,
                    "source_description": source_description,
                    "script_name": script_name
            })

    # Randomly change the order of the elements
    # random.shuffle(instructions)
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    files = ['train', 'valid']
    for file in files:
        file_path, json_path = downloader(file)
        create_instruction(file_path, json_path)
