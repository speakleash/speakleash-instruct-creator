"""
Instructions creator based on polqa dataset
"""

import json
import os
import random
import re
from typing import Set

from tqdm import tqdm
import pandas as pd


try:
    from utils.functions import download_file, get_dir_path
except ImportError as e:
    print(f"Error: {e}")

    def get_dir_path(_):
        return None


QUOTES = [("'", "'"), ('"', '"'), ("<<", ">>")]

POSITIVE_ANSWERS = [
    "tak, kontekst odpowiada na to pytanie",
    "tak, odpowiedź znajduje się w podanym kontekście",
    "tak, odpowiedź występuje w danym kontekście",
    "tak, odpowiedź jest zawarta w kontekście",
    "tak, treść kontekstu obejmuje odpowiedź",
    "tak, kontekst dostarcza odpowiedzi na pytanie",
    "tak, odpowiedź jest ukryta w kontekście",
    "tak, w kontekście mieści się odpowiedź na pytanie",
    "tak, kontekst zawiera odpowiedź",
    "tak, odpowiedź jest zawarta w treści",
    "tak, wszystko jest wyjaśnione w tekście",
]


NEGATIVE_ANSWERS = [
    "nie, kontekst nie odpowiada na to pytanie",
    "nie, odpowiedź nie znajduje się w podanym kontekście",
    "nie, odpowiedź nie występuje w danym kontekście",
    "nie, odpowiedź nie jest zawarta w kontekście",
    "nie, treść kontekstu nie obejmuje odpowiedzi",
    "nie, kontekst nie dostarcza odpowiedzi na pytanie",
    "nie, odpowiedź nie jest ukryta w podanej treści",
    "nie, w kontekście nie znajduje się odpowiedź na pytanie",
    "nie, kontekst nie zawiera odpowiedzi",
    "nie, odpowiedź nie jest zawarta w treści",
    "nie, wszystko nie jest wyjaśnione w tekście",
]

INSTRUCT_TEMPLATES = [
    "Czy tekst poniżej zawiera odpowiedź na pytanie {question}?",
    "Czy odpowiedź na pytanie {question} jest zawarta w poniższym tekście?",
    "Czy mogę znaleźć odpowiedź na pytanie {question} w następującym kontekście?",
    "Czy poniższy tekst odpowiada na pytanie {question}?",
    "Czy treść poniżej zawiera odpowiedź na pytanie {question}?",
    "Czy w materiale poniżej mogę znaleźć odpowiedź na pytanie {question}?",
    "Czy poniższy tekst zawiera informacje stanowiące odpowiedź na pytanie {question}?",
    "Czy w kontekście poniżej zawarta jest odpowiedź na pytanie {question}?",
    "Czy poniższe treści zawierają odpowiedź na pytanie {question}?",
    "Czy odpowiedź na pytanie {question} jest w tekście poniżej?",
    "Czy mogę odnaleźć odpowiedź na pytanie {question} w tekście poniżej?",
]

# Mandatory dataset information fields for json objects
source_name = f"ipipan-{os.path.basename(__file__).replace('.py', '')}"
source_url = "https://huggingface.co/datasets/ipipan/polqa"
source_description = (
    "Pary, dla których input to pytanie o to czy w danym "
    "kontekście (passage) znajduje się odpowiedź na pytanie (question). Autor bazowego zestawu danych to Instytu Podstaw "
    "Informatyki Polskiej Akademii Nauk."
)
script_name = os.path.basename(__file__)

# Get the path to the currently executing python script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define directories name for downloaded and output files
data_dir = get_dir_path("data") or os.path.join(base_dir, "data")
output_dir = get_dir_path("output") or os.path.join(base_dir, "output")

# Create directory for downloading data from server / link
os.makedirs(data_dir, exist_ok=True)

# Create directory (if does not exists) for created instructions json files
os.makedirs(output_dir, exist_ok=True)


def enquote_question(question: str) -> str:
    left, right = random.choice(QUOTES)
    return left + question + right


def downloader(file: str) -> tuple:
    """
    Download a CSV file and return its file path and corresponding JSON file path.

    :param file: The name of the file to download
    :return: A tuple containing path do downloaded file and output JSON file.
    """
    file_path = download_file(
        f"https://huggingface.co/datasets/ipipan/polqa/resolve/main/data/{file}.csv?download=true",
        data_dir,
        f"ipipan_polqa_{file}.csv ",
    )
    json_path = os.path.join(output_dir, f"ipipan_polqa_context_has_answer_{file}.json")
    return file_path, json_path


def text_cleaner(text: str) -> str:
    """
    Clean string with regex formula.

    :param text: Provided text for cleaning.
    :return: Cleaned text.
    """
    text = re.sub(r"\[\d+\]\.$", "", text)
    return (
        text.replace("Ŝ", "ż")
        .replace("„", '"')
        .replace("”", '"')
        .replace(",,", '"')
        .replace("''", '"')
        .replace(" • ", " * ")
        .replace("×", "*")
        .replace("·", "*")
        .replace("–", "-")
        .replace("\r", "")
    )


def create_instruction(
    file_path: str, json_path: str, accepted_relevance: Set[int]
) -> None:
    """
    Create instructions in JSON format from a CSV file and save them in a JSON file.

    :param instruction: The instruction text to be included in the JSON output file..
    :param file_path: The path to the downloaded CSV file.
    :param json_path: The path to the output JSON file.
    """

    instructions = []
    added_pairs = set()
    i = 0
    data = pd.read_csv(file_path, usecols=["question", "passage_text", "relevant"])
    # Iterate through rows and pick defined ones
    for index, row in tqdm(
        data.iterrows(), desc="Producing instructions...", total=len(data)
    ):
        relevant = row["relevant"]
        input = text_cleaner(row["passage_text"])
        pair = (row["question"], input)

        if (pair in added_pairs) or (relevant not in accepted_relevance):
            continue

        instruct_template = INSTRUCT_TEMPLATES[i % len(INSTRUCT_TEMPLATES)]
        instruct = instruct_template.format(
            question=enquote_question(text_cleaner(row["question"]))
        )

        output = (
            POSITIVE_ANSWERS[i % len(POSITIVE_ANSWERS)]
            if relevant
            else NEGATIVE_ANSWERS[i % len(NEGATIVE_ANSWERS)]
        ) + random.choice(
            ["", "."]
        )  # sometimes add dot at the end

        added_pairs.add(pair)
        instructions.append(
            {
                "instruct": instruct,
                "input": input,
                "output": output,
                "source_name": source_name,
                "source_url": source_url,
                "source_description": source_description,
                "script_name": script_name,
                "positive": relevant,
            }
        )
        i += 1
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    files = ["train", "valid"]
    target_accepted_relevance = {
        0,  # positive answer, passage OK
        1,  # negative, passage not OK, does not answer the question
    }
    for file in files:
        file_path, json_path = downloader(file)
        create_instruction(file_path, json_path, target_accepted_relevance)