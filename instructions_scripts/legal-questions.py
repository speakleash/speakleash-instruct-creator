"""
Instructions creator based on legal-questions

DISCLAIMER: the dataset is based on the test subset, so it was removed from instructions merging in the PR#15
"""
import json
import os
import random

import pandas as pd

try:
    from utils.functions import download_file, get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

source_name = os.path.basename(__file__).replace(".py", "") + " piotr-rybak-legal-questions"
source_url = "https://huggingface.co/datasets/piotr-rybak/legal-questions/"
source_description = "Pary pytanie-odpowiedź z zakresu prawa. Dataset składa się z pytań oraz ręcznie anotowanych fragmentów z artykułów prawnych zawierających potencjalne odpowiedzi (oznaczone True/False). "

script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_path_1 = download_file(
        "https://huggingface.co/datasets/piotr-rybak/legal-questions/resolve/main/data/test.csv?download=true",
        data_dir,
        "legal-questions.csv"
)
json_path_1 = os.path.join(output_dir, "legal-questions.json")


def create_instruction(instruction, file_path, json_path):
    instructions = []
    data = pd.read_csv(file_path, usecols=['question', 'passage_text', 'relevant'])

    for index, row in data.iterrows():
        source = row['question']
        target = row['passage_text']
        if row['relevant']:
            instructions.append({"instruct": instruction, "input": source, "output": target, "source_name": source_name,
                                 "source_url": source_url, "source_description": source_description,
                                 "script_name": script_name})
        else:
            continue

    random.shuffle(instructions)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


create_instruction("Odpowiedz na pytanie.", file_path_1, json_path_1)
