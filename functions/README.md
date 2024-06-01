# Functions

Example of the function record and it's fields:

```json
[
  {
    "function_name": "call_llm",
    "description": "Call a Large Language Model (LLM) with a given prompt and return the generated response.",
    "input": {
      "prompt": "Translate the following English text to French: 'Hello, how are you?'"
    },
    "output": "Bonjour, comment ça va?",
    "source_name": "Translation Guide",
    "source_description": "A guide on how to translate text using various methods and tools."
  },
  {
    "function_name": "get_transcription",
    "description": "Get the transcription of an audio file.",
    "input": {
      "audio_file_path": "/path/to/audio/file.wav"
    },
    "output": "This is the transcription of the audio file.",
    "source_name": "Audio Processing Handbook",
    "source_description": "A comprehensive handbook on audio processing techniques, including transcription."
  }
]
```

It would be beneficial to include any fields with metadata, such as:

```json
"source_name": "The name of the resource used for the dataset creation, if any were used." (like shown above)
"source_url": "The URL of the used source datasets, if any were used." 
"source_description": "A short description of the used dataset: what it is about, the purpose of creation, authors." (like shown above)
"script_name": "If the script generating the dataset is reusable and you want to share it with us by committing to our repository."
"status": "If the instruction has been already manually verified, you can set the status as word `ok`. If not, leave the field as an empty string or None."
"updated_by": "If the instruction has already been manually verified, leave your name/nickname in this field. It will help us to give thanks :)"
"id": "numeric identifier for the dataset entry"
```
