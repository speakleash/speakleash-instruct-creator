# speakleash-instruct-creator

Create a script that will create a json with instructions and place it in the output folder (e.g. allegro-summarization.py). Then run merge-files.py. The script will merge all the json files into one big json file


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

Plan list:
## Dataset number
(person's initials responsible for dataset | work status | dataset url | dataset file name)

# Plan
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
IC - IN PROGRESS
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

##POMYSŁY
https://huggingface.co/datasets/WiktorS/polish-news
Można generować tytułu i abstrakty na podstawie tekstu


https://huggingface.co/datasets/ptaszynski/PolishCyberbullyingDataset
https://huggingface.co/datasets/Paul/hatecheck-polish
Do wykrywania mowy-nienawiści


https://huggingface.co/datasets/klima7/polish-tales
Bajki wyciągnąłbym kilka kluczowych rzeczowników i powiedział opowiedz mi bajkę o kocie. Trochę zabawy

https://huggingface.co/datasets/sepidmnorozy/Polish_sentiment



