from backend.services.clause_extraction import extract_clauses

sample_text = """
Eligibility Criteria

Minimum 5 years experience.

Estimated Budget

₹15 Crore

Project Duration

12 Months

Technical Requirements

Cloud Infrastructure

Payment Terms

40% advance

Submission Deadline

15 August 2026 """

result = extract_clauses(sample_text)

for clause, value in result.items():

    print("-" * 50)

    print(clause)

    print("-" * 50)

    print(value)

    print()