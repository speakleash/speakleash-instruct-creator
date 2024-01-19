### IMPORTS
import os
import tarfile
import shutil
import random
import json
from typing import Dict, List

import jsonlines
import requests


### DICTS
# Ocena trafności odczytanej intencji
intent_score = {
	0: "Intencja nie jest zrozumiała",
	1: "Intencja jest zrozumiała",
	2: "To bardzo trafna interpretacja intencji"
}

# Ocena składni i gramatyki
grammar_score = {
	0: "Nienaturalna gramatyka", # Completely unnatural (nonsensical, cannot be understood at all)
	1: "Znaczące błędy w gramatyce", # Severe errors (the meaning cannot be understood and doesn't sound natural in your language)
	2: "Drobne błędy w gramatyce", # Some errors (the meaning can be understood but it doesn't sound natural in your language)
	3: "Dobra jakość gramatyki", # Good enough (easily understood and sounds almost natural in your language)
	4: "Idealna gramatyka" # Perfect (sounds natural in your language)
}

# Poprawność 
spelling_score = {
	0: "Więcej niż 2 błędy",
	1: "1 lub 2 błędy",
	2: "Brak błędów"
}

# Klasyfikacja języka
language_identification = {
	"target": "Język polski",
	"english": "Język angielski",
	"other": "Inny język",
	"target|english": "Język polski i angielski",
	"target|other": "Język polski i inny",
	"english|other": "Język angielski i inny",
	"target|english|other": "Język polski, angielski i inny"
}

# Kategorie
scenario = {
	"alarm": "budzik",
	"audio": "system grający",
	"iot": "inteligentny dom",
	"calendar": "kalendarz",
	"play": "odtwarzanie",
	"general": "ogólne",
	"datetime": "czas i data",
	"takeaway": "zamówienie na wynos",
	"news": "wiadomości",
	"music": "muzyka",
	"weather": "pogoda",
	"qa": "pytania i odpowiedzi",
	"social": "media społecznościowe",
	"recommendation": "sugestie i rekomendacje",
	"cooking": "gotowanie",
	"transport": "przemieszczanie się",
	"email": "emaile",
	"lists": "listy"
}

