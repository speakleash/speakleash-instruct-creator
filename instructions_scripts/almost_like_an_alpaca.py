"""Script generates instructions files"""
import os
import json
import random
import config

try:
    from utils.functions import download_file, get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None


source_name = "almost_like_an_alpaca"
source_url = "http://instruct.speakleash.space/"
source_description = "Instrukcje powstały na podstawie pytań/zadań z zestawu danych Alpaca i odpowiedzi z polskiego Internetu."
script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

all = []
instructions = []

for i in range(0, 100):
    file_name = f"almost_like_an_alpaca_{i}.json"
    file_path = download_file(f"{source_url}/{file_name}", data_dir, file_name)
    if file_path:
        print(f"Downloaded {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            all = all + data

    else:
        break

print(f"Downloaded {len(all)} instructions")
random.shuffle(all)

for item in all:
    output = item.get("output", "")
    instruction = item.get("instruction", "")
    if instruction and output:
        instructions.append({
                "instruct": instruction,
                "input": "",
                "output": output,
                "source_name": source_name,
                "source_url": source_url,
                "source_description": source_description,
                "script_name": script_name
        })

random.shuffle(instructions)

with open(os.path.join(output_dir,script_name.replace(".py", ".json")), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
