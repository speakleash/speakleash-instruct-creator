import sys
import os

# Get the absolute path to the directory containing the utils package
utils_dir = os.path.dirname(os.path.join(os.path.dirname(__file__), 
                                         "/Users/pawelkiszczak/!-SpeakLeash/speakleash-instruct-creator/utils"))

# Add the utils directory to sys.path if it's not already there
if utils_dir not in sys.path:
    sys.path.append(utils_dir)