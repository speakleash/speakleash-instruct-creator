import json
import numpy as np
import os
import pandas as pd
import regex as re
import stylo_metrix as sm
import torch

from langdetect import detect
from speakleash import Speakleash
from transformers import AutoTokenizer, AutoModelForSequenceClassification

try:
    from utils.functions import get_dir_path, create_directory
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None


source_name = os.path.basename(__file__).replace(".py", "") + " speakleash_forums_questions"
script_name = os.path.basename(__file__)
source_url = "skrypt długo się generuje, paczka przesłana ręcznie"
source_description = "Dokumenty z forów internetowych o jakości HIGH, wyodrębniono z nich automatycznie" \
                     "pary pytania - odpowiedź (forum_forum_wszystkodlawnetrza_pl_corpus,forum_ezoforum_pl_corpus)."
PROJECTS = [
    "forum_forum_wszystkodlawnetrza_pl_corpus",
    "forum_ezoforum_pl_corpus",
]

LIMIT = 4000

TOKENIZER = AutoTokenizer.from_pretrained("cross-encoder/ms-marco-MiniLM-L-6-v2")
MODEL = AutoModelForSequenceClassification.from_pretrained("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Regex patterns for url address, html code samples, e-mail address, mentions/hashtags, CamelCase etc.
code_pattern = re.compile(r"(<.*?>)|({\S*})|(&\S*;)")
url_pattern = re.compile(r"(http|https)://\S+|www\.\S+")
e_mail_pattern = re.compile(r"(\S+@\S+\.\S+)")
other_pattern = re.compile(r"([#@]\S+)")
author_pattern = re.compile(r"(\d{1,2}\s\w{3}\s\d{1,2}:\d{2}[^:]*:)|(\S+\snapisał\(a\):)|\n")
symbol_pattern = re.compile(r"[$&\*=#@/]+")
space_pattern = re.compile(r"\s+")
camel_pattern = re.compile(r"([a-z0-9])([A-Z])")


# Downloading data and creating a DataFrame
def get_frame():
    texts = []
    for p in PROJECTS:
        for d in sl.datasets:
            if d.name == p:
                counter = 0
                for doc, meta in d.ext_data:
                    if detect(doc) == "pl" and meta["quality"] == "HIGH":
                        counter = counter + 1
                        texts.append(doc)
                        if counter > LIMIT:
                            break
    return pd.DataFrame({'text': texts})


# Data cleaning (customized)
def clean_forum(forum_input):  # for forums
    forum_input = re.sub(code_pattern, '<code>', str(forum_input))
    forum_input = re.sub(url_pattern, '<url>', forum_input)
    forum_input = re.sub(e_mail_pattern, '<e-mail>', forum_input)
    forum_input = re.sub(other_pattern, '', forum_input)
    forum_input = re.sub(symbol_pattern, '', forum_input)
    forum_input = re.sub(author_pattern, '<dialog>', forum_input)
    forum_input = re.sub(space_pattern, ' ', forum_input)
    cl_text = re.sub(camel_pattern, r"\1 \2", forum_input)
    return cl_text


# Calculating metrics for syntax specification for text snippets.
# Two metrics are taken into account:
# 1. 'SY_S_DE' (words in a declarative sequence)
# 2. 'SY_S_IN' (words in an interrogative sequence)
# (source: https://github.com/ZILiAT-NASK/StyloMetrix)
def get_stylo(df):
    df.text = df.text.apply(lambda x: x.split('<dialog>'))
    metrics = sm.get_all_metrics('pl')
    to_analyse = [metrics[155], metrics[157]]
    stylo = sm.StyloMetrix('pl', metrics=to_analyse)
    metrics_list = []
    for t in df.text.values:
        metrics_list.append(stylo.transform(t))
    return metrics_list


# Filtering metrics results
def get_qa(metrics_list):
    questions = dict()
    answers = dict()
    for mi, m in enumerate(metrics_list):
        a = m['text'].loc[m['SY_S_DE'] > 0.9].index.tolist()
        q = m['text'].loc[m['SY_S_IN'] > 0.9].index.tolist()
        if len(m.text.iloc[q].values) > 1 and len(m.text.iloc[a].values) > 1:
            questions[mi] = m.text.iloc[q].values.tolist()
            answers[mi] = m.text.iloc[a].values.tolist()
        else:
            continue
    qa_df = pd.DataFrame(columns=['input', 'output'])
    qa_df['input'] = questions.values()
    qa_df['output'] = answers.values()
    qa_df["instruct"] = "Odpowiedz na pytanie."
    return qa_df


# Matching questions and answers with a cross-encoder (https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2)
def get_pairs(qa_df):
    pair_list = []
    for inst, qr, an in qa_df[["instruct", "input", "output"]].values:
        for q in range(len(qr)):
            features = TOKENIZER(
                [qr[q]] * len(an),
                an,
                padding=True,
                truncation=True,
                return_tensors="pt"
            )
            MODEL.eval()
            with torch.no_grad():
                scores = MODEL(**features).logits
                pair_list.append({
                        "instruct": inst,
                        "input": qr[q],
                        "output": an[np.argmax(scores)],
                        "source_name": source_name,
                        "source_url": source_url,
                        "source_description": source_description,
                        "script_name": script_name
                })
    return pair_list


if __name__ == '__main__':
    base_dir = "./"
    replicate_to = get_dir_path("data_speakleash") or os.path.join(base_dir, "data_speakleash")
    output_dir = get_dir_path("output") or os.path.join(base_dir, "output")
    create_directory(output_dir)
    sl = Speakleash(replicate_to)
    df1 = get_frame()
    df1['text'] = df1['text'].apply(clean_forum)
    metrics_list1 = get_stylo(df1)
    qa_df1 = get_qa(metrics_list1)
    instructions = get_pairs(qa_df1)

    with open(f"{output_dir}/speakleash_forums.json", "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)
