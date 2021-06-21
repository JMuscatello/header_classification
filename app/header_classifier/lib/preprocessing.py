import re


def preprocess(text):
    """
    Preprocesses text to replace header numbers and indicate all caps by
    appending a string

    Args:
        text (String): String to apply preprocessing to

    Returns:
        processed string
    """
    text = re.sub(r'[0-9]+(\.?)\s+(?=[A-Z].+)', 'NUM', text)
    if text.isupper():
        text = text + ' ALL_CAPS'
    return text
