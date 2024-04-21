"""
Instructions creator based on allegro klej-dyk dataset

Removed test subset in Pull Request #15
"""

import os
import pandas as pd
import json
import random

try:
    from utils.functions import download_file, get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

source_name = os.path.basename(__file__).replace(".py", "") + " allegro/klej-dyk"
source_url = "https://huggingface.co/datasets/allegro/klej-dyk"
source_description = "Pary pytanie - odpowiedź pochodzące z sekcji Czy wiesz... z polskiej Wikipedii. " \
                     "odpowiedzi są anotowane jako trafne (1) albo nietrafne (0)."

script_name = os.path.basename(__file__)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Removed in Pull Request #15
# file_path_1 = download_file(
#     "https://huggingface.co/datasets/allegro/klej-dyk/resolve/main/test.csv?download=true",
#     data_dir,
#     "allegro-klej-dyk-test.csv"
# )
# json_path_1 = os.path.join(output_dir, "allegro-klej-dyk_test.json")

file_path_2 = download_file(
    "https://huggingface.co/datasets/allegro/klej-dyk/resolve/main/train.csv?download=true",
    data_dir,
    "allegro-klej-dyk-train.csv"
)
json_path_2 = os.path.join(output_dir, "allegro-klej-dyk_train.json")


def create_instruction(instruction, file_path, json_path):

    instructions = []
    data = pd.read_csv(file_path, usecols=['question', 'answer', 'target'])

    for index, row in data.iterrows():
        source = row['question']
        target = row['answer']
        if row['target'] == 1:
            instructions.append({"instruct": instruction, "input": source, "output": target, "source_name": source_name, "source_url": source_url, "source_description": source_description, "script_name": script_name})
        else:
            continue

    random.shuffle(instructions)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


# create_instruction("Odpowiedz na pytanie.", file_path_1, json_path_1) # Removed in Pull Request #15
create_instruction("Odpowiedz na pytanie.", file_path_2, json_path_2)
