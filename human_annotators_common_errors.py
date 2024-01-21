"""Instructions creator based on human_annotators_common_errors"""
import json
import os
import random

import jsonlines

from utils.functions import download_file

# Mandatory dataset data for json objects
SOURCE_NAME = f"{os.path.basename(__file__).replace('.py', '')}"
SOURCE_DESCRIPTION = 'Zbiór danych zawierający zbiory testowe do korekcji błędów ortograficznych. Dataset składa się ' \
                     'ze zdań prawidłowych, nieprawidłowych oraz wskazań błędów ortograficznych. Autorem zestawu ' \
                     'danych jest Ermlab'

SOURCE_URL = 'https://github.com/Ermlab/polish-gec-datasets/tree/main/'
FILE = 'human_annotators_common_errors_10K.jsonl'
DATA_DIR = 'data'
OUTPUT_DIR = 'output'
SCRIPT_NAME = os.path.basename(__file__)


def downloader(download_url: str, file: str) -> tuple:
    """
    Download dataset file, return its file path and corresponding JSON file path.

    :param download_url: Url address of the dataset file.
    :param file: The name of the dataset file to be downloaded.
    :return: A tuple containing path to downloaded file and output JSON file.
    """
    download_url = _convert_github_url(download_url)
    file_path = download_file(f"{download_url}/{file}", DATA_DIR, file)
    json_path = os.path.join(OUTPUT_DIR, f"{file}")
    return file_path, json_path


def get_instruct(error_type: str, element_incorrect: str) -> str:
    """
    Generate instruct based on the provided error and correct, input text.

    :param error_type: Type of the error in the text.
    :param element_incorrect: Incorrect text which contains error.
    :return: Generated instruction.
    """
    error_map = {
            'lex': [
                    'Popraw błędy leksykalne w podanym tekście',
                    'Skoryguj wszelkie nieprawidłowości leksykalne w podanym fragmencie',
                    'Znajdź i popraw błędy leksykalne',
                    'Usuń niewłaściwe słownictwo z tekstu',
                    'Popraw błędy leksykalne, aby tekst był poprawny',
                    'W tekście występują nieprawidłowo użyte słowa, popraw je',
                    'Wyszukaj i popraw wszelkie błędne wyrazy w tekście',
                    'Dostosuj użycie słownictwa w podanym fragmencie',
                    'Dokonaj korekty słów użytych niezgodnie z kontekstem',
                    'Znajdź słowa niepasujące do kontekstu i popraw je',
            ],
            'ort': [
                    'Wyeliminuj błędy ortograficzne z tekstu',
                    'Popraw wszelkie błędy pisowni w poniższym tekście',
                    'Znajdź i napraw błędy ortograficzne',
                    'Skoryguj błędy w pisowni słów',
                    'Usuń wszelkie literówki i błędy w pisowni',
                    'Zidentyfikuj błędy w pisowni i napraw je',
                    'Sprawdź tekst pod kątem literówek i popraw je',
                    'Wykryj i popraw wszelkie błędy pisowni w tekście',
                    'Popraw wszelkie nieprawidłowości w pisowni',
                    'Skoryguj błędy ortograficzne w poniższym fragmencie',
            ],
            'synt': [
                    'Popraw błędy składniowe w podanym tekście:',
                    'Popraw błędy syntaktyczne',
                    'Skoryguj podany tekst, poprawiając błędy składniowe',
                    'Usuń błędy składniowe z poniższego tekstu',
                    'Poniższy tekst zawiera błędy składniowe, usuń je',
                    'Pozbądź się błędów syntaktycznych z poniższego tekstu',
                    'Znajdź i popraw błędy składniowe w poniższym tekście',
                    'Ten tekst zawiera błędy w składni, popraw je',
                    'Składnia tego tekstu zawiera błędy, pozbądź się ich',
                    'Spraw, aby poniższy tekst nie zawierał błędów składniowych'
            ],
            'flex': [
                    'Popraw błędy związane z błędną odmianą słów',
                    'Dokonaj korekty błędnych form odmiany',
                    'Znajdź i popraw niepoprawne formy słów',
                    'Skoryguj błędy w odmianie przez przypadki, liczby, rodzaje lub osoby',
                    'W tekście występują błędy fleksyjne, napraw je',
                    'Ten tekst zawiera błędy związane z błędną odmianą słów, popraw je',
                    'Znajdź i skoryguj błędy fleksyjne, które znajdują się w poniższym tekście',
                    'Napraw błędne formy słów w danym tekście',
                    'Usuń błędy związane z nieprawidłową odmianą',
                    'Skoryguj błędne formy słów w podanym tekście',
            ],
            'punct': [
                    'Popraw błędy interpunkcyjne',
                    'Napraw błędy w użyciu znaków interpunkcyjnych',
                    'Znajdź i usuń błędy w stosowaniu przecinków, kropek itd.',
                    'Skoryguj interpunkcję w tekście',
                    'Usuń wszelkie błędy w użyciu znaków interpunkcyjnych',
                    'Popraw błędne użycie znaków interpunkcyjnych w tekście',
                    'Dokonaj korekty interpunkcji w podanym fragmencie',
                    'Znajdź i napraw błędy w stosowaniu przecinków i kropek',
                    'Popraw wszelkie nieprawidłowości w użyciu znaków interpunkcyjnych',
                    'Skoryguj błędy w użyciu interpunkcji, takie jak przecinki czy kropki',
            ]
    }

    return f"{random.choice(error_map.get(error_type))}:\n{element_incorrect}"


