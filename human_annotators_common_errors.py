"""Instructions creator based on human_annotators_common_errors"""
import json
import os
import random

import jsonlines

from utils.functions import download_file

# Mandatory dataset data for json objects
SOURCE_NAME = f"{os.path.basename(__file__).replace('.py', '')}"
SOURCE_URL = 'https://github.com/Ermlab/polish-gec-datasets/blob/main/'
SOURCE_DESCRIPTION = 'Zbiór danych zawierający zbiory testowe do korekcji błędów ortograficznych. Dataset składa się ' \
                     'ze zdań prawidłowych, nieprawidłowych oraz wskazań błędów ortograficznych. Autore zestawu ' \
                     'danych to Ermlab'

script_name = os.path.basename(__file__)

# Get the path to the currently executing python script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define directories name for downloaded and output files
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")

# Create directory for downloading data from server / link
os.makedirs(data_dir, exist_ok=True)

# Create directory (if does not exists) for created instructions json files
os.makedirs(output_dir, exist_ok=True)


def _convert_github_url(git_url: str) -> str:
    """
    Converts provided github url to downloadable url for raw format files. If is not from github or already
    represents raw file, it returns unchanged link.

    :param url: Link to the githhub repository file
    :return: Link to the githhub repository in raw format, if conditions are met.
    """
    if 'github' in git_url and '/tree/' in git_url and not 'raw' in git_url:
        return git_url.replace('/tree/', '/raw/', 1)
    return git_url


def downloader(download_url: str, file: str) -> tuple:
    """
    Download a CSV file and return its file path and corresponding JSON file path.

    :param file: The name of the file to download
    :return: A tuple containing path do downloaded file and output JSON file.
    """
    download_url = _convert_github_url(download_url)
    file_path = download_file(f"{download_url}/{file}", data_dir, file)
    json_path = os.path.join(output_dir, f"{file}")
    return file_path, json_path


