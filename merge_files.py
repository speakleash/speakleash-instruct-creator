import json
import os
import random
import subprocess
import sys
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "output")
data_dir = os.path.join(base_dir, "data")
version = "0_0_5"

generate = False

scipts_to_run = []
scipts_to_run.append({"script_name" : "allegro_klej_dyk_questions.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "legal-questions.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_LEGAL_QA"})
scipts_to_run.append({"script_name" : "polish-summaries-corpus.py", "author" : "Ic & MariaF", "category": "NLP_SUMMARIZATION"})
scipts_to_run.append({"script_name" : "polqa_questions.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "poquad_text_extraction.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "speakleash-categorization.py", "author" : "Amarok & Sekon", "category": "NLP_CLASSIFICATION"})
scipts_to_run.append({"script_name" : "speakleash_forums_questions.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "wiki-lemmat-words.py", "author" : "Sekon", "category": "NLP_LEMMATIZATION"})
scipts_to_run.append({"script_name" : "allegro-summarization.py", "author" : "Sekon", "category": "NLP_SUMMARIZATION"})
scipts_to_run.append({"script_name" : "speakleash-create-sentence.py", "author" : "Sekon", "category": "NLP_SENTENCE_CREATION"})
scipts_to_run.append({"script_name" : "create_password.py", "author" : "Sekon", "category": "BUSINESS_TOOLS"})
scipts_to_run.append({"script_name" : "speakleash-simple-math-operations.py", "author" : "ChrisO", "category": "KNOWLEDGE_MATH"})
scipts_to_run.append({"script_name" : "amazon-massive-pl.py", "author" : "pawkis", "category": "NLP_INTENT_DETECTION"})
scipts_to_run.append({"script_name" : "plwiki_random_word_list.py", "author" : "Sekon", "category": "NLP_WORD_LIST"})
scipts_to_run.append({"script_name" : "plwiki_random_word_pos.py", "author" : "Sekon", "category": "NLP_WORD_POS"})
scipts_to_run.append({"script_name" : "quotes.py", "author" : "Sekon", "category": "NLP_QUOTES"})
scipts_to_run.append({"script_name" : "vulgar_words.py", "author" : "Sekon", "category": "NLP_VULGAR_DETECTION"})
scipts_to_run.append({"script_name" : "sentiment_detection.py", "author" : "Sekon", "category": "NLP_SENTIMENT_DETECTION"})

if generate:
    for script in scipts_to_run:
        print("Running: " + script["script_name"])
        result = subprocess.run([sys.executable, script["script_name"]], capture_output=True, text=True)
        

def get_author(script_name):
    for script in scipts_to_run:
        if script["script_name"] == script_name:
            return script["author"]
        
def get_category(script_name):
    for script in scipts_to_run:
        if script["script_name"] == script_name:
            return script["category"]

print("Merging files...")

files = os.listdir(output_dir)
all = []
counter = 1

authors_stats = {}
source_stats = {}
category_stats = {}

for file in files:
    file_path = os.path.join(output_dir, file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    file_counter = 1

    for item in data:

        print("Merging file: " + file.upper().replace(".JSON","") + " (" + str(file_counter) + ")")
        new_item = {}
        new_item['instruct'] = item.get('instruct', 'instruction')
        new_item['input'] = item['input']
        new_item['output'] = item['output']
        category = item.get('category', get_category(item['script_name']))

        print("Category: " + category)

        new_item['category'] = category

        script_name = item.get('script_name', '')
        source_name = item.get('source_name', '')
        source_url = item.get('source_url', '')
        source_description = item.get('source_description', '')
        author = get_author(script_name)

        new_item['source_name'] = source_name

        if author not in authors_stats:
            authors_stats[author] = 1
        else:
            authors_stats[author] += 1

        if category not in category_stats:
            category_stats[category] = 1
        else:
            category_stats[category] += 1

        if source_name not in source_stats:
            source_stats[source_name] = {}
            source_stats[source_name]["count"] = 1
            source_stats[source_name]["url"] = source_url
            source_stats[source_name]["description"] = source_description
        else:
            source_stats[source_name]["count"] += 1

        all.append(new_item)
        counter += 1
        file_counter += 1

    print(file.upper().replace(".JSON","") + ";" + str(file_counter))

random.shuffle(all)

current_date = datetime.now()
formatted_date = current_date.strftime("%Y_%m_%d")

with open("speakleash_pl_instructions_" + formatted_date + "_v" + version + ".jsonl", "w", encoding="utf-8") as plik:
    for item in all:
        plik.write(json.dumps(item, ensure_ascii=False) + "\n")

with open("authors_stats_" + formatted_date +  "_v" + version + ".json", "w", encoding="utf-8") as plik:
    plik.write(json.dumps(authors_stats, ensure_ascii=False))

with open("source_stats_" + formatted_date +  "_v" + version + ".json", "w", encoding="utf-8") as plik:
    plik.write(json.dumps(source_stats, ensure_ascii=False))

with open("category_stats_" + formatted_date +  "_v" + version + ".json", "w", encoding="utf-8") as plik:
    plik.write(json.dumps(category_stats, ensure_ascii=False))

print("Done!")
print("Total instructions: " + str(counter))
