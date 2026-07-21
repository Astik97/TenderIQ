"""
====================================================
TenderIQ - Clause Extraction Service

====================================================

This service is responsible for:

1. Cleaning extracted tender text
2. Splitting the document into clauses
3. Removing empty clauses
4. Returning a clean clause list

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
# Remove Page Numbers
# ==================================================

def remove_page_numbers(text):
    """
    Remove common page number patterns.
    """

    if not text:
        return ""

    patterns = [

        r"Page\s+\d+\s+of\s+\d+",
        r"Page\s+\d+",
        r"Page No\.?\s*\d+",
        r"^\d+$",
        r"^\d+\s+of\s+\d+$"

    ]

    for pattern in patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE | re.MULTILINE
        )

    return text

# ==================================================
# Remove Repeated Headers & Footers
# ==================================================

def remove_headers_and_footers(text):
    """
    Remove common repeated headers and footers.
    """

    if not text:
        return ""

    patterns = [

        r"Government of India",
        r"Tender Document",
        r"Confidential",
        r"Page Header",
        r"Footer",
        r"Digitally Signed",
        r"This is a computer generated document"

    ]

    for pattern in patterns:

        text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE
        )

    return text

# ==================================================
# Remove Table of Contents
# ==================================================

def remove_table_of_contents(text):
    """
    Remove table of contents section.
    """

    if not text:
        return ""

    toc_pattern = re.compile(

        r"contents.*?(?=\n\s*(1\.|section|chapter|introduction))",

        flags=re.IGNORECASE | re.DOTALL

    )

    return toc_pattern.sub("", text)

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

    clauses = re.split(

    r"""
    (?=
        \n\d+(\.\d+)*\.?\s
        |
        \nSECTION\s+[IVXLC0-9]+
        |
        \nANNEXURE
        |
        \nAPPENDIX
        |
        \n[A-Z][A-Z\s]{5,}
    )
    """,

    text,

    flags=re.VERBOSE | re.IGNORECASE

)
    
    cleaned = []
    
    for clause in clauses:
        
        if clause is None:
            continue
        
        clause = clause.strip()
        
        if not clause:
            continue
        
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

        if len(current.split()) < 8 and i + 1 < len(clauses):

        # if (
        #     HEADING_PATTERN.match(current)
        #     and i + 1 < len(clauses)
        #     and not HEADING_PATTERN.match(clauses[i + 1].strip())
        # ):

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

    text = remove_page_numbers(text)

    text = remove_headers_and_footers(text)

    text = remove_table_of_contents(text)

    clauses = split_into_clauses(text)

    clauses = remove_empty_clauses(clauses)

    clauses = merge_short_clauses(clauses)

    return clauses