# Intencje
intent = {
	'alarm_set': 'ustawienie budzika',
	'audio_volume_mute': 'wyciszenie dźwięku',
	'iot_hue_lightchange': 'zmiana inteligentnego oświetlenia',
	'iot_hue_lightoff': 'wyłączenie inteligentnego oświetlenia',
	'iot_hue_lighton': 'włączenie inteligentnego oświetlenia',
	'iot_hue_lightdim': 'przyciemnienie oświetlenia',
	'iot_cleaning': 'użycie inteligentnego sprzętu sprzątającego',
	'calendar_query': 'zapytanie o termin',
	'play_music': 'odtworzenie muzyki', 
	'general_quirky': 'zapytanie o coś',
	'general_greet': 'przywitanie', 
	'datetime_query': 'zapytanie o czas i godzinę',
	'datetime_convert': 'konwersja czasu',
	'takeaway_query': 'zapytanie związane z zamówieniem na wynos', 
	'alarm_remove': 'usunięcie stałego budzika', 
	'alarm_query': 'zapytanie związane z budzikiem',
	'news_query': 'zapytanie związane z wiadomościami',
	'music_likeness': 'pozytywna ocena muzyki',
	'music_query': 'zapytanie związane z muzyką', 
	'iot_hue_lightup': 'zwiększenie natęzenia inteligentnego oświetlenia',
	'takeaway_order': 'zamówienie na wynos',
	'weather_query': 'zapytanie związane z pogodą',
	'music_settings': 'ustawienia odtwarzacza muzyki',
	'audio_volume_down': 'ściszenie odtwarzacza',
	'general_joke': 'zapytanie o dowcip',
	'music_dislikeness': 'negatywna ocena muzyki',
	'audio_volume_other': 'zapytanie o głośność odtwarzacza',
	'iot_coffee': 'zapytanie inteligentnego sprzętu o napój',
	'audio_volume_up': 'zwiększenie głośności odtwarzacza',
	'iot_wemo_on': 'włączenie inteligentnego sterowania zasilaniem',
	'iot_wemo_off': 'wyłączenie inteligentnego sterowania zasilaniem',
	'qa_stock': 'zapytanie o akcje na giełdzie', 
	'play_radio': 'użycie radia',
	'social_post':' post na mediach społecznościowych', 
	'recommendation_locations': 'rekomendacja celu podróży', 
	'cooking_recipe': 'przepis na potrawę',
	'qa_factoid': 'odpowiedź na pytanie',
	'recommendation_events': 'rekomendacja wydarzenia',
	'calendar_set': 'ustawienie wydarzenia lub przypomnienia w kalendarzu',
	'play_audiobook': 'odtwarzanie audiobooka',
	'play_podcasts': 'odtwarzanie podcastu',
	'social_query': 'zapytanie związane z mediami społecznościowymi',
	'transport_query': 'zapytanie związane z podrózą', 
	'email_sendemail': 'wysłanie emaila', 
	'transport_ticket': 'bilet na podróż',
	'recommendation_movies': 'rekomendacja filmu', 
	'lists_query': 'zapytanie związane z listą (np. zakupowe)',
	'play_game': 'zapytanie o grę', 
	'email_query': 'zapytanie związanie z emailem',
	'transport_traffic': 'zapytanie o natężenie ruchu',
	'cooking_query': 'zapytanie związane z gotowaniem',
	'qa_definition': 'zapytanie o definicję',
	'calendar_remove': 'usunięcie wydarzenia z kalendarza',
	'lists_remove': 'usunięcie listy', 
	'email_querycontact': 'zapytanie związane z listą kontaktów',
	'lists_createoradd': 'edytowanie listy', 
	'email_addcontact': 'dodaj kontakt do ksiązki adresowej email', 
	'transport_taxi': 'zapytanie o taksówkę',
	'qa_maths': 'zapytanie związane z matematyką', 
	'qa_currency': 'zapytanie związane z kursem walut'
}

# Main dictionary for function purposes
main_dict = {
	"scenario": {
		"type": "scenario",
		"instruction": "Przydziel poniszy tekst do jednej z podanych kategorii: ",
		"output": scenario,
		"categories": list(scenario.values())
	},
	"intent": {
		"type": "intent",
		"instruction": "Zidentyfikuj intencję w poniższym tekście i przydzidziel do jednej z podanych kategorii: ",
		"output": intent,
		"categories": list(intent.values())
	},
	"intent_score": {
		"type": "intent_score",
		"instruction": "Oceń trafność zidentyfikowanej intencji w poniższym tekście i sklasyfikuj intencję na podstawie podanych kategorii: ",
		"output": intent_score,
		"categories": list(intent_score.values())
	},
	"grammar_score": {
		"type": "grammar_score",
		"instruction": "Oceń poprawność gramatyki w poniższym tekście i sklasyfikuj na podstawie podanych kategorii: ",
		"output": grammar_score,
		"categories": list(grammar_score.values())
	},
	"spelling_score": {
		"type": "spelling_score",
		"instruction": "Przeanalizuj poniższy tekst i sklasyfikuj ilość błędów w tekście na podstawie podanych kategorii: ",
		"output": spelling_score,
		"categories": list(spelling_score.values())
	},
	"language_identification": {
		"type": "language_identification",
		"instruction": "Przeanalizuj poniższy tekst i sklasyfikuj język tego tekstu na podstawie podanych kategorii: ",
		"output": language_identification,
		"categories": list(language_identification.values())
	}
}

