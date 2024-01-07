import os 
from speakleash import Speakleash
import random
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")
replicate_to = os.path.join(base_dir, "datasets")

source_name = "news_9_general_corpus"
source_url = "https://speakleash.org/"
source_description = "Instrukcje powstały na podstawie zestawu danych news_9_general_corpus. Dataset zawiera artykuły z polskiego Internetu."
script_name = os.path.basename(__file__)


sl = Speakleash(replicate_to)
counter = 0
data = sl.get("news_9_general_corpus").ext_data

def best_category(data, threshold=90):
    max_category = max(data, key=data.get)
    if data[max_category] > threshold:
        return max_category, data[max_category]
    else:
        return None, None


prompts = ["Przypisz kategorie do przedstawionego tekstu.", "Skategoryzuj podany tekst", "Zaklasyfikuj treść podanego tekstu.", "Określ kategorię dla podanego tekstu.", "Zidentyfikuj i przypisz odpowiednią kategorię dla podanego tekstu.", "Przydziel podany tekst do odpowiedniej kategorii."]

counter = 0
instructions = []

for item in data:
    txt, meta = item
    quality = meta.get("quality", "")
    categories = meta.get("category", {})
    category, pp = best_category(categories, 95)

    if quality.upper() == "HIGH" and category is not None: 
        counter += 1
        random.shuffle(prompts)
        outputs = []
        outputs.append("Tekst należy do kategorii: " + category)
        outputs.append("Kategoria tekstu to: " + category)
        outputs.append("Wykryta kategoria: " + category)
        outputs.append("Kategoria: " + category)
        outputs.append("Kategoria tekstu: " + category)

        random.shuffle(outputs)
        instructions.append({"instruct": prompts[0], "input" : txt, "output" : "Tekst należy do kategorii: " + outputs[0], "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})


random.shuffle(instructions)
with open(os.path.join(output_dir, "speakleash-categorization.json"), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))






