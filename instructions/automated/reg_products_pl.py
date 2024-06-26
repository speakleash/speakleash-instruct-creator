import datetime
import os
import sys
import requests
import json, shutil
import pandas as pd
from unidecode import unidecode
from goose3 import Goose
from collections import defaultdict
import re 
from urllib.parse import urlparse

# Add the 'utils' folder to the sys.path
utils_path = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'utils')
sys.path.append(utils_path)


def get_request(payload, WEB_NO: int, WEB_OFFSET: int):
    """
    Sends a POST request to the Google Serper API with the given payload.

    Args:
        payload (str): The payload to be sent in the request.
        WEB_NO (int): The number of search results to fetch.
        WEB_OFFSET (int): The number of additional results to fetch.

    Returns:
        str: The response text from the API.
    """
    url = "https://google.serper.dev/search"

    payload = json.dumps({
    "q": str(payload),
    "location": "Poland",
    "gl": "pl",
    "hl": "pl",
    "num": WEB_NO + WEB_OFFSET,
    "autocorrect": False
    })
    headers = {
    'X-API-KEY': 'f098495a313b5f76b66c71b8e93f31b8ac992454',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return(response.text)


def google_search(data, WEB_NO, WEB_OFFSET, save_data=True):
    """
    Performs a Google search for each row in the given data and returns the results.

    Args:
        data (pandas.DataFrame): The data containing the search queries.
        WEB_NO (int): The number of search results to fetch.
        WEB_OFFSET (int): The number of additional results to fetch.
        save_data (bool, optional): Whether to save the search results to a file. Defaults to True.

    Returns:
        dict: A dictionary containing the search results for each query.
    """
    results = {}
    for _, d in data.iterrows():
        query_results = get_request(d[2], WEB_NO, WEB_OFFSET)
        if query_results is False:  # Check if get_request() returns False
            print("Stopping execution as no credits left")
            break
        results[d[-1]] = query_results
        if save_data == True and len(results) % 10 == 0:
            with open(data_dir+'pages_dump2.json', 'w+', encoding='utf-8') as f:
                try:
                     curr_dumps = json.load(f)
                except json.decoder.JSONDecodeError:
                        curr_dumps = {}  # Create an empty dictionary if the file is empty or invalid JSON
                curr_dumps.update(results)
                json.dump(results, f, indent=2, ensure_ascii=False)
    return results

def format_names(input_string):
    """
    Formats the given input string by removing accents and replacing spaces with underscores.

    Args:
        input_string (str): The input string to be formatted.

    Returns:
        str: The formatted string.
    """
    cleaned_string = unidecode(input_string)
    cleaned_string = re.split(r"[\\/]",cleaned_string)[0].strip().replace(" ", "_").lower()
    
    return cleaned_string


def parse_response(response):
    """
    Parses the response from the Google Serper API and extracts the relevant information.

    Args:
        response (str): The response text from the API.

    Returns:
        list: A list of dictionaries containing the parsed results.
    """
    parsed_results = {}
    keys = ['title', 'link', 'snippet'] 
    for i, results in response.items():
        try:
            parsed_results[i] = [{key: result[key] for key in keys} for  result in json.loads(results)['organic']]
        except Exception as e:
            continue

    return parsed_results

def extract_content(source, data, WEB_NO: int, MIN_CHAR: int ):
    """
    Extracts the content from the given list of web pages.

    Args:
        source (dict): A dictionary containing the search results for each query.
        data (pandas.DataFrame): The data containing the search queries.
        WEB_NO (int): The number of search results to extract.

    Returns:
        dict: A dictionary containing the extracted content for each page.
        list: A list of invalid links that could not be extracted.
    """
    pages_extract = {}
    error_links = []
    with Goose({'use_publish_date': False}) as g:
        for name, dt in source.items():
            json_files = []
            for page in dt:
                    try:
                        response = requests.get(page['link'])
                        if response.status_code == 200:
                            content = g.extract(url=page['link'])
                            # Extract metadata
                            meta_description = content.meta_description
                            title = content.title
                            page_text = content.cleaned_text

                    except Exception as e:
                        error_links.append(page['link'])
                        print(page['link'], e)
                        continue
                    page_text = re.sub(r'[\n\t]+', ' ', content.cleaned_text)    
                    if len(page_text) < MIN_CHAR:
                        continue

                    json_files.append({"meta_description" : content.meta_description, "title" : content.title, "content" : page_text, "url" : page['link'],
                                       "category" : data.loc[data.iloc[:,-1] == name, data.columns[0]].values[0], "sub_category" : data.loc[data.iloc[:,-1] == name, 
                                       data.columns[1]].values[0], "phrase" : data.loc[data.iloc[:,-1] == name, data.columns[2]].values[0]})
                    if len(json_files) >= WEB_NO:
                        print(len(json_files), WEB_NO)
                        break
            save_jsons(name, json_files)
            pages_extract[name] = json_files

    return pages_extract, error_links

def extract_content(source, data, WEB_NO: int, MIN_CHAR: int):
    """
    Extracts the content from the given list of web pages.

    Args:
        source (dict): A dictionary containing the search results for each query.
        data (pandas.DataFrame): The data containing the search queries.
        WEB_NO (int): The number of search results to extract.
        MIN_CHAR (int): The minimum number of characters for extracted content.

    Returns:
        dict: A dictionary containing the extracted content for each page.
        list: A list of invalid links that could not be extracted.
    """
    pages_extract = {}
    error_links = []

    for name, dt in source.items():
        json_files = []
        for page in dt:
            try:
                response = requests.get(page['link'])
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extract metadata
                    meta_description = soup.find('meta', attrs={'name': 'description'})
                    title = soup.title.text if soup.title else None
                    page_text = soup.get_text()

            except Exception as e:
                error_links.append(page['link'])
                print(page['link'], e)
                continue
            
            # Clean up the text
            page_text = re.sub(r'[\n\t]+', ' ', page_text)
            if len(page_text) < MIN_CHAR:
                continue

            json_files.append({
                "meta_description": meta_description['content'] if meta_description else None,
                "title": title,
                "content": page_text,
                "url": page['link'],
                "category": data.loc[data.iloc[:, -1] == name, data.columns[0]].values[0],
                "sub_category": data.loc[data.iloc[:, -1] == name, data.columns[1]].values[0],
                "phrase": data.loc[data.iloc[:, -1] == name, data.columns[2]].values[0]
            })

            if len(json_files) >= WEB_NO:
                print(len(json_files), WEB_NO)
                break

        save_jsons(name, json_files)
        pages_extract[name] = json_files

    return pages_extract, error_links

def save_jsons(name, dt):
    """
    Saves the extracted content as JSON files.

    Args:
        data (dict): A dictionary containing the extracted content for each page.
    """

    name = re.sub(r'[^a-zA-Z0-9_]', '', name) 
    path = output_dir + name
    os.makedirs(path, exist_ok=True)
    print(len(dt))
    for p in dt:
        parsed_url = str(urlparse(p['url']).netloc.replace('www.', ''))
        # Extract the last part of the path which typically represents the webpage name
        with open(path + '\\'+ parsed_url + str(datetime.datetime.now().timestamp()).replace(".","") + '.json', 'w', encoding='utf-8') as f:
            json.dump(p, f, ensure_ascii=False)
    

def has_scrapped_cookies(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        content = data.get('content', '')
        # Use regex to search for the string "cookie" in the content field
        if re.search(r'\bcookie\b', content, re.IGNORECASE):
            return True
    return False

# Function to move file to trash folder
def move_to_trash(json_file, trash_folder):
    if not os.path.exists(trash_folder):
        os.makedirs(trash_folder)
    shutil.move(json_file, os.path.join(trash_folder, os.path.basename(json_file)))


DATASET = "reg_prods.csv"   # dataset name - source in huggingface
WEB_NO = 20                 # number of results to be extracted
WEB_OFFSET = 10             # number of additional results to fetch from google search
MIN_CHAR = 100              # minimum number of characters in the extracted content

try:
    from utils.functions import *
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

base_dir = os.path.dirname(os.path.abspath(__name__))
data_dir = os.path.join(base_dir, "data\\")
output_dir = get_dir_path("output\\") or os.path.join(base_dir, "output")


file_path = download_file(
    "https://huggingface.co/datasets/dr-mg/regional_prods_pl/raw/main/reg_prods.csv",
    data_dir,
    DATASET
)
#load dataset and convert code names
data = pd.read_csv(data_dir + DATASET)
data = data.replace('\s{2,}', ' ', regex=True)
data['code'] = data.apply(lambda x: format_names(x[2]), axis=1)

# Perform a Google search for each row in the dataset
search_results = google_search(data, WEB_NO, WEB_OFFSET)

parsed_results = parse_response(search_results)
pages_content, invalid_links = extract_content(parsed_results, data, WEB_NO, MIN_CHAR)


files_with_cookies = []
# Trash folder
trash_folder = base_dir + '/thrash'

# Walk through the directory tree
for folder, subfolders, files in os.walk(output_dir):
    for file in files:
        if file.endswith('.json'):
            json_file = os.path.join(folder, file)
            if has_scrapped_cookies(json_file):
                files_with_cookies.append(file)
                move_to_trash(json_file, trash_folder)

# Save list of files with scrapped cookie information
with open('files_with_cookies.txt', 'w') as f:
    for file in files_with_cookies:
        f.write(file + '\n')