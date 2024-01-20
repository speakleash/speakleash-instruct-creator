### IMPORTS
import json
import os
import random
import shutil
import tarfile
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
	'social_post':'post na mediach społecznościowych', 
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
		"instruction": ["Przydziel poniższy tekst do jednej z podanych kategorii: ",
				  "Sklasyfikuj tekst do jednej z podanych kategorii: ",
				  "Określ, do której kategorii należy poniższy tekst: ",
				  "Skategoryzuj poniższy tekst według podanych kategorii: ",
				  "Zaklasyfikuj tekst do jednej z dostępnych kategorii: "],
		"output": scenario,
		"categories": list(scenario.values())
	},
	"intent": {
		"type": "intent",
		"instruction": ["Zidentyfikuj intencję w poniższym tekście i przydzidziel do jednej z podanych kategorii: ",
				  "Skonkretyzuj zamiar zawarty w poniższym tekście i przypisz do odpowiedniej kategorii: ", 
				  "Znajdź intencję w poniższym tekście i zaklasyfikuj ją do jednej z wymienionych kategorii: ",
				  "Sklasyfikuj intencję w tekście i wybierz odpowiadającą kategorię: ",
				  "Przydziel intencję zawartą w tekście do jednej z kategorii: "],
		"output": intent,
		"categories": list(intent.values())
	},
	"intent_score": {
		"type": "intent_score",
		"instruction": ["Oceń trafność zidentyfikowanej intencji w poniższym tekście i sklasyfikuj intencję na podstawie podanych kategorii: ",
				  "Sklasyfikuj trafność identyfikacji intencji i przydziel jej jedną z kategorii: ",
				  "Skategoryzuj celność ekstrakcji intencji wiadomości i oceń jedną z kategorii: ",
				  "Sprawdź trafność rozpoznanej intencji w poniższym tekście i sklasyfikuj ją zgodnie z dostępnymi kategoriami: ",
				  "Dokładnie zweryfikuj intencję w tekście poniżej i przyporządkuj ją do jednej z wyznaczonych kategorii: "],
		"output": intent_score,
		"categories": list(intent_score.values())
	},
	"grammar_score": {
		"type": "grammar_score",
		"instruction": ["Oceń poprawność gramatyki w tekście i sklasyfikuj na podstawie podanych kategorii: ",
				  "Przeanalizuj poprawność gramatyczną w tekście poniżej i przyporządkuj ją do odpowiedniej kategorii: ",
				  "Sprawdź, czy gramatyka w tekście poniżej jest poprawna oraz przyporządkuj ją do jednej z kategorii: ",
				  "Zweryfikuj poprawność gramatyczną w podanym tekście i sklasyfikuj ją zgodnie z dostępnymi kategoriami: ",
				  "Na podstawie analizy jakości gramatyki, przyporządku tekst do jednej z kategorii: "],
		"output": grammar_score,
		"categories": list(grammar_score.values())
	},
	"spelling_score": {
		"type": "spelling_score",
		"instruction": ["Przeanalizuj poniższy tekst i sklasyfikuj ilość błędów w tekście na podstawie podanych kategorii: ",
				  "Sprawdź podany tekst i oceń ilość błędów zgodnie z podanymi kategoriami: ",
				  "Oceń poprawność podanego teksu i sklasyfikuj go według następujących kategorii: ",
				  "Zweryfikuj jakość tekstu i przyporządkuj go do jednej z kategorii: ",
				  "Przypisz podany tekst do jednej z kategorii na podstawie znalezionych w nim błędów: "],
		"output": spelling_score,
		"categories": list(spelling_score.values())
	},
	"language_identification": {
		"type": "language_identification",
		"instruction": ["Przeanalizuj poniższy tekst i sklasyfikuj język tego tekstu na podstawie podanych kategorii: ",
				  "Oceń język jakim jest pisany tekst oraz przypisz go do właściwej kategorii: ",
				  "Sprawdź w jakim języku został stworzony poniższy tekst i sklasyfikuj według kategorii: ",
				  "Jaki jest język tekstu? Odpowiedź na podstawie dostępnych kategorii: ",
				  "Przeanalizuj podany tekst i sklasyfikuj jego język mając do dyspozycji kategorie: "],
		"output": language_identification,
		"categories": list(language_identification.values())
	}
}

### FUNCTIONS
def download_and_unzip(url: str, 
					   destination_folder: str ='downloaded'):
	"""
	Download a file from the given URL and unzip it if it is in tar.gz or tgz format.

	Parameters:
	- url (str): The URL of the file to be downloaded.
	- destination_folder (str): The destination folder to save the downloaded and unpacked files.
							   Defaults to 'downloaded' if not provided.

	Returns:
	- bool: True if the download and unpacking were successful, False otherwise.
	"""
	
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
	"""
	Load instructions from a JSON Lines file, move the file to a specified directory,
	and clean up the downloaded folder.

	Returns:
	- list: A list containing the loaded instructions as dictionaries.

	Note:
	The file path is set to 'downloaded/1.1/data/pl-PL.jsonl', and the loaded data is
	moved to the 'data_dir' directory while maintaining its base name. The 'downloaded/'
	directory is then removed.

	Example:
	```python
	loaded_data = load_instructions()
	print(f"Total instructions loaded: {len(loaded_data)}")
	```

	"""
	# Prepare directories
	fpath = os.path.abspath('downloaded/1.1/data/pl-PL.jsonl')
	move_path = os.path.join(data_dir, os.path.basename(fpath))

	os.makedirs(data_dir, exist_ok=True)
	os.makedirs(output_dir, exist_ok=True)
	
	data = []

	# Load in the data
	with jsonlines.open(fpath) as f:
		for line in f.iter():
			data.append(line)	

	# Delete unneseccasry files
	shutil.move(fpath, move_path)
	shutil.rmtree('downloaded/')

	print(f"Loaded {len(data)} base instructions")
	return data

def get_categories_as_string(categories: List,
							 main_category: str = None,
							 k: int = 4):
	"""
	Generate a string representation of a list of random categories, including the specified main category.

	Parameters:
	- main_category (str): The main category that must be included in the generated list.
	- categories (List): A list of available categories to choose from.
	- k (int): The number of categories to generate (excluding the main category). Defaults to 4.

	Returns:
	- str: A string representation of the generated list of categories in a shuffled order.

	Example:
	```python
	main_category = "Science"
	all_categories = ["Technology", "Nature", "Math", "History", "Art"]
	category_string = get_categories_as_string(main_category, all_categories, k=3)
	print("Random Categories:", category_string)
	```

	Note:
	If the provided list of categories has more than 10 elements, the function generates a shuffled
	list of k random categories (excluding the main category) using random.choices. If there are 10
	or fewer elements, the entire list is used. The main category is ensured to be included in the
	final list, and the result is returned as a comma-separated string.
	"""

	if len(categories) > 10 and main_category: 
		x = 0
		while x != 5:
			random_categories = random.choices(list(categories), k=5)
			if main_category not in random_categories:
				x = len(set(random_categories))
		
		random_categories.append(main_category)

	else:
		random_categories = categories

	random.shuffle(random_categories)
	output = ", ".join(random_categories) + "."
	return output

