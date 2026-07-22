import re

def normalize_whitespace(text):
    """
    Remove extra spaces, tabs and blank lines.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")

    text = text.replace("\r", "\n")

    # Remove repeated spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces around newlines
    text = re.sub(r" *\n *", "\n", text)

    # Keep paragraph spacing
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def remove_special_characters(text):
    """
    Remove unnecessary symbols while keeping letters,
    numbers and common punctuation.
    """

    text = re.sub(r'[^a-zA-Z0-9\s.,:%()/\-]', '', text)

    return text

def convert_to_lowercase(text):
    """Convert everything to lowercase."""

    return text.lower()

def clean_text(text):
    """Complete preprocessing pipeline."""

    text = convert_to_lowercase(text)

    text = remove_special_characters(text)

    text = normalize_whitespace(text)

    return text