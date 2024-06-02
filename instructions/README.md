# Instructions

Example of main fields (depends on the type of the implemented set: instructions, functions, conversations, etc.) for the instructions type:
```json
{
  "instruction": "Why is the EU putting in place a Carbon Border Adjustment Mechanism?",
  "input": "Text on which answer will be based on (if exists) else leave empty string",
  "output": "The EU is at the forefront of international efforts..."
},
```
It would be beneficial to include any fields with metadata, such as:

```json
"source_name": "The name of the resource used for the dataset creation, if any were used."
"source_url": "The URL of the used source datasets, if any were used."
"source_description": "A short description of the used dataset: what it is about, the purpose of creation, authors."
"script_name": "If the script generating the dataset is reusable and you want to share it with us by committing to our repository."
"status": "If the instruction has been already manually verified, you can set the status as "ok". If not, leave the field as an empty string or None."
"updated_by": "If the instruction has already been manually verified, leave your name/nickname in this field. It will help us to give thanks :)"
"id": "numeric identifier for the dataset entry"
```
