"""
Instructions creator based on polqa dataset

Removed test subset in Pull Request #15
"""

import json
import os
import random

import pandas as pd

from utils.functions import download_file

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
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")

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


def create_instruction(instruction: str, file_path: str, json_path: str) -> None:
    """
    Create instructions in JSON format from a CSV file and save them in a JSON file.

    :param instruction: The instruction text to be included in the JSON output file..
    :param file_path: The path to the downloaded CSV file.
    :param json_path: The path to the output JSON file.
    """

    instructions = []

    # Read data columnts from the csv file
    data = pd.read_csv(file_path, usecols=['question', 'passage_text', 'relevant'])

    # Iterate through rows and pick defined ones
    for index, row in data.iterrows():
        source = row['question']
        target = row['passage_text']
        if row['relevant']:
            instructions.append({
                    "instruct": instruction,
                    "input": source,
                    "output": target,
                    "source_name": source_name,
                    "source_url": source_url,
                    "source_description": source_description,
                    "script_name": script_name
            })
        else:
            continue

    # Randomly change the order of the elements
    random.shuffle(instructions)

    # Write prepared instructions to the output file
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    files = ['train', 'valid']
    for file in files:
        file_path, json_path = downloader(file)
        create_instruction("Odpowiedz na pytanie.", file_path, json_path)
