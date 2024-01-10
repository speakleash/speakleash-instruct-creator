import json
import os
import random
import subprocess
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "output")
data_dir = os.path.join(base_dir, "data")
version = "0_0_2"

generate = False

scipts_to_run = []
scipts_to_run.append({"script_name" : "allegro_klej_dyk_questions.py", "author" : "Ic & MariaF"})
scipts_to_run.append({"script_name" : "legal-questions.py", "author" : "Ic & MariaF"})
scipts_to_run.append({"script_name" : "polish-summaries-corpus.py", "author" : "Ic & MariaF"})
scipts_to_run.append({"script_name" : "polqa_questions.py", "author" : "Ic & MariaF"})
scipts_to_run.append({"script_name" : "poquad_text_extraction.py", "author" : "Ic & MariaF"})
scipts_to_run.append({"script_name" : "speakleash-categorization.py", "author" : "Amarok & Sekon"})
scipts_to_run.append({"script_name" : "speakleash_forums_questions.py", "author" : "Ic & MariaF"})
scipts_to_run.append({"script_name" : "wiki-lemmat-words.py", "author" : "Sekon"})
scipts_to_run.append({"script_name" : "allegro-summarization.py", "author" : "Sekon"})
scipts_to_run.append({"script_name" : "speakleash-create-sentence.py", "author" : "Sekon"})
scipts_to_run.append({"script_name" : "create_password.py", "author" : "Sekon"})
scipts_to_run.append({"script_name" : "plwiki_create_random_word_list.py", "author" : "Sekon"})


if generate:
    for script in scipts_to_run:
        print("Running: " + script["script_name"])
        result = subprocess.run([sys.executable, script["script_name"]], capture_output=True, text=True)
        

def get_author(script_name):
    for script in scipts_to_run:
        if script["script_name"] == script_name:
            return script["author"]

print("Merging files...")

files = os.listdir(output_dir)
all = []
counter = 1

authors_stats = {}
source_stats = {}

for file in files:
    file_path = os.path.join(output_dir, file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    file_counter = 1

    for item in data:

        new_item = {}
        new_item['instruct'] = item['instruct']
        new_item['input'] = item['input']
        new_item['output'] = item['output']

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

with open("speakleash_pl_instructions_v" + version + ".jsonl", "w", encoding="utf-8") as plik:
    for item in all:
        plik.write(json.dumps(item, ensure_ascii=False) + "\n")

with open("authors_stats_v" + version + ".json", "w", encoding="utf-8") as plik:
    plik.write(json.dumps(authors_stats, ensure_ascii=False))

with open("source_stats_v" + version + ".json", "w", encoding="utf-8") as plik:
    plik.write(json.dumps(source_stats, ensure_ascii=False))

print("Done!")
print("Total instructions: " + str(counter))
