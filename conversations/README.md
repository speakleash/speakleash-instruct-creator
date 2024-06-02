# Conversations

Example of the conversation record and it's fields.

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a Digital Marketing Expert."
    },
    {
      "role": "user",
      "content": "What are the first steps in creating a search network campaign in Google Ads?"
    },
    {
      "role": "assistant",
      "content": "The first step is to create a new campaign on your Google Ads account..."
    },
    {
      "role": "user",
      "content": "How do I choose the right keywords for my campaign?"
    },
    {
      "role": "assistant",
      "content": "Choosing the right keywords is crucial for the success of the campaign. You should start with...
    }
  ],
  "source_name": "Digital Marketing Guide"
  "source_description": "An article about using Google Tools to boost your image."
}
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
