import re

CLAUSES = {

    "Eligibility": [
        "eligibility",
        "eligibility criteria",
        "qualification",
        "bidder qualification",
        "minimum experience"
    ],

    "Budget": [
        "budget",
        "estimated budget",
        "project cost",
        "estimated cost"
    ],

    "Timeline": [
        "timeline",
        "project duration",
        "duration",
        "completion period"
    ],

    "Technical Requirements": [
        "technical requirements",
        "technical specification",
        "scope of work",
        "technical details"
    ],

    "Payment Terms": [
        "payment terms",
        "payment schedule",
        "payment"
    ],

    "EMD": [
        "emd",
        "earnest money deposit"
    ],

    "Security Deposit": [
        "security deposit"
    ],

    "Submission Deadline": [
        "submission deadline",
        "last date",
        "closing date"
    ]

}

def find_clause_heading(line):

    line = line.lower().strip()

    for clause, keywords in CLAUSES.items():

        for keyword in keywords:

            if keyword in line:
                return clause

    return None

def split_into_blocks(text):
    """
    Split a tender document into logical blocks.

    Detects:
    - Numbered sections
    - SECTION headings
    - ANNEXURE
    - APPENDIX
    - Large uppercase headings

    Falls back to the entire document if no headings are found.
    """

    if not text:
        return []

    pattern = r"""
    (?=
        \n\d+(\.\d+)*\.?\s
        |
        \nSECTION\s+[A-Z0-9IVXLC]+
        |
        \nANNEXURE[-\sA-Z0-9]*
        |
        \nAPPENDIX[-\sA-Z0-9]*
        |
        \n[A-Z][A-Z\s(),/&:-]{8,}
    )
    """

    blocks = re.split(
        pattern,
        text,
        flags=re.VERBOSE | re.IGNORECASE
    )

    cleaned = []

    for block in blocks:

        if block is None:
            continue

        block = block.strip()

        if len(block) > 50:
            cleaned.append(block)

    # If nothing matched, keep the entire document
    if not cleaned:
        cleaned.append(text.strip())

    return cleaned

def extract_clauses(text):

    extracted_clauses = {}

    current_clause = None

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        heading = find_clause_heading(line)

        if heading:

            current_clause = heading

            extracted_clauses[current_clause] = []

        elif current_clause:

            extracted_clauses[current_clause].append(line)

    for clause in extracted_clauses:
        extracted_clauses[clause] = " ".join(extracted_clauses[clause])

    return extracted_clauses