import os 
import random
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")

source_name = "TODO"
source_url = "https://TODO"
source_description = "TODO PO POLSKU"
script_name = os.path.basename(__file__)

instructions = []

for i in range(100):
    instructions.append({"instruct": "Stwórz krótki tekst o SpeakLeashu", "input" : "", "output" : "Otwarty projekt, którego celem jest zbudowanie zestawu danych dla Dużego Modelu Językowego, o rozmiarze co najmniej 1TB, składającego się z różnorodnych tekstów w języku polskim. Naszym celem jest umożliwienie badań nad uczeniem maszynowym i wytrenowanie na podstawie zebranych danych, generatywnego, wstępnie wytrenowanego modelu transformatora.", "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})

random.shuffle(instructions)
with open(os.path.join(output_dir, "TODO.json"), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))






