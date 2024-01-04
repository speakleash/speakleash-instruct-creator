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

file_path_1 = download_file("https://huggingface.co/datasets/allegro/summarization-allegro-articles/resolve/main/body_lead_to_title/train.csv?download=true", data_dir, "allegro-summarization-allegro-articles-body-lead-to-title.csv")
json_path_1 = os.path.join(output_dir, "allegro-summarization-allegro-articles-body-lead-to-title.json")

file_path_2 = download_file("https://huggingface.co/datasets/allegro/summarization-allegro-articles/resolve/main/body_to_lead/train.csv?download=true", data_dir, "allegro-summarization-allegro-articles-body-to-lead.csv")
json_path_2 = os.path.join(output_dir, "allegro-summarization-allegro-articles-body-to-lead.json")

file_path_3 = download_file("https://huggingface.co/datasets/allegro/summarization-allegro-articles/resolve/main/lead_to_title/train.csv?download=true", data_dir, "allegro-summarization-allegro-articles-lead-to-title.csv")
json_path_3 = os.path.join(output_dir, "allegro-summarization-allegro-articles-lead-to-title.json")



def create_instruction(instruction, file_path, json_path):

    instructions = []
    data = pd.read_csv(file_path, usecols=['source', 'target'])

    for index, row in data.iterrows():
        source = row['source']
        target = row['target']
        instructions.append({"instruct": instruction, "input" : source, "output" : target})

    random.shuffle(instructions)

    with open(json_path, "w") as f: 
        json.dump(instructions, f, indent=4, ensure_ascii=False)

create_instruction("Stwórz tytuł dla podanego artykułu.",file_path_1, json_path_1)
create_instruction("Stwórz wstęp dla podanego artykułu.", file_path_2, json_path_2)
create_instruction("Stwórz tytuł dla podanego wstępu.", file_path_3, json_path_3)