def create_instructions(data: List[Dict],
						main_dict: Dict):

	"""
	Create a list of instructions based on input data and a provided main dictionary.

	Parameters:
	- data (List[Dict]): A list of dictionaries containing input data, judgments, and other information.
	- main_dict (Dict): A dictionary containing configuration details, categories, and instructions.

	Returns:
	- List[Dict]: A list of instructions as dictionaries.

	Example:
	```python
	input_data = [...]  # List of dictionaries containing input data
	main_configuration = {...}  # Dictionary containing configuration details

	instructions = create_instructions(input_data, main_configuration)
	```

	Note:
	The function creates instructions based on the given input data and main dictionary. It uses
	configuration details, categories, and instructions to generate a list of dictionaries with
	instructions, input data, output details, and other metadata. Two loops are used: the base loop
	for 'intent' and 'scenario' types, and the inner loop for 'intent_score', 'grammar_score',
	'spelling_score', and 'language_identification' types.
	"""

	# Setup variables
	output = []
	temp = {}

	type_base = ['intent', 'scenario']
	type_inner = ['intent_score', 'grammar_score', 'spelling_score', 'language_identification']

	# Base type loop
	for type in type_base:
		for item in data:
			for worker in item['judgments']:

				categories = get_categories_as_string(
					main_category=main_dict[type]['output'][item[type]], 
					categories=main_dict[type]['categories'])

				'''
				OPTIONAL DICTIONARY CREATION EXAMPLE
				temp = {
					'instruction': random.choice(main_dict[type]['instruction']),
					'input': item['utt'],
					'output': main_dict[type]['output'][item[type]],
					'categories': main_dict[type]['categories'],
					'source_name': source_name,
					'source_url': source_url,
					'source_description': source_description,
					'script_name': script_name
				}
				'''

				temp['instruction'] = random.choice(main_dict[type]['instruction']) + categories
				temp['input'] = item['utt']
				temp['output'] = main_dict[type]['output'][item[type]]

				# Categories not needed bue to them being included in the main instruction
				#temp['categories'] = main_dict[type]['categories']
				#temp['categories'] = categories

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

				categories = get_categories_as_string( 
					categories=main_dict[type]['categories'])

				temp['instruction'] = random.choice(main_dict[type]['instruction']) + categories
				temp['input'] = item['utt']
				temp['output'] = main_dict[type]['output'][worker[type]]
				#temp['categories'] = main_dict[type]['categories']
				temp['source_name'] = source_name
				temp['source_url'] = source_url
				temp['source_description'] = source_description
				temp['script_name'] = script_name
				output.append(temp)
				temp = {}
	
	print(f"Inner loop finished, created {len(output) - output_base_cnt} instructions.")


	print(f"Collected {len(output)} instructions")
	return output

def remove_duplicates(data, shuffle=False):
	"""
	Remove duplicate items from a list, optionally shuffling the unique items.

	Parameters:
	- data: The input list containing items to be deduplicated.
	- shuffle (bool): If True, shuffle the unique items in the output list. Defaults to False.

	Returns:
	- list: A deduplicated list of items.

	Example:
	```python
	input_data = [...]  # List containing items with potential duplicates
	unique_data = remove_duplicates(input_data, shuffle=True)
	```

	Note:
	The function removes duplicate items from the input list, maintaining the order of the first
	occurrence of each item. The deduplicated list is returned, and if specified, it can be shuffled.
	The function prints information about the deduplication process, including the number of
	duplicates found and the size of the final output list.
	"""
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

	if shuffle:
		random.shuffle(output)

	return output

def save_instructions(instructions, output_dir, json_file='amazon-massive-pl.json'):
	"""
	Save a list of instructions to a JSON file.

	Parameters:
	- instructions: The list of instructions to be saved.
	- output_dir (str): The directory where the JSON file will be saved.
	- json_file (str): The name of the JSON file. Defaults to 'amazon-massive-pl.json'.

	Example:
	```python
	instruction_list = [...]  # List of instructions to be saved
	save_instructions(instruction_list, '/path/to/output_directory')
	```

	Note:
	The function saves the provided list of instructions to a JSON file located in the specified
	output directory. The JSON file is formatted with an indentation of 4 spaces, and non-ASCII
	characters are preserved. After successfully saving the instructions, a confirmation message
	is printed, including the path to the saved file.
	"""
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
download_and_unzip(url=source_url)
data = load_instructions()
instructions = create_instructions(data, main_dict)
instructions_cleared = remove_duplicates(instructions, shuffle=True)
save_instructions(instructions_cleared, output_dir)