import os 
from speakleash import Speakleash
import random
import json
import sys
import spacy

try:
    from utils.functions import get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

nlp = spacy.load("pl_core_news_md")

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")
replicate_to = os.path.join(base_dir, "datasets")

source_name = "news_8_general_corpus"
source_url = "https://speakleash.org/"
source_description = "Instrukcje powstały na podstawie zestawu danych news_8_general_corpus. Dataset zawiera artykuły z polskiego Internetu."
script_name = os.path.basename(__file__)


sl = Speakleash(replicate_to)
counter = 0
data = sl.get("news_8_general_corpus").ext_data

counter = 0
instructions = []

for item in data:
    txt, meta = item
    quality = meta.get("quality", "")

    if quality.upper() == "HIGH":
        doc = nlp(txt)
        counter += 1
    
        for sent in doc.sents:
            if  sent.text.strip().endswith("?") and sent.text[0].isupper():  
                verb = ""
                noun = ""
                adj = ''
                words = []
                for token in sent:
                    if token.pos_ == "VERB" and verb == "":
                        verb = token.lemma_.strip().lower()
                        words.append(token.lemma_.strip().lower())
                    if token.pos_ == "NOUN" and noun == "":
                        noun = token.lemma_.strip().lower()
                        words.append(token.lemma_.strip().lower())
                    if token.pos_ == "ADJ" and adj == "":
                        adj = token.lemma_.strip().lower()
                        words.append(token.lemma_.strip().lower())
                    
                if verb != "" and noun != "" and adj != "":
                    random.shuffle(words)
                    instruct = "Stwórz przykładowe pytania składające się ze słów: " + ", ".join(words) + "."
                    output = "Przykładowe pytania: " + sent.text
                    instructions.append({"instruct": instruct, "input" : "", "output" : output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})
                    print("Instructions: " + str(len(instructions)), counter)

    if len(instructions) > 100000:
        break
        

random.shuffle(instructions)
with open(os.path.join(output_dir, "speakleash-create-question.json"), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)), counter)






