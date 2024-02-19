import os
import requests


def download_file(url: str, download_dir: str, file_name: str) -> str:
    """
    Download file with the given url address.

    :param url: Provided url address to download the file
    :param download_dir: The destination folder for the downloaded file.
    :param file_name: The name of the downloaded file.
    :return: The path to the downloaded file.
    """

    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, file_name)

    if not os.path.exists(file_path):
        r = requests.get(url, allow_redirects=True)
        with open(file_path, 'wb') as file:
            file.write(r.content)

    return file_path


def create_directory(*paths: str) -> None:
    """
    If not created yet, create any numer of given directories.

    :param: paths: The patsh to the directories to be created
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)


def get_dir_path(dir_name: str) -> str or None:
    """
    Get the path to the parent directory. If the parent directory does not exist, return None.
    Returns the same path for scripts run independently as well ass through merge_files.py

    :param dir_name: The name of the directory.
    :return: The path to the parent directory or None if it does not exist.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(base_dir)
    return os.path.join(parent_path, dir_name)
