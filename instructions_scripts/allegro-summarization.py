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

source_name = "allegro-summarization-allegro-articles"
source_url = "https://huggingface.co/datasets/allegro/summarization-allegro-articles/"
source_description = "Instrukcje powstały na podstawie zestawu danych allegro-summarization-allegro-articles. Dataset zawiera artykuły z serwisu Allegro wraz z ich podsumowaniami. Autor zestawu danych to Allegro ML Research"
script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

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
        instructions.append({"instruct": instruction, "input" : source, "output" : target, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})

    random.shuffle(instructions)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)

create_instruction("Stwórz tytuł dla podanego artykułu.",file_path_1, json_path_1)
create_instruction("Stwórz wstęp dla podanego artykułu.", file_path_2, json_path_2)
create_instruction("Stwórz tytuł dla podanego wstępu.", file_path_3, json_path_3)