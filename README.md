# speakleash-instruct-creator

Create a script that will create a json with instructions and place it in the output folder (e.g. allegro-summarization.py). Then run merge-files.py. The script will merge all the json files into one big json file

Template:
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
IC - TODO
https://github.com/Ermlab/polish-gec-datasets
human_annotators_common_errors_10K.jsonl

## 6
MF - DONE
https://huggingface.co/datasets/piotr-rybak/legal-questions/tree/main/data
piotr-rybak_legal-questions.jsonl

## 7
? - TODO
https://www.amazon.science/blog/amazon-releases-51-language-dataset-for-language-understanding
Amazaon Massive Dataset
massive_amazon.jsonl

## 8
MF - DONE
https://huggingface.co/datasets/allegro/klej-dyk

## 9
MF - TODO
Q&A extraction from SpeakLeash datasets (selected forums)
