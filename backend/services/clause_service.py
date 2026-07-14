"""
====================================================
TenderIQ
Clause Extraction Service
Milestone 5
====================================================

This service is responsible for:

1. Cleaning extracted tender text
2. Splitting the document into clauses
3. Removing empty clauses
4. Returning a clean clause list

This service DOES NOT compare clauses.

Comparison is handled later by compare_service.py
"""

import re

# ==================================================
# Clean Extracted Text
# ==================================================

def clean_text(text):
    """
    Clean extracted OCR/PDF text.

    Removes:

    • Multiple blank lines
    • Extra spaces
    • Tabs
    • Leading/trailing whitespace
    """

    if not text:
        return ""

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Remove multiple spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

# ==================================================
# Split Into Clauses
# ==================================================

def split_into_clauses(text):
    """
    Split a tender into logical clauses.

    Current strategy:

    Split wherever two blank lines occur.

    Future versions will split using:

    • Clause numbers
    • Section numbers
    • NLP
    • LLMs
    """

    text = clean_text(text)

    clauses = re.split(r"\n\s*\n", text)

    return clauses

# ==================================================
# Remove Empty Clauses
# ==================================================

def remove_empty_clauses(clauses):
    """
    Remove empty clauses.
    """

    cleaned = []

    for clause in clauses:

        clause = clause.strip()

        if clause:

            cleaned.append(clause)

    return cleaned

# ==================================================
# Main Function
# ==================================================

def extract_clauses(text):
    """
    Main function used by compare_service.py

    Returns:

    [
        clause1,
        clause2,
        clause3
    ]
    """

    clauses = split_into_clauses(text)

    clauses = remove_empty_clauses(clauses)

    return clauses