### FUNCTIONS
def download_and_unzip(url="https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz", 
					   destination_folder='downloaded'):
	# Create destination folder 
	os.makedirs(destination_folder, exist_ok=True)

	# Get the file name from the URL
	file_name = url.split("/")[-1]
	file_path = os.path.join(destination_folder, file_name)

	# Download the file
	print(f"Starting download: {file_name}")
	try:
		response = requests.get(url)
		if response.ok:
			with open(file_path, 'wb') as f:
				f.write(response.content)
			print(f"File {file_name} downloaded successfully.")
	except Exception as e:
		print(f"An error has occured: {e}")
		return False
	
	# Unpack the file
	if file_name.endswith('.tar.gz') or file_name.endswith('tgz'):
		with tarfile.open(file_path, 'r:gz') as tar:
			tar.extractall(destination_folder)
			print(f"File {file_name} unpacked successfully")
			return True
	else:
		print(f"Unsupported file format: {file_name}")
		return False

def load_instructions():
	fpath = os.path.abspath('downloaded/1.1/data/pl-PL.jsonl')
	move_path = os.path.join(data_dir, os.path.basename(fpath))

	os.makedirs(data_dir, exist_ok=True)
	os.makedirs(output_dir, exist_ok=True)
	
	data = []

	with jsonlines.open(fpath) as f:
		for line in f.iter():
			data.append(line)	

	shutil.move(fpath, move_path)
	shutil.rmtree('downloaded/')

	print(f"Loaded {len(data)} base instructions")
	return data

def create_instructions(data: List[Dict],
						main_dict: Dict,
						):
	output = []
	temp = {}

	type_base = ['intent', 'scenario']
	type_inner = ['intent_score', 'grammar_score', 'spelling_score', 'language_identification']

	# Base type loop
	for type in type_base:
		for item in data:
			for worker in item['judgments']:
				temp['instruction'] = main_dict[type]['instruction']
				temp['input'] = item['utt']
				temp['output'] = main_dict[type]['output'][item[type]]
				temp['categories'] = main_dict[type]['categories']
				temp['source_name'] = source_name
				temp['source_url'] = source_url
				temp['source_description'] = source_description
				temp['script_name'] = script_name
				output.append(temp)
				temp = {}
	
	print(f"Base loop finished, created {len(output)} instructions.")

	# Base loop counter
	output_base_cnt = len(output)

	# Inner type loop
	for type in type_inner:
		for item in data:
			for worker in item['judgments']:
				temp['instruction'] = main_dict[type]['instruction']
				temp['input'] = item['utt']
				temp['output'] = main_dict[type]['output'][worker[type]]
				temp['categories'] = main_dict[type]['categories']
				temp['source_name'] = source_name
				temp['source_url'] = source_url
				temp['source_description'] = source_description
				temp['script_name'] = script_name
				output.append(temp)
				temp = {}
	
	print(f"Inner loop finished, created {len(output) - output_base_cnt} instructions.")


	print(f"Collected {len(output)} instructions")
	return output

def remove_duplicates(data):
	seen = set()
	output = []


	for item in data:
		if str(item) not in seen:
			seen.add(str(item))
			output.append(item)
	
	before = len(data)
	after = len(output)

	print(f"Deduplication finished, found {before-after} duplicates")
	print(f"Final output is {after} instructions")

	random.shuffle(output)

	return output

def save_instructions(instructions, output_dir, json_file='amazon-massive-pl.json'):
	fpath = os.path.join(output_dir, json_file)
	with open(fpath, 'w', encoding='utf-8') as f:
		json.dump(instructions, f, indent=4, ensure_ascii=False)

	print(f"Instructions saved successfully to {fpath}")


### CONFIG 
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')
output_dir = os.path.join(base_dir, 'output')
source_name = "amazon-massive-nlu-v1.1/pl-PL.json"
source_url = "https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz"
source_description = "Instrukcje powstały dzięki wykorzystaniu zestawu danych Amazon Massive NLU Dataset, version 1.1."
script_name = os.path.basename(__file__)


### MAIN
download_and_unzip()
data = load_instructions()
instructions = create_instructions(data, main_dict)
instructions_cleared = remove_duplicates(instructions)
save_instructions(instructions_cleared, output_dir)