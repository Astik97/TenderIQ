"""
====================================================
TenderIQ - Clause Extraction Service
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

HEADING_PATTERN = re.compile(
    r"""
    ^
    (
        \d+(\.\d+)*\.?\s+[A-Za-z].*
        |
        [A-Z][A-Za-z ]{3,}$
    )
    """,
    re.VERBOSE
)

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
    text = text.replace("\r", "\n")

    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n{2,}", "\n\n", text)

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

    if not text:
        return []

    clauses = re.split(r"\n\s*\n", text)

    cleaned = []
    
    for clause in clauses:
        
        if clause is None:
            continue
        
        clause = clause.strip()
        
        if not clause:
            continue

        # if len(clause) < 20:
        #     continue
        
        cleaned.append(clause)

    return cleaned

# =========================================================
# Merge Small Fragments
# =========================================================

def merge_short_clauses(clauses):

    merged = []

    i = 0

    while i < len(clauses):

        current = clauses[i].strip()

        if (
            HEADING_PATTERN.match(current)
            and i + 1 < len(clauses)
            and not HEADING_PATTERN.match(clauses[i + 1].strip())
        ):

            current += "\n\n" + clauses[i + 1].strip()

            i += 1

        merged.append(current)

        i += 1

    return merged

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

    text = clean_text(text)

    clauses = split_into_clauses(text)

    clauses = remove_empty_clauses(clauses)

    clauses = merge_short_clauses(clauses)

    return clauses