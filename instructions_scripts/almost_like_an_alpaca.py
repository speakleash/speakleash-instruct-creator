import os
import json
import random
import requests

def download_file(url: str, download_dir: str, file_name: str) -> str:
    """
    Download file with the given url address.

    :param url: Provided url address to download the file
    :param download_dir: The destination folder for the downloaded file.
    :param file_name: The name of the downloaded file.
    :return: The path to the downloaded file.
    """

    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, file_name)

    if not os.path.exists(file_path):
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            return None
        with open(file_path, 'wb') as file:
            file.write(r.content)

    return file_path



source_name = "almost_like_an_alpaca"
source_url = "http://instruct.speakleash.space/"
source_description = "Instrukcje powstały na podstawie pytań/zadań z zestawu danych Alpaca i odpowiedzi z polskiego Internetu."
script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")

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
        instructions.append(
            {"instruct": instruction, "input": "", "output": output, "source_name": source_name,
             "source_url": source_url, "source_description": source_description,
             "script_name": script_name})

with open(os.path.join(output_dir,script_name.replace(".py", ".json")), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)

