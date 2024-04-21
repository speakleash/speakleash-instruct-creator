from datasets import load_dataset
import os
import random
import json
import sys


try:
    from utils.functions import download_file, get_dir_path, create_directory
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None
    

script_name = os.path.basename(__file__)
source_name = script_name.replace(".py", "")
source_url = "https://huggingface.co/datasets/psc"
source_description = "Instrukcje powstały dzięki zestawowi danych: The Polish Summaries Corpus"


base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") if not None else os.path.join(base_dir, "data")
output_dir = get_dir_path("output") if not None else os.path.join(base_dir, "output")

# Create directory instructions file
create_directory(output_dir)


instructions = []
dataset = load_dataset("sepidmnorozy/Polish_sentiment")
dataset_df = dataset["train"].to_pandas()


items = [
    {
        "instruct": "Czy podany tekst jest pozytywny czy negatywny?",
        "negative": ["negatywny", "Podany tekst jest negatywny."],
        "positive": ["pozytywny", "Podany tekst jest pozytywny."],
    },
    {
        "instruct": "Określ, czy następujący tekst ma konotacje pozytywne czy negatywne?",
        "negative": ["negatywne", "Podany tekst ma konotacje negatywne."],
        "positive": ["pozytywne", "Podany tekst ma konotacje pozytywne."],
    },
    {
        "instruct": "Czy następujący tekst ma pozytywne czy negatywne znaczenie?",
        "negative": ["negatywne", "Podany tekst ma znaczenie negatywne."],
        "positive": ["pozytywne", "Podany tekst ma znaczenie pozytywne."],
    },
    {
        "instruct": "Jakie są konotacje podanego tekstu - pozytywne czy negatywne?",
        "negative": ["negatywne", "Podany tekst ma konotacje negatywne."],
        "positive": ["pozytywne", "Podany tekst ma konotacje pozytywne."],
    },
    {
        "instruct": "Jak oceniasz ton podanego tekstu - czy jest pozytywny czy negatywny?",
        "negative": ["negatywny", "Podany tekst ma ton negatywny."],
        "positive": ["pozytywny", "Podany tekst ma ton pozytywny."],
    },
    {
        "instruct": "Czy podany tekst wyraża emocje pozytywne czy negatywne?",
        "negative": ["negatywne", "Podany tekst wyraża emocje negatywne."],
        "positive": ["pozytywne", "Podany tekst wyraża emocje pozytywne."],
    },
]

for index, row in dataset_df.iterrows():
    text = str(row["text"]).strip()
    label = row["label"]

    if text.strip() == "":
        continue


    item = random.choice(items)
    instruct = item["instruct"]
    output = ""

    if label == 0:
        output = random.choice(item["negative"])

    if label == 1:
        output = random.choice(item["positive"])
    
    instructions.append(
        {
            "instruct": instruct,
            "input": text.strip(),
            "output": output,
            "source_name": source_name,
            "source_url": source_url,
            "source_description": source_description,
            "script_name": script_name,
        }
    )

random.shuffle(instructions)
with open(os.path.join(output_dir, script_name.replace(".py",".json")), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))