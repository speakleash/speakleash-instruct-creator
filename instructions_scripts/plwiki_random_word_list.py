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

limit = 1000
instruction_limit = 150000

base_dir = os.path.dirname(os.path.abspath(__file__))
# data_dir = get_dir_path("data") or os.path.join(base_dir, "data") #  commented out until Speakleash package update
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")
replicate_to = get_dir_path("data_speakleash") or os.path.join(base_dir, "data_speakleash")

sl = Speakleash(replicate_to)
counter = 0
wiki = sl.get("plwiki").data
instructions = []
words = {}


def get_random_word(words, words_count, lemma_mode, char):
    random_words = []
    new_words = []

    if lemma_mode == 0:
        new_words = list(words.values())
    else:
        new_words = list(words.keys())

    random.shuffle(new_words)

    for word in new_words:
        if char == ' ':
            random_words.append(word)
        else:
            if word[0] == char:
                random_words.append(word)

        if len(random_words) == words_count:
            break

    return random_words


def bulleting(words, mode):
    if mode == 0:
        return "\n".join([f"• {word}" for word in words])
    else:
        return "\n".join([f"{i + 1}. {word}" for i, word in enumerate(words)])


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


def create_instruct(verbs, nouns, adjs, instruct_type):
    words_count = random.randint(4, 10)
    words_count_in_words = number_2_10_in_words(words_count)
    lemma_mode = random.randint(0, 1)

    if random.randint(0, 1) == 0:
        char = random.choice("abcdefghijklmnoprstuwzśźżćł")
    else:
        char = ' '

    words = []

    if instruction_type == 0:
        words = get_random_word(all, words_count, lemma_mode, char)
    if instruction_type == 1:
        words = get_random_word(verbs, words_count, lemma_mode, char)
    if instruction_type == 2:
        words = get_random_word(nouns, words_count, lemma_mode, char)
    if instruction_type == 3:
        words = get_random_word(adjs, words_count, lemma_mode, char)

    instruct = ""
    output = ""
    input = ""

    if lemma_mode == 0 and char != ' ':
        instruct = random.choice([
                f"Podaj {words_count_in_words} słów (formie podstawowej) rozpoczynających się na literę \"{char}\".",
                f"Podaj {words_count} słów (formie podstawowej) rozpoczynających się na literę \"{char}\".",
                f"Wymień {words_count_in_words} słów (formie podstawowej), które zaczynają się na literę \"{char}\".",
                f"Wymień {words_count} słów (formie podstawowej), które zaczynają się na literę \"{char}\".",
                f"Czy możesz podać {words_count_in_words} słów (formie podstawowej) zaczynających się na literę \"{char}\".",
                f"Czy możesz podać {words_count} słów (formie podstawowej) zaczynających się na literę \"{char}\".",
                f"Czy jesteś w stanie wymienić {words_count_in_words} słów (formie podstawowej) rozpoczynających się na literę \"{char}\".",
                f"Czy jesteś w stanie wymienić {words_count} słów (formie podstawowej) rozpoczynających się na literę \"{char}\".",
                f"Czy możesz wymienić {words_count_in_words} słów (formie podstawowej), które zaczynają się na literę \"{char}\".",
                f"Czy możesz wymienić {words_count} słów (formie podstawowej), które zaczynają się na literę \"{char}\".",
        ])

    if lemma_mode == 0 and char == ' ':
        instruct = random.choice([
                f"Podaj {words_count_in_words} słów (w formie podstawowej).",
                f"Podaj {words_count} słów (w formie podstawowej).",
                f"Wymień {words_count_in_words} słów (w formie podstawowej).",
                f"Wymień {words_count} słów (w formie podstawowej).",
                f"Czy możesz podać {words_count_in_words} słów (w formie podstawowej).",
                f"Czy możesz podać {words_count} słów (w formie podstawowej).",
                f"Czy jesteś w stanie wymienić {words_count_in_words} słów (w formie podstawowej).",
                f"Czy jesteś w stanie wymienić {words_count} słów (w formie podstawowej).",
                f"Czy możesz wymienić {words_count_in_words} słów (formie podstawowej).",
                f"Czy możesz wymienić {words_count} słów (formie podstawowej).",
        ])

    if lemma_mode == 1 and char != ' ':
        instruct = random.choice([
                f"Podaj {words_count_in_words} słów rozpoczynających się na literę \"{char}\".",
                f"Podaj {words_count} słów rozpoczynających się na literę \"{char}\".",
                f"Wymień {words_count_in_words} słów rozpoczynających się na literę \"{char}\".",
                f"Wymień {words_count} słów rozpoczynających się na literę \"{char}\".",
                f"Czy możesz podać {words_count_in_words} słów rozpoczynających się na literę \"{char}\".",
                f"Czy możesz podać {words_count} słów rozpoczynających się na literę \"{char}\".",
                f"Czy jesteś w stanie wymienić {words_count_in_words} słów rozpoczynających się na literę \"{char}\".",
                f"Czy jesteś w stanie wymienić {words_count} słów rozpoczynających się na literę \"{char}\".",
                f"Czy możesz wymienić {words_count_in_words} słów, które zaczynają się na literę \"{char}\".",
                f"Czy możesz wymienić {words_count} słów, które zaczynają się na literę \"{char}\".",
        ])

    if lemma_mode == 1 and char == ' ':
        instruct = random.choice([
                f"Podaj {words_count_in_words} słów.",
                f"Podaj {words_count} słów.",
                f"Wymień {words_count_in_words} słów.",
                f"Wymień {words_count} słów.",
                f"Czy możesz podać {words_count_in_words} słów.",
                f"Czy możesz podać {words_count} słów.",
                f"Czy jesteś w stanie wymienić {words_count_in_words} słów.",
                f"Czy jesteś w stanie wymienić {words_count} słów.",
                f"Czy możesz wymienić {words_count_in_words} słów.",
                f"Czy możesz wymienić {words_count} słów.",
        ])

    output = random.choice([
            ", ".join(words),
            " ".join(words),
            "\n".join(words),
            "/".join(words),
            "\n".join([f"• {word}" for word in words]),
            "\n".join([f"{i + 1}. {word}" for i, word in enumerate(words)])
    ])

    return instruct, input, output, words_count, len(words)


verbs = {}
nouns = {}
adjs = {}
counter = 0

for txt in wiki:
    doc = nlp(txt)
    counter += 1
    print("Analiza słów, krok " + str(counter) + " z " + str(limit))
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_digit and token.is_oov == False:
            word = token.text.strip()
            lemma = token.lemma_.strip()

            if token.pos_ == "VERB":
                if lemma not in verbs:
                    verbs[lemma] = word

            if token.pos_ == "NOUN":
                if lemma not in nouns:
                    nouns[lemma] = word

            if token.pos_ == "ADJ":
                if lemma not in adjs:
                    adjs[lemma] = word

    if counter > limit:
        break

all = {}
all.update(verbs)
all.update(nouns)
all.update(adjs)

for i in range(instruction_limit):
    instruction_type = random.randint(0, 3)
    print("Instrukcje: " + str(len(instructions)) + " z " + str(instruction_limit))
    instruct, input, output, count1, count2 = create_instruct(verbs, nouns, adjs, instruction_type)
    if count1 == count2:
        instructions.append({"instruct": instruct, "input": input, "output": output, "source_name": source_name,
                             "source_url": source_url, "source_description": source_description,
                             "script_name": script_name})

random.shuffle(instructions)
with open(os.path.join(output_dir, script_name.replace(".py", ".json")), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))
