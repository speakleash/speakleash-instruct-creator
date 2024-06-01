Speakleash training and tuning datasets
----------------------

The repository consists of three sections of specific datasets::
- conversations
- functions
- instructions

Each section will include datasets created:
- fully automated by scripts
- manually, scripts with the help of a human
- samples which will show 3 records of what was created


Generate instruction JSON files using implemented instruction scripts.

#
<details>
<summary>Released instruction version: 2024_03_07_v0_0_13 (expandable list with download links):</summary><br>

All generated instruction JSON zip files:<br>
http://instruct.speakleash.space/instructions_not_merged/instructions_not_merged_2024_03_07_v0_0_13.zip

Merged instruction JSON files into one final zipfile:<br>
http://instruct.speakleash.space/instructions_merged_and_stats/instructions_merged_and_stats_2024_03_07_v0_0_13.zip

Merged instruction JSON file files:<br>
http://instruct.speakleash.space/speakleash_pl_instructions_2024_03_07_v0_0_13.jsonl

Merged instruction JSON file files (Alpaca format):<br>
http://instruct.speakleash.space/speakleash_pl_instructions_alpaca_2024_03_07_v0_0_13.jsonl

Or using terminal commands:<br>
- For Linux:<br>
`wget` 

- For Windows:<br>
`curl` 
</details>

## Introduction:
To contribute, clone this repository and add a new instructions script (e.g., ```allegro-summarization.py```) to the ```instructions_scripts``` directory.

Instruction files are generated in the ```output``` directory.

External datasets are downloaded to the ```data``` directory.

Internal datasets from the ```Speakleash``` package are downloaded separately to the ```data_speakleash``` directory. This temporary solution
is implemented due to the current version of the ```Speakleash``` package. The ```manifests``` files are downloaded automatically to the same
directory as ```datasets```, so spearating both directories was done for better readability. This functionality was done with the purpose but
we are working on some changes, described in this ```issue```:
https://github.com/speakleash/speakleash/issues/10


## Generate files
To generate one final instructions JSON file, merge them using the ```merge_files.py``` script. It will be created in the
directory called ```instructions_merged_and_stats``` along with statistical files describing the instructions data.
To update instruction samples, run the ```generate_samples.py``` script. It will generate JSON files with three records each.
### Important information:
```sentiment_detection.py``` -> requires HuggingFace token.<br>
```orca_math_create_english_docx.py``` with ```orca_math_create_json_from_docx.py``` -> the scripts need to be self-translated in an external service,
so they are not included in merge_files.py. More information inside these scripts.
```speakleash_forums_questions.py``` -> if installed requirements won't work, follow the steps included in this documentation: https://github.com/ZILiAT-NASK/StyloMetrix
If you are facing problems with dependencies, execute manual installation of the following libraries:
```pip install http://mozart.ipipan.waw.pl/~rtuora/spacy/pl_nask-0.0.7.tar.gz```<br>
```pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.7.0/pl_core_news_md-3.7.0-py3-none-any.whl```<br>
It is a temporary solution but will work.

## Mandatory instructions fields
Each JSON object with an instruction should containt mandatory fields like:
```json
{
    ...
    "source_name": "os.path.basename(file).replace('.py', '') + ' TODO'",
    "source_url": "https:// - TODO",
    "source_description": "TODO",
    "script_name": "os.path.basename(file)"
}
```
<details>
<summary>Instructions list to do (expandable list):</summary><br>

## Dataset number
(person's initials responsible for dataset | work status | dataset url | dataset file name)

## Plan
## 1 
SK - DONE
https://huggingface.co/datasets/allegro/summarization-polish-summaries-corpus
allegro-summarization-polish-summaries-corpus.csv

## 2
SK - DONE
https://huggingface.co/datasets/allegro/summarization-allegro-articles
allegro-summarization-allegro-articles-body-lead-to-title.csv
allegro-summarization-allegro-articles-body-to-lead.csv
allegro-summarization-allegro-articles-lead-to-title.csv

## 3
MF - DONE
https://huggingface.co/datasets/clarin-pl/poquad
poquad-train.json

## 4
IC - DONE
https://huggingface.co/datasets/ipipan/polqa
ipipan_polqa.csv

## 5
IC - IN PROGRESS (2 datasets done)<br>
https://github.com/Ermlab/polish-gec-datasets
human_annotators_common_errors_10K.jsonl

## 6
MF - DONE
https://huggingface.co/datasets/piotr-rybak/legal-questions/tree/main/data
piotr-rybak_legal-questions.jsonl

## 7
PK - DONE
https://www.amazon.science/blog/amazon-releases-51-language-dataset-for-language-understanding
Amazaon Massive Dataset, v1.1
massive_amazon.jsonl

## 8
MF - DONE
https://huggingface.co/datasets/allegro/klej-dyk

## 9
MF - DONE
https://github.com/speakleash/speakleash/tree/main
Q&A extraction from SpeakLeash datasets (selected forums)
"forum_forum_wszystkodlawnetrza_pl_corpus",
"forum_ezoforum_pl_corpus"

## 10
IC - IN PROGRESS
https://dl.fbaipublicfiles.com/fasttext/word-analogies/questions-words-pl.txt
Polish Analogy Dataset

## 11
MF - DONE
https://github.com/ZILiAT-NASK/BAN-PL/data/BAN-PL_1.zip
BAN-PL.csv


## POMYSŁY
https://huggingface.co/datasets/WiktorS/polish-news
Można generować tytułu i abstrakty na podstawie tekstu


https://huggingface.co/datasets/ptaszynski/PolishCyberbullyingDataset
https://huggingface.co/datasets/Paul/hatecheck-polish
Do wykrywania mowy-nienawiści


https://huggingface.co/datasets/klima7/polish-tales
Bajki wyciągnąłbym kilka kluczowych rzeczowników i powiedział opowiedz mi bajkę o kocie. Trochę zabawy

https://huggingface.co/datasets/sepidmnorozy/Polish_sentiment

</details>
