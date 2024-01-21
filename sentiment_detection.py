from datasets import load_dataset
import os
import random
import json

script_name = os.path.basename(__file__)
source_name = script_name.replace(".py", "")
source_url = "https://huggingface.co/datasets/Brand24/mms"
source_description = "Instrukcje powstały dzięki zestawowi danych: Massive Multilingual Sentiment Corpora (MMS)"

limit = 1000
instruction_limit = 150000

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")

counter = 0
instructions = []
mms_dataset = load_dataset("Brand24/mms")
mms_dataset_df = mms_dataset["train"].to_pandas()

items = [
    {
        "instruct": "Czy podany tekst jest pozytywny, neutralny czy negatywny?",
        "negative": ["negatywny", "Podany tekst jest negatywny."],
        "neutral": ["neutralny", "Podany tekst jest neutralny."],
        "positive": ["pozytywny", "Podany tekst jest pozytywny."],
    },
    {
        "instruct": "Określ, czy następujący tekst ma konotacje pozytywne, neutralne czy negatywne?",
        "negative": ["negatywne", "Podany tekst ma konotacje negatywne."],
        "neutral": ["neutralne", "Podany tekst ma konotacje neutralne."],
        "positive": ["pozytywne", "Podany tekst ma konotacje pozytywne."],
    },
    {
        "instruct": "Czy następujący tekst ma pozytywne, neutralne czy negatywne znaczenie?",
        "negative": ["negatywne", "Podany tekst ma znaczenie negatywne."],
        "neutral": ["neutralne", "Podany tekst ma znaczenie neutralne."],
        "positive": ["pozytywne", "Podany tekst ma znaczenie pozytywne."],
    },
    {
        "instruct": "Jakie są konotacje podanego tekstu - pozytywne, neutralne czy negatywne?",
        "negative": ["negatywne", "Podany tekst ma konotacje negatywne."],
        "neutral": ["neutralne", "Podany tekst ma konotacje neutralne."],
        "positive": ["pozytywne", "Podany tekst ma konotacje pozytywne."],
    },
    {
        "instruct": "Jak oceniasz ton podanego tekstu - czy jest pozytywny, neutralny czy negatywny?",
        "negative": ["negatywny", "Podany tekst ma ton negatywny."],
        "neutral": ["neutralny", "Podany tekst ma ton neutralny."],
        "positive": ["pozytywny", "Podany tekst ma ton pozytywny."],
    },
    {
        "instruct": "Czy podany tekst wyraża emocje pozytywne, neutralne czy negatywne?",
        "negative": ["negatywne", "Podany tekst wyraża emocje negatywne."],
        "neutral": ["neutralne", "Podany tekst wyraża emocje neutralne."],
        "positive": ["pozytywne", "Podany tekst wyraża emocje pozytywne."],
    },
]


mms_dataset_df = mms_dataset_df[mms_dataset_df["language"] == "pl"]

for index, row in mms_dataset_df.iterrows():
    text = str(row["text"]).strip()
    label = row["label"]
    domain = row["domain"]

    if text.strip() == "":
        continue


    item = random.choice(items)
    instruct = item["instruct"]
    output = ""

    if label == 0:
        output = random.choice(item["negative"])

    if label == 1:
        output = random.choice(item["neutral"])

    if label == 2:
        output = random.choice(item["positive"])
    
    counter += 1
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



