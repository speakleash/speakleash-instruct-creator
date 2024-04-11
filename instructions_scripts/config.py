import sys
import os
from utils.functions import get_dir_path

# Get the absolute path to the directory containing the utils package
base_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = get_dir_path("utils") or os.path.join(base_dir, "utils")

# Add the utils directory to sys.path if it's not already there
if utils_dir not in sys.path:
    sys.path.append(utils_dir)