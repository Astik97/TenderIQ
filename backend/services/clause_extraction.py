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