def get_instruct(error_type: str, element_incorrect: str) -> str:
    """
    Generate instruct based on the provided error and correct, input text.

    :param error_type: Type of the error in the text.
    :param element_incorrect: Incorrect text which contains error.
    :return: Generated insturction.
    """
    instruct_lex = [
            'Popraw błędy leksykalne w podanym tekście',
            'Skoryguj wszelkie nieprawidłowości leksykalne w podanym fragmencie',
            'Znajdź i popraw błędy leksykalne',
            'Usuń niewłaściwe słownictwo z tekstu',
            'Popraw błędy leksykalne, aby tekst był poprawny',
            'W tekście występują nieprawidłowo użyte słowa, popraw je',
            'Wyszukaj i popraw wszelkie błędne wyrazy w tekście',
            'Usprawnij użycie słownictwa w podanym fragmencie',
            'Dokonaj korekty słów użytych niezgodnie z kontekstem',
            'Znajdź słowa niepasujące do kontekstu i popraw je',
    ]

    instruct_ort = [
            'Wyeliminuj błędy ortograficzne z tekstu',
            'Popraw wszelkie błędy pisowni w poniższym tekście',
            'Znajdź i napraw błędy ortograficzne',
            'Skoryguj błędy w pisowni słów',
            'Usuń wszelkie literówki i błędy w pisowni',
            'Zidentyfikuj błędy w pisowni i napraw je',
            'Sprawdź tekst pod kątem literówek i popraw je',
            'Wykryj i popraw wszelkie błędy pisowni w tekście',
            'Popraw wszelkie nieprawidłowości w pisowni słów',
            'Skoryguj błędy ortograficzne w poniższym fragmencie',
    ]

    instruct_synt = [
            'Popraw błędy składniowe w podanym tekście:',
            'Popraw błędy syntaktyczne:'
            'Skoryguj podany tekst, poprawiając błędy składniowe',
            'Usuń błędy składniowe z poniższego tekstu',
            'Poniższy tekst zawiera błędy składniowe, usuń je',
            'Pozbądź się błędów syntaktycznych z poniższego tekstu',
            'Znajdź i poraw błędy składniowe w poniższym tekście',
            'Ten tekst zawiera błędy w składni, popraw je',
            'Składnia tego tekstu zawiera błędy, pozbądź się ich',
            'Spraw aby poniższy tekst nie zawierał błędów składniowych'
    ]

    instruct_flex = [
            'Popraw błędy związane z błędną odmianą słów',
            'Dokonaj korekty błędnych form odmiany słów',
            'Znajdź i popraw niepoprawne formy słów',
            'Skoryguj błędy w odmianie przez przypadki, liczby lub osoby',
            'W tekście występują błędy fleksyjne, napraw je',
            'Ten tekst zawiera błędy związane z błędną odmianą słów, popraw je',
            'Znajdź i skoryguj błędy fleksyjne, które znajdują się w poniższym tekście',
            'Napraw błędne formy słów w danym tekście',
            'Usuń błędy związane z nieprawidłową odmianą',
            'Skoryguj błędne formy słów w podanym tekśćie.',
    ]

    instruct_punct = [
            'Popraw błędy interpunkcyjne',
            'Napraw błędy w użyciu znaków interpunkcyjnych',
            'Znajdź i usunąć błędy w stosowaniu przecinków, kropek itd',
            'Skoryguj interpunkcję w tekście',
            'Usuń wszelkie błędy w użyciu znaków interpunkcyjnych',
            'Popraw błędne użycie znaków interpunkcyjnych w tekście',
            'Dokonaj korekty interpunkcji w podanym fragmencie',
            'Znajdź i napraw błędy w stosowaniu przecinków i kropek',
            'Popraw wszelkie nieprawidłowości w użyciu znaków interpunkcyjnych',
            'Skoryguj błędy w użyciu interpunkcji, takie jak przecinki, kropki',
    ]

    if error_type == 'lex':
        instruct = random.choice(instruct_lex)
    elif error_type == 'ort':
        instruct = random.choice(instruct_ort)
    elif error_type == 'synt':
        instruct = random.choice(instruct_synt)
    elif error_type == 'flex':
        instruct = random.choice(instruct_flex)
    elif error_type == 'punct':
        instruct = random.choice(instruct_punct)

    return f"{instruct}:\n{element_incorrect}"


