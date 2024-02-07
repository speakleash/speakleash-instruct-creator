import os
import random
import json

try:
    from utils.functions import download_file, get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

script_name = os.path.basename(__file__)
source_name = script_name.replace(".py", "")
source_url = "https://pl.wikiquote.org/wiki/"
source_description = "Instrukcje powstały podstawie cytatów z polskiej Wikicytaty."


instruction_limit = 150000

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")
replicate_to = os.path.join(base_dir, "datasets")
download_dir = os.path.join(base_dir, "download")

url = "http://instruct.speakleash.space/raw/quotes_output.json"

if not os.path.exists(download_dir):
    os.makedirs(download_dir)

counter = 0
instructions = []


def bulleting(words, mode):
    if mode == 0:
        return "\n".join([f"• {word}" for word in words])
    else:
        return "\n".join([f"{i+1}. {word}" for i, word in enumerate(words)])
   
first_name = [
    "Anna",
    "Maria",
    "Katarzyna",
    "Małgorzata",
    "Agnieszka",
    "Barbara",
    "Ewa",
    "Krystyna",
    "Elżbieta",
    "Zofia",
    "Janina",
    "Teresa",
    "Danuta",
    "Jadwiga",
    "Irena",
    "Halina",
    "Helena",
    "Grażyna",
    "Bożena",
    "Stanisława",
    "Jan",
    "Andrzej",
    "Piotr",
    "Krzysztof",
    "Stanisław",
    "Tomasz",
    "Paweł",
    "Józef",
    "Marcin",
    "Marek",
    "Michał",
    "Grzegorz",
    "Jerzy",
    "Tadeusz",
    "Adam",
    "Łukasz",
    "Zbigniew",
    "Ryszard",
    "Dariusz",
    "Henryk",
]

def is_person(category):
    # Simple, limited. You have to look for a better solution
    
    parts = category.split(" ")
    
    if len(parts) != 2:
        return False
    
    name = category.split(" ")[0]

    if name in first_name:
        return True



def number_2_10_in_words(nr):
    if nr == 2:
        return "dwa"

    if nr == 3:
        return "trzy"

    if nr == 4:
        return "cztery"

    if nr == 5:
        return "pięć"

    if nr == 6:
        return "sześć"

    if nr == 7:
        return "siedem"

    if nr == 8:
        return "osiem"

    if nr == 9:
        return "dziewięć"

    if nr == 10:
        return "dziesięć"


counter = 0
instructions = []

if not os.path.exists(os.path.join(download_dir, "quotes_output.json")):
    download_file(url, download_dir, "quotes_output.json")
    print("Downloaded file: " + url)

