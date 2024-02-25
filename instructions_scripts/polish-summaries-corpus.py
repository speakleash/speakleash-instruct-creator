import os
import pandas as pd
import json
import random
from utils.functions import download_file, get_dir_path

source_name = os.path.basename(__file__).replace(".py", "")
source_url = "https://huggingface.co/datasets/allegro/summarization-polish-summaries-corpus"
source_description = "TODO"
script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") if not None else os.path.join(base_dir, "data")
output_dir = get_dir_path("output") if not None else os.path.join(base_dir, "output")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_path = download_file("https://huggingface.co/datasets/allegro/summarization-polish-summaries-corpus/resolve/main/whole/train.csv?download=true", data_dir, "summarization-polish-summaries-corpus.csv")
json_path = os.path.join(output_dir, "summarization-polish-summaries-corpus.json")


def create_instruction(instruction, file_path, json_path):

    instructions = []
    data = pd.read_csv(file_path, usecols=['source', 'target'])

    for index, row in data.iterrows():
        source = row['source']
        target = row['target']
        instructions.append({"instruct": instruction, "input" : source, "output" : target, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})

    random.shuffle(instructions)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)

create_instruction("Streść podany tekst.",file_path, json_path)