def get_answer(error_type: str, element_correct: str) -> str:
    """
    Generate answer based on the provided error and correct, input text.

    :param error_type: Type of the error in the text.
    :param element_correct: Correct text which does not contain error.
    :return: Generated answer.
    """
    answer_map = {
            'lex': [
                    'Poprawna wersja tekstu, pozbawiona błędów leksykalnych',
                    'Poprawiona wersja',
                    'Tekst z poprawionymi błędami leksykalnymi prezentuje się następująco',
                    'Naprawiono tekst, usuwając niewłaściwie użyte słowa',
                    'Tekst z niewłaściwie użytym wyrazem wygląda następująco',
                    'Poprawiono słownictwo w poniższym tekście. Ma on następującą postać',
                    'Poniższy tekst zawiera już poprawnie użyte słowa',
                    'Naprawiono nieprawidłowo użyte słowa',
                    'Skorygowano błędne wyrazy w podanym tekście',
            ],
            'ort': [
                    'Oto poprawiona forma tekstu, niezawierająca błędów ortograficznych',
                    'Tekst poprawiono, eliminując błędy w pisowni',
                    'Naprawiono literówki i błędy pisowni, oto poprawiony tekst',
                    'Tekst pozbawiono błędów ortograficznych, oto jego poprawiona forma',
                    'Tekst z poprawioną pisownią prezentuje się następująco',
                    'Naprawiono błędy pisowni, oto wynik korekty',
                    'Tekst po korekcie ortograficznej brzmi teraz w taki sposób',
                    'Usunięto nieprawidłową pisownię, oto poprawiony tekst',
                    'Tekst po usunięciu literówek prezentuje się następująco',
                    'Oto tekst po korekcie ortograficznej'
            ],
            'synt': [
                    'Oto poprawiona forma tekstu, niezawierająca błędów składniowych',
                    'Tekst poprawiono, eliminując błędy syntaktyczne',
                    'Naprawiono składnię tekstu, oto jego poprawiona forma',
                    'Tekst pozbawiono błędów w konstrukcji zdania, oto wynik korekty',
                    'Tekst z poprawioną składnią prezentuje się następująco',
                    'Naprawiono błędy szyku, oto poprawiony tekst',
                    'Tekst po korekcie syntaktycznej brzmi teraz poprawnie',
                    'Usunięto błędny szyk elementów w zdaniu, oto poprawiony tekst',
                    'Tekst po usunięciu błędów w składni prezentuje się następująco',
                    'Oto tekst po korekcie składniowej'
            ],
            'flex': [
                    'Oto poprawiona forma tekstu, niezawierająca błędów fleksyjnych',
                    'Tekst poprawiono, eliminując błędy w odmianie słów',
                    'Naprawiono formy gramatyczne, oto poprawiony tekst',
                    'Tekst pozbawiono błędnych końcówek słów, oto wynik korekty',
                    'Tekst z poprawionymi błędami fleksyjnymi prezentuje się następująco',
                    'Naprawiono błędną odmianę, oto poprawiony tekst',
                    'Tekst po korekcie fleksyjnej brzmi teraz poprawnie',
                    'Usunięto nieprawidłowe formy odmiany, oto poprawiony tekst',
                    'Tekst po usunięciu błędnych końcówek prezentuje się następująco',
                    'Oto tekst po korekcie fleksyjnej'
            ],
            'punct': [
                    'Oto poprawiona forma tekstu, niezawierająca błędów interpunkcyjnych',
                    'Tekst poprawiono, eliminując błędy w interpunkcji',
                    'Naprawiono interpunkcję, oto poprawiony tekst',
                    'Tekst pozbawiono błędnych znaków interpunkcyjnych, oto wynik korekty',
                    'Tekst z poprawioną interpunkcją prezentuje się następująco',
                    'Naprawiono błędy w użyciu przecinków i kropek, oto poprawiony tekst',
                    'Tekst po korekcie interpunkcyjnej brzmi teraz poprawnie',
                    'Usunięto błędy w stosowaniu interpunkcji, oto poprawiony tekst',
                    'Tekst po usunięciu nieprawidłowej interpunkcji prezentuje się następująco',
                    'Oto tekst po korekcie interpunkcyjnej'
            ]
    }

    return f"{random.choice(answer_map.get(error_type))}:\n{element_correct}"


