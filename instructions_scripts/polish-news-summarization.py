"""Instructions creator based on WiktorS/polish-news dataset."""
from datasets import load_dataset
import os
import random
import json
import pandas as pd

try:
    from utils.functions import get_dir_path
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None


SCRIPT_NAME = os.path.basename(__file__)
SOURCE_NAME = SCRIPT_NAME.replace(".py", "")
SOURCE_URL = "https://huggingface.co/datasets/WiktorS/polish-news"
SOURCE_DESCRIPTION = "This dataset contains more than 250k articles obtained from polish news site tvp.info.pl. Main purpouse of collecting the data was to create a transformer-based model for text summarization."

OUTPUT_DIR = 'output'


def create_dirs() -> None:
    """
    Create storage directories for both downloaded dataset and created JSON instructions file.
    """
    # Get the path to the currently executing python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    output_dir = get_dir_path(OUTPUT_DIR) or os.path.join(base_dir, OUTPUT_DIR)

    # Create directory (if it does not exist yet) for created instructions json files
    os.makedirs(output_dir, exist_ok=True)
    

def download_dataset(dataset: str = "WiktorS/polish-news", split:str = "train") -> pd.DataFrame:
    """
    Download and load a dataset to the frame.

    :param dataset: The name or path of the dataset.
    :param subset: The subset or category of the dataset to download.
    :param split: The dataset split to download (e.g., "train", "validation").
    :return: A Pandas DataFrame containing the downloaded dataset.
    """
    dataset = load_dataset(dataset, split=split)
    
    dataset.set_format('pandas')
    frame = dataset[:]
    
    return frame 


def create_instruction(frame: pd.DataFrame) -> None:
    """
    Create instructions in JSON format from a dataframe and save them in a JSON file.

    :param frame: pandas dataframe with data..
    :param json_path: The path to the output JSON file.
    """
    INSTRUCT_LIST = [
        "Napisz skróconą wersję podanego tekstu.",
        "Przygotuj streszczenie dla tego tekstu.",
        "Dokonaj streszczenia z podanego materiału.",
        "Streść poniższy tekst.",
        "Zrób streszczenie.",
        "Przygotuj skrót informacji z podanego tekstu."
    ]
    
    instructions = []

    for index, row in frame.iterrows():

        instructions.append(
             {
                "instruct": random.choice(INSTRUCT_LIST), 
                 "input": row['content'], 
                 "output": row['headline'], 
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
