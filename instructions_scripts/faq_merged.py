"""Instructions creator based on human_annotators_common_errors"""
import json
import os
import re

import pandas as pd


try:
    from utils.functions import download_file, get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

# Mandatory dataset data for json objects
SOURCE_NAME = f"web_{os.path.basename(__file__).replace('.py', '')}"
SOURCE_DESCRIPTION = 'Zbiór instrukcji wysokiej jakości stworzonych ręcznie przez Spatium (Grzegorz)'

FILE = 'faq_merged.xlsx'
DATA_DIR = 'data'
OUTPUT_DIR = 'output'
SCRIPT_NAME = os.path.basename(__file__)


def text_cleaner(text: str) -> str:
    """
    Clean string with regex formula.

    :param text: Provided text for cleaning.
    :return: Cleaned text.
    """
    text = re.sub(r"\[\d+\]\.$", '', text)
    return text.replace('Ŝ', 'ż').replace('„', '"').replace('”', '"').replace(',,', '"').replace("''", '"').replace(' • ', ' * ').replace('×', '*').replace('·', '*').replace('–', '-').replace('\r', '')


def create_dirs() -> None or tuple:
    """
    Create storage directories for both downloaded dataset and created JSON instructions file.
    """
    # Get the path to the currently executing python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define directories name for downloaded and output files. File is being downloaded manually, so put it in the
    # DATA_DIR file or just try to create it via this function
    data_dir = get_dir_path(DATA_DIR) or os.path.join(base_dir, DATA_DIR)
    output_dir = get_dir_path(OUTPUT_DIR) or os.path.join(base_dir, OUTPUT_DIR)

    # Create directory for downloading data from server / link
    os.makedirs(data_dir, exist_ok=True)

    # Create directory (if it does not exist yet) for created instructions json files
    os.makedirs(output_dir, exist_ok=True)
    return data_dir, output_dir


def paths_data(data_dir: str, output_dir: str) -> tuple:
    """
    Download a CSV file and return its file path and corresponding JSON file path.

    :param file: The name of the file to download
    :return: A tuple containing path do downloaded file and output JSON file.
    """

    file_path = os.path.join(data_dir, FILE)
    json_path = os.path.join(output_dir, FILE.replace('.xlsx', '.json'))
    return file_path, json_path


def create_instruction(file_path: str, json_path: str) -> None:
    """
    Create instructions in JSON format from a JSON file and save them in a JSON file.

    :param file_path: The path to the downloaded CSV file.
    :param json_path: The path to the output JSON file.
    """

    instructions = []
    duplicates_correct = []

    # xlsx file has only 2 colums, so adding paramter usecols=[0, 1] is not needed)
    data = pd.read_excel(file_path)

    for index, row in data.iterrows():
        question = text_cleaner(row['Q'])
        answer = text_cleaner(row['A'])
        pair = (question, answer)
        if pair not in duplicates_correct:
            instructions.append({
                    "instruct": question,
                    "input": "",
                    "output": answer,
                    "source_name": SOURCE_NAME,
                    "source_description": SOURCE_DESCRIPTION,
                    "script_name": SCRIPT_NAME
            })

    print(f'---- Instructions num = {len(instructions)}')
    with open(json_path, "w", encoding='utf-8') as save_file:
        json.dump(instructions, save_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    data_dir, output_dir = create_dirs()
    file_path, json_path = paths_data(data_dir, output_dir)
    create_instruction(file_path, json_path)
