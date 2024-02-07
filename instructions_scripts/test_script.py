import os

try:
    from utils.functions import download_file, bob, get_dir_path2
except ImportError as e:
    print(f'Error: {e}')
    def get_dir_path(directory):
        return None

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")

print(data_dir)
print(download_file)
print(get_dir_path)
bob()