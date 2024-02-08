"""Generate samples of the JSON files insturctions."""
import os
import json

# Output directory for the samples of the instructions
SAMPLES_DIR = 'instructions_samples'

# Directory containing created instructions files in json format
INSTRUCTIONS_FILES_DIR = 'output'

# Get the paths of the instructions and samples directories
base_dir = os.path.dirname(os.path.abspath(__file__))
samples_path = os.path.join(base_dir, SAMPLES_DIR)
instructions_files_path = os.path.join(base_dir, INSTRUCTIONS_FILES_DIR)

# Get the list of the generated instructions files
instructions_files = os.listdir(instructions_files_path)

# Iterate thorugh every instruction to create sample
for instruction in instructions_files:
    instruction_path = os.path.join(instructions_files_path, instruction)
    # Read instruction json file
    with open(instruction_path, 'r', encoding='utf-8') as json_read:
        data = json.load(json_read)
        # Generate new name of the json sample file
        instruction_name = instruction.split('.')[0]
        sample_file = os.path.join(samples_path, f'{instruction_name}_sample.json')
        # Create new sample json file and save 3 first records from the instruction file
        with open(sample_file, 'w', encoding='utf-8') as sample_file:
            first_three_elements = data[:3]
            json.dump(first_three_elements, sample_file, indent=4, ensure_ascii=False)
