import json
import os
import random

import spacy
from speakleash import Speakleash

try:
    from utils.functions import get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

nlp = spacy.load("pl_core_news_md")

script_name = os.path.basename(__file__)
source_name = script_name.replace(".py", "")
source_url = "https://speakleash.org/"
source_description = "Instrukcje powstały dzięki ekstrakcji słów z polskiej wersji Wikipedii i przetworzenia ich za pomocą pakietu Spacy."

limit = 120000

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")
replicate_to = os.path.join(base_dir, "datasets")

sl = Speakleash(replicate_to)
counter = 0
wiki = sl.get("plwiki").data
instructions = []
words = {}


def random_instruct():
    instructs = [
            "Jaką cześcią mowy jest podane słowo?",
            "Czy możesz określić, jaką częścią mowy jest to słowo?",
            "Czy wiesz, jaką częścią mowy jest dane słowo?",
            "Czy możesz zidentyfikować, jaką częścią mowy jest to słowo?",
            "Czy możesz określić, do której części mowy należy to słowo?",
            "Czy jesteś w stanie zidentyfikować, jaką częścią mowy jest to słowo?",
            "Czy potrafisz określić, jaką częścią mowy jest to słowo?",
            "Czy jesteś w stanie określić, do której części mowy należy to słowo?",
            "Czy potrafisz zidentyfikować, do której części mowy należy to słowo?",
            "Czy jesteś w stanie określić, jaką częścią mowy jest dane słowo?",
            "Czy potrafisz określić, do której części mowy należy dane słowo?",
            "Czy jesteś w stanie zidentyfikować, do której części mowy należy to słowo?",
            "Czy potrafisz zidentyfikować, jaką częścią mowy jest dane słowo?",
            "Czy jesteś w stanie określić, jaką częścią mowy jest to słowo?",
            "Czy potrafisz określić, jaką częścią mowy jest to słowo?",
            "Czy jesteś w stanie zidentyfikować, jaką częścią mowy jest dane słowo?"
    ]

    return random.choice(instructs)


verbs = {}
nouns = {}
adjs = {}

for txt in wiki:
    doc = nlp(txt)
    print("Instructions: " + str(len(instructions)))
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_digit and token.is_oov == False:
            word = token.text.strip()
            lemma = token.lemma_.strip()

            if token.pos_ == "VERB":
                if lemma not in verbs:
                    verbs[lemma] = 1
                    instructions.append({"instruct": random_instruct(), "input": word, "output": "czasownik",
                                         "source_name": source_name, "source_url": source_url,
                                         "source_description": source_description, "script_name": script_name})
                else:
                    verbs[lemma] += 1

            if token.pos_ == "NOUN":
                if lemma not in nouns:
                    nouns[lemma] = 1
                    instructions.append({"instruct": random_instruct(), "input": word, "output": "rzeczownik",
                                         "source_name": source_name, "source_url": source_url,
                                         "source_description": source_description, "script_name": script_name})
                else:
                    nouns[lemma] += 1

            if token.pos_ == "ADJ":
                if lemma not in adjs:
                    adjs[lemma] = 1
                    instructions.append({"instruct": random_instruct(), "input": word, "output": "przymiotnik",
                                         "source_name": source_name, "source_url": source_url,
                                         "source_description": source_description, "script_name": script_name})
                else:
                    adjs[lemma] += 1

    if len(instructions) > limit:
        break

random.shuffle(instructions)
with open(os.path.join(output_dir, script_name.replace(".py", ".json")), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))
