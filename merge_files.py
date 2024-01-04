import json
import os
import random

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "output")
data_dir = os.path.join(base_dir, "data")
version = "0_0_2"

files = os.listdir(output_dir)
all = []
counter = 1

for file in files:
    file_path = os.path.join(output_dir, file)
    with open(file_path, "r") as f:
        data = json.load(f)

    for item in data:
        item['source'] = file.replace(".json", "")
        all.append(item)
        counter += 1

random.shuffle(all)

with open("speakleash_pl_instructions_v" + version + ".jsonl", "w") as plik:
    for item in all:
        plik.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Done!")
print("Total instructions: " + str(counter))
