"""Instructions creator based on human_annotators_common_errors"""
import json
import os
import random

import jsonlines

from utils.functions import download_file

# Mandatory dataset data for json objects
SOURCE_NAME = f"{os.path.basename(__file__).replace('.py', '')}"
SOURCE_URL = 'https://github.com/Ermlab/polish-gec-datasets/blob/main/'
SOURCE_DESCRIPTION = 'Zbiór danych zawierający zbiory testowe do korekcji błędów ortograficznych. Dataset składa się ' \
                     'ze zdań prawidłowych, nieprawidłowych oraz wskazań błędów ortograficznych. Autore zestawu ' \
                     'danych to Ermlab'

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


def _convert_github_url(git_url: str) -> str:
    """
    Converts provided github url to downloadable url for raw format files. If is not from github or already
    represents raw file, it returns unchanged link.

    :param url: Link to the githhub repository file
    :return: Link to the githhub repository in raw format, if conditions are met.
    """
    if 'github' in git_url and '/tree/' in git_url and not 'raw' in git_url:
        return git_url.replace('/tree/', '/raw/', 1)
    return git_url


def downloader(download_url: str, file: str) -> tuple:
    """
    Download a CSV file and return its file path and corresponding JSON file path.

    :param file: The name of the file to download
    :return: A tuple containing path do downloaded file and output JSON file.
    """
    download_url = _convert_github_url(download_url)
    file_path = download_file(f"{download_url}/{file}", data_dir, file)
    json_path = os.path.join(output_dir, f"{file}")
    return file_path, json_path


def create_instruction(instruction: str, file_path: str, json_path: str) -> None:
    """
    Create instructions in JSON format from a JSON file and save them in a JSON file.

    :param instruction: The instruction text to be included in the JSON output file.
    :param file_path: The path to the downloaded CSV file.
    :param json_path: The path to the output JSON file.
    """

    instructions = []

    with jsonlines.open(file_path, 'r') as reader_file:
        for element in reader_file:
            instructions.append({
                    "instruct": instruction,
                    "input": element['incorrect'],
                    "output": element['correct'],
                    "source_name": SOURCE_NAME,
                    "source_url": SOURCE_URL,
                    "source_description": SOURCE_DESCRIPTION,
                    "script_name": script_name
            })

    # Randomly change the order of the elements
    random.shuffle(instructions)

    # Write prepared instructions to the output file
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    URL = 'https://github.com/Ermlab/polish-gec-datasets/tree/main'
    FILE = 'human_annotators_common_errors_10K.jsonl'
    file_path, json_path = downloader(URL, FILE)
    create_instruction("Popraw podane zdanie.", file_path, json_path)