def get_answer(error_type: str, element_correct: str) -> str:
    """
    Generate answer based on the provided error and correct, input text.

    :param error_type: Type of the error in the text.
    :param element_correct: Correct text which does not contain error.
    :return: Generated answer.
    """
    answer_lex = [
            'Poprawna wersja tekstu, pozbawiona błędów leksykalnych',
            'Poprawiona wersja',
            'Tekst z poprawionymi błędami leksykalnymi prezentuje się następująco',
            'Naprawiono tekst, usuwając niewłaściwie użyte słowa',
            'Tekst z niewłaściwie użytym wyrazem wygląda następująco',
            'Poprawiono słownictwo w poniższym tekście. Ma on nastepującą postać',
            'Poniższy tekst zawiera już poprawnie użyte słowa',
            'Naprawiono nieprawidłowo użyte słowa',
            'Skorygowano błędne wyrazy w podanym tekście',
    ]

    answer_ort = [
            'Oto poprawiona forma tekstu, nie zawierająca błędów ortograficznych',
            'Tekst został skorygowany, eliminując błędy w pisown.',
            'Naprawiono literówki i błędy pisowni, oto poprawiony tekst',
            'Tekst pozbawiono błędów ortograficznych, oto jego poprawiona forma',
            'Tekst z poprawioną pisownią prezentuje się następująco',
            'Naprawiono błędy pisowni, oto wynik korekty',
            'Tekst po korekcie ortograficznej brzmi teraz w taki sposób',
            'Usunięto nieprawidłowe pisownie słów, oto poprawiony tekst',
            'Tekst po usunięciu literówek prezentuje się następująco',
            'Oto tekst po korekcie ortograficznej'
    ]

    answer_synt = [
            'Oto poprawiona forma tekstu, nie zawierająca błędów składniowych',
            'Tekst został skorygowany, eliminując błędy syntaktyczne',
            'Naprawiono składnię tekstu, oto jego poprawiona forma',
            'Tekst pozbawiono błędów w konstrukcji zdania, oto wynik korekty',
            'Tekst z poprawioną składnią prezentuje się następująco',
            'Naprawiono błędy w ułożeniu słów, oto poprawiony tekst',
            'Tekst po korekcie syntaktycznej brzmi teraz poprawnie',
            'Usunięto błędne ułożenie elementów w zdaniu, oto poprawiony tekst',
            'Tekst po usunięciu błędnych składni prezentuje się następująco',
            'Oto tekst po korekcie składniowej'
    ]

    answer_flex = [
            'Oto poprawiona forma tekstu, nie zawierająca błędów fleksyjnych',
            'Tekst został skorygowany, eliminując błędy w odmianie słów',
            'Naprawiono formy odmiany słów, oto poprawiony tekst',
            'Tekst pozbawiono błędnych końcówek słów, oto wynik korekty',
            'Tekst z poprawionymi błędami fleksyjnymi prezentuje się następująco',
            'Naprawiono błędne odmiany słów, oto poprawiony tekst',
            'Tekst po korekcie fleksyjnej brzmi teraz poprawnie',
            'Usunięto nieprawidłowe formy odmiany, oto poprawiony tekst',
            'Tekst po usunięciu błędnych końcówek prezentuje się następująco',
            'Oto tekst po korekcie fleksyjnej'
    ]

    answer_punct = [
            'Oto poprawiona forma tekstu, nie zawierająca błędów interpunkcyjnych',
            'Tekst został skorygowany, eliminując błędy w interpunkcji',
            'Naprawiono interpunkcję, oto poprawiony tekst',
            'Tekst pozbawiono błędnych znaków interpunkcyjnych, oto wynik korekty',
            'Tekst z poprawioną interpunkcją prezentuje się następująco',
            'Naprawiono błędy w użyciu przecinków i kropek, oto poprawiony tekst',
            'Tekst po korekcie interpunkcyjnej brzmi teraz poprawnie',
            'Usunięto błędy w stosowaniu interpunkcji, oto poprawiony tekst',
            'Tekst po usunięciu nieprawidłowej interpunkcji prezentuje się następująco',
            'Oto tekst po korekcie interpunkcyjnej'
    ]

    if error_type == 'lex':
        instruct = random.choice(answer_lex)
    elif error_type == 'ort':
        instruct = random.choice(answer_ort)
    elif error_type == 'synt':
        instruct = random.choice(answer_synt)
    elif error_type == 'flex':
        instruct = random.choice(answer_flex)
    elif error_type == 'punct':
        instruct = random.choice(answer_punct)

    return f"{instruct}:\n{element_correct}"


def create_instruction(file_path: str, json_path: str) -> None:
    """
    Create instructions in JSON format from a JSON file and save them in a JSON file.

    :param instruction: The instruction text to be included in the JSON output file.
    :param file_path: The path to the downloaded CSV file.
    :param json_path: The path to the output JSON file.
    """

    instructions = []

    with jsonlines.open(file_path, 'r') as reader_file:
        for element in reader_file:
            error_type = element['errors'][0]['type']
            instructions.append({
                    "instruct": get_instruct(error_type, element['incorrect']),
                    "output": get_answer(error_type, element['correct']),
                    "source_name": SOURCE_NAME,
                    "source_url": SOURCE_URL,
                    "source_description": SOURCE_DESCRIPTION,
                    "script_name": script_name
            })

    # Randomly change the order of the elements
    random.shuffle(instructions)

    # Write prepared instructions to the output file
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    URL = 'https://github.com/Ermlab/polish-gec-datasets/tree/main'
    FILE = 'human_annotators_common_errors_10K.jsonl'
    file_path, json_path = downloader(URL, FILE)
    create_instruction(file_path, json_path)