with open(os.path.join(download_dir, "quotes_output.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

keywords = {}

# f"Wypisz {quotes_count_in_words} znane cytaty dotyczące {words[0]}.",
# f"Podaj {quotes_count_in_words} powszechnie znane cytaty o {words[2]}.",

keywords["Zmysły"] = ["zmysłów", "z zmysłami", "zmysłach"]
keywords["Miłość"] = ["miłości", "z miłością", "miłości"]
keywords["Życie"] = ["życia", "z życiem", "życiu"]
keywords["Przyjaźń"] = ["przyjaźni", "z przyjaźnią", "przyjaźni"]
keywords["Szczęście"] = ["szczęścia", "ze szczęściem", "szczęściu"]
keywords["Praca"] = ["pracy", "z pracą", "pracy"]
keywords["Pieniądze"] = ["pieniędzy", "z pieniędzmi", "pieniędzmi"]
keywords["Czas"] = ["czasu", "z czasem", "czasie"]
keywords["Rodzina"] = ["rodziny", "z rodziną", "rodzinie"]

keywords["Mądrość"] = ["mądrości", "z mądrością", "mądrości"]
keywords["Sukces"] = ["sukcesu", "z sukcesem", "sukcesie"]
keywords["Przyszłość"] = ["przyszłości", "z przyszłością", "przyszłości"]
keywords["Wiedza"] = ["wiedzy", "z wiedzą", "wiedzy"]
keywords["Wolność"] = ["wolności", "z wolnością", "wolności"]
keywords["Prawda"] = ["prawdy", "z prawdą", "prawdzie"]
keywords["Wojna"] = ["wojny", "z wojną", "wojnie"]
keywords["Prawo"] = ["prawa", "z prawem", "prawie"]
keywords["Zdrowie"] = ["zdrowia", "ze zdrowiem", "zdrowiu"]

# Wypisz dwa znane cytaty dotyczące miłości

for item in data:

    category = item.get("category", "")
    quotes = item.get("quotes", [])

    if is_person(category):

        quotes_count = random.randint(2, 4)
        if quotes_count > len(quotes):
            quotes_count = len(quotes)

        quotes_count_in_words = number_2_10_in_words(quotes_count)
       
        random.shuffle(quotes)
        quotes = quotes[:quotes_count]

        instruct = random.choice(
            [
                f"Podaj {quotes_count} popularne cytaty związane z daną osobą lub której są autorstwem.",
                f"Podaj {quotes_count_in_words} popularne cytaty związane z daną osobą lub której są autorstwem.",
                f"Przytocz {quotes_count} słynne cytaty powiązane z określoną osobą lub które napisała",
                f"Przytocz {quotes_count_in_words} słynne cytaty powiązane z określoną osobą lub które napisała",
                f"Przedstaw {quotes_count} znane cytaty dotyczące wybranej osoby lub której są autorstwa",
                f"Przedstaw {quotes_count_in_words} znane cytaty dotyczące wybranej osoby lub której są autorstwa",
            ]
        )

        output = random.choice(
            [
                "\n".join(quotes),
                "\n".join([f"• {q}" for q in quotes]),
                "\n".join([f"{i+1}. {q}" for i, q in enumerate(quotes)]),
            ]
        )

        input = category
        instructions.append(
            {
                "instruct": instruct,
                "input": input,
                "output": output,
                "source_name": source_name,
                "source_url": source_url,
                "source_description": source_description,
                "script_name": script_name,
            }
        )


    if category in keywords:
        for k in range(3):
            words = keywords[category]

            quotes_count = random.randint(2, 4)
            if quotes_count > len(quotes):
                quotes_count = len(quotes)

            quotes_count_in_words = number_2_10_in_words(quotes_count)

            random.shuffle(quotes)
            quotes = quotes[:quotes_count]

            instruct = random.choice(
                [
                    f"Wypisz {quotes_count_in_words} znane cytaty dotyczące {words[0]}.",
                    f"Wypisz {quotes_count} znane cytaty dotyczące {words[0]}.",
                    f"Podaj {quotes_count_in_words} powszechnie znane cytaty o {words[2]}.",
                    f"Podaj {quotes_count} powszechnie znane cytaty o {words[2]}.",
                    f"Czy możesz wskazać {quotes_count_in_words} popularne cytaty dotyczące {words[0]}?",
                    f"Proszę o {quotes_count} znane powiedzenia na temat {words[0]}",
                    f"Proszę o {quotes_count_in_words} znane powiedzenia na temat {words[0]}",
                ]
            )

            output = random.choice(
                [
                    "\n".join(quotes),
                    "\n".join([f"• {q}" for q in quotes]),
                    "\n".join([f"{i+1}. {q}" for i, q in enumerate(quotes)]),
                ]
            )

            input = ""
            instructions.append(
                {
                    "instruct": instruct,
                    "input": input,
                    "output": output,
                    "source_name": source_name,
                    "source_url": source_url,
                    "source_description": source_description,
                    "script_name": script_name,
                }
            )


with open(os.path.join(download_dir, "quotes_output.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
    print("Saved file: " + os.path.join(download_dir, "quotes_output.json"))

random.shuffle(instructions)
with open(
    os.path.join(output_dir, script_name.replace(".py", ".json")), "w", encoding="utf-8"
) as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))
