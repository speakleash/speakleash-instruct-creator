import os
import requests

def download_file(url, download_dir, file_name):

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    file_path = os.path.join(download_dir, file_name)

    if os.path.exists(file_path):
        return file_path

    r = requests.get(url, allow_redirects=True)
    open(file_path, 'wb').write(r.content)

    return file_path
