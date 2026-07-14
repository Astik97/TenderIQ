from backend.services.clause_service import extract_clauses

sample_text = """
Eligibility Criteria

The bidder should have 5 years experience.

Technical Specification

The system should support cloud deployment.

Payment Terms

Payment will be made within 30 days.
"""

clauses = extract_clauses(sample_text)

print("=" * 50)
print("Extracted Clauses")
print("=" * 50)

for i, clause in enumerate(clauses, start=1):
    print(f"\nClause {i}")
    print("-" * 30)
    print(clause)