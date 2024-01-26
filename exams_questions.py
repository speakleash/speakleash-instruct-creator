"""Instructions creator based on EXAMS dataset."""
from datasets import load_dataset
import os
import random
import json
import pandas as pd


SCRIPT_NAME = os.path.basename(__file__)
SOURCE_NAME = SCRIPT_NAME.replace(".py", "")
SOURCE_URL = "https://huggingface.co/datasets/exams"
SOURCE_DESCRIPTION = "EXAMS is a benchmark dataset for multilingual and cross-lingual question answering from high school examinations. It consists of more than 24,000 high-quality high school exam questions."

OUTPUT_DIR = 'output'


def create_dirs() -> None:
    """
    Create storage directories for both downloaded dataset and created JSON instructions file.
    """
    # Get the path to the currently executing python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(base_dir, OUTPUT_DIR)

    # Create directory (if it does not exist yet) for created instructions json files
    os.makedirs(output_dir, exist_ok=True)
    

def download_dataset(dataset: str = "exams", subset:str = "crosslingual_pl", split:str = "train") -> pd.DataFrame:
    """
    Download and load a dataset to the frame.

    :param dataset: The name or path of the dataset.
    :param subset: The subset or category of the dataset to download.
    :param split: The dataset split to download (e.g., "train", "validation").
    :return: A Pandas DataFrame containing the downloaded dataset.
    """
    dataset = load_dataset(dataset, subset, split=split)
    
    dataset.set_format('pandas')
    frame = dataset[:]
    
    return frame 


def _parse_dataset_row(row):
    """
    Parse a row from the dataset and extract input and output.

    :param row: A row from the dataset.
    :return: A tuple containing input and output strings.
    """
    question = row['question']['stem']
    choices = row['question']['choices']['text']
    choicesKey = row['question']['choices']['label']
    answerKey = row['answerKey']

    answer = {}
    input = question

    for (choice, key) in zip(choices, choicesKey):
        answer[key] = choice
        input = input + "\n" + key + ". " + choice

    output = answerKey + ". " + answer[answerKey]
    return input, output


def create_instruction(frame: pd.DataFrame) -> None:
    """
    Create instructions in JSON format from a JSON file and save them in a JSON file.

    :param frame: pandas dataframe with data..
    :param json_path: The path to the output JSON file.
    """
    INSTRUCT_LIST = [
        "Podaj odpowiedź na poniższe pytanie.", 
        "Jaka jest prawidłowa odpowiedź?",
        "Rozwiąż test i wybierz dobrą odpowiedź.",
        "Wybierz właściwą odpowiedź.",
        "Udziel odpowiedzi na pytanie.",
    ]
    
    instructions = []

    for index, row in frame.iterrows():
        input, output = _parse_dataset_row(row)
        instructions.append(
             {
                "instruct": random.choice(INSTRUCT_LIST), 
                 "input": input, 
                 "output": output, 
                 "source_name": SOURCE_NAME, 
                 "source_url": SOURCE_URL, 
                 "source_description": SOURCE_DESCRIPTION, 
                 "script_name": SCRIPT_NAME
            } 

        )

    # Randomly change the order of the elements
    random.shuffle(instructions)

    output_path = os.path.join(OUTPUT_DIR, SCRIPT_NAME.replace(".py",".json"))
    
    # Write prepared instructions to the output file
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    create_dirs()
    frame = download_dataset()
    create_instruction(frame)
