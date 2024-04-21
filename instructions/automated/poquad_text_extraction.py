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

source_name = os.path.basename(__file__).replace(".py", "") + " clarin-pl-poquad"
source_url = "https://huggingface.co/datasets/clarin-pl/poquad/resolve/main/poquad"
source_description = "Instrukcje zawierające: tytuł artykułu z Wikipedii, treść artykułu, oraz pytanie do artykułu i " \
                     "wyodrębnioną odpowiedź."
script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_path_1 = download_file(
    "https://huggingface.co/datasets/clarin-pl/poquad/resolve/main/poquad-train.json?download=true",
    data_dir,
    "poquad-train.json"
)
json_path_1 = os.path.join(output_dir, "poquad-train.json")

file_path_2 = download_file(
    "https://huggingface.co/datasets/clarin-pl/poquad/resolve/main/poquad-dev.json?download=true",
    data_dir,
    "poquad-dev.json"
)
json_path_2 = os.path.join(output_dir, "poquad-dev.json")


def create_instruction(instruction, file_path, json_path):
    instructions = []
    data_temp = pd.read_json(file_path, orient="index", typ="series")
    data = pd.DataFrame(data_temp["data"])
    instructions_sets = []
    for index, row in data.iterrows():
        if len(row["paragraphs"][0]["qas"]) != 0 and list(
            row["paragraphs"][0]["qas"][0].keys()
        )[0] == "question":
            source = row["paragraphs"][0]["qas"][0]["question"]
            if list(
                row["paragraphs"][0]["qas"][0].keys()
            )[1] == "plausible_answers":
                target = row["paragraphs"][0]["qas"][0]["plausible_answers"][0]["generative_answer"]
            elif list(
                row["paragraphs"][0]["qas"][0].keys()
            )[1] == "answers":
                target = row["paragraphs"][0]["qas"][0]["answers"][0]["generative_answer"]
            else:
                continue
            set = (instruction, source + ' ' + row["paragraphs"][0]["context"], target)
            if set not in instructions_sets:
                instructions_sets.append(set)
                instructions.append(
                    {
                        "instruct": instruction,
                        "input": source + ' ' + row["paragraphs"][0]["context"],
                        "output": target,
                        "source_name": source_name,
                        "source_url": source_url,
                        "source_description": source_description,
                        "script_name": script_name,
                     }
                )
    random.shuffle(instructions)

    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


create_instruction("Znajdź w podanym tekście odpowiedź na pytanie.", file_path_1, json_path_1)
create_instruction("Znajdź w podanym tekście odpowiedź na pytanie.", file_path_2, json_path_2)