def crate_dirs() -> None:
    """
    Create storage directories for both downloaded dataset and created JSON instructions file.
    """
    # Get the path to the currently executing python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define directories name for downloaded and output files
    data_dir = os.path.join(base_dir, DATA_DIR)
    output_dir = os.path.join(base_dir, OUTPUT_DIR)

    # Create directory for downloading data from server / link
    os.makedirs(data_dir, exist_ok=True)

    # Create directory (if it does not exist yet) for created instructions json files
    os.makedirs(output_dir, exist_ok=True)


def _convert_github_url(git_url: str) -> str:
    """
    Converts provided github url to downloadable url for raw format files. If is not from github or already
    represents raw file, it returns unchanged link.

    :param git_url: Link to the github repository file
    :return: Link to the github repository in raw format, if conditions are met.
    """
    if 'github' in git_url and '/tree/' in git_url and 'raw' not in git_url:
        return git_url.replace('/tree/', '/raw/', 1)
    return git_url


def create_instruction(file_path: str, json_path: str) -> None:
    """
    Create instructions in JSON format from a JSON file and save them in a JSON file.

    :param file_path: The path to the downloaded CSV file.
    :param json_path: The path to the output JSON file.
    """

    instructions = []

    try:
        with jsonlines.open(file_path, 'r') as reader_file:
            for element in reader_file:
                error_type = element['errors'][0]['type']
                instructions.append({
                        "instruct": get_instruct(error_type, element['incorrect']),
                        "output": get_answer(error_type, element['correct']),
                        "source_name": SOURCE_NAME,
                        "source_url": SOURCE_URL,
                        "source_description": SOURCE_DESCRIPTION,
                        "script_name": SCRIPT_NAME
                })
    except (FileNotFoundError, jsonlines.Error) as e:
        print(f"Error reading file {file_path}: {e}")

    # Randomly change the order of the elements
    random.shuffle(instructions)

    # Write prepared instructions to the output file
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    crate_dirs()
    file_path, json_path = downloader(SOURCE_URL, FILE)
    create_instruction(file_path, json_path)
