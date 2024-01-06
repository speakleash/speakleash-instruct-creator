import os
import pandas as pd
import json
import random
from utils.functions import download_file


base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_path_1 = download_file(
    "https://huggingface.co/datasets/allegro/klej-dyk/resolve/main/test.csv?download=true",
    data_dir,
    "allegro-klej-dyk-test.csv"
)
json_path_1 = os.path.join(output_dir, "allegro-klej-dyk_test.json")

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
            instructions.append({"instruct": instruction, "input": source, "output": target})
        else:
            continue

    random.shuffle(instructions)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


create_instruction("Odpowiedz na pytanie.", file_path_1, json_path_1)
create_instruction("Odpowiedz na pytanie.", file_path_2, json_path_2)
