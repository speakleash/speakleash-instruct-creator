import os
import pandas as pd
import json
import random
from utils.functions import download_file, get_dir_path

source_name = os.path.basename(__file__).replace(".py", "")
source_url = "https://huggingface.co/datasets/allegro/summarization-polish-summaries-corpus"
source_description = "Instrukcje powstały na bazie zbioru The Polish Summaries Corpus zawierającego ręczne " \
                     "streszczenia artykułów prasowych."
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


def create_instruction(instruct_list: list, file_path: str, json_path: str, remove_duplicates_arg: bool = True) -> None:

    instructions = []
    data = pd.read_csv(file_path, usecols=['source', 'target'])

    if remove_duplicates_arg:
        data = remove_duplicates(data)

    for index, row in data.iterrows():
        source = row['source']
        target = row['target']
        instructions.append({"instruct": random.choice(instruct_list), "input": source, "output": target, "source_name": source_name, "source_url": source_url, "source_description": source_description, "script_name": script_name})

    random.shuffle(instructions)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


def remove_duplicates(data):
    data = data.sample(frac=1).reset_index(drop=True)
    data = data.drop_duplicates(subset='source', keep='first')
    return data


INSTRUCT_LIST = [
            "Napisz skróconą wersję podanego tekstu.",
            "Przygotuj skróconą wersję podanego tekstu.",
            "Napisz skróconą wersję poniższego tekstu.",
            "Przygotuj skróconą wersję poniższego tekstu.",
            "Napisz skróconą wersję tego tekstu.",
            "Przygotuj skróconą wersję tego tekstu.",
            "Przygotuj streszczenie dla tego tekstu.",
            "Napisz streszczenie dla tego tekstu.",
            "Przygotuj streszczenie dla podanego tekstu.",
            "Napisz streszczenie dla podanego tekstu.",
            "Dokonaj streszczenia z podanego materiału.",
            "Przygotuj streszczenia z podanego materiału.",
            "Dokonaj streszczenia z tego materiału.",
            "Napisz streszczenia z tego materiału.",
            "Dokonaj streszczenia z tego tekstu.",
            "Streść poniższy tekst.",
            "Streść ten tekst.",
            "Zrób streszczenie.",
            "Napisz streszczenie.",
            "Przygotuj streszczenie.",
            "Przygotuj skrót informacji z podanego tekstu.",
            "Napisz skrót informacji z podanego tekstu.",
            "Streść podany tekst."
    ]

create_instruction(INSTRUCT_LIST, file_path, json_path)
