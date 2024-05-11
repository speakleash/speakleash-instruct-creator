import re


def reduce_whitespace(text):
    """
    Reduces sequences of whitespace characters in the input string.

    This function performs the following transformations:
    1. Replaces sequences of spaces and newlines mixed together with a single newline.
    2. Replaces sequences of space characters with a single space.
    3. Trims leading and trailing whitespace from the input string.

    Parameters:
    text (str): The input string to be transformed.

    Returns:
    str: The transformed string with reduced whitespace.
    """
    if text is None:
        return text

    # Remove leading and trailing whitespace
    text = text.strip()

    # Replace sequences including at least one newline and any amount of spaces/tabs with a single newline
    text = re.sub(r'(\s*\n+\s*)+', '\n', text)

    # Replace multiple space characters with a single space
    text = re.sub(r'[ \t]+', ' ', text)

    return text
