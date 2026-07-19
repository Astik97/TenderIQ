from backend.services.clause_service import extract_clauses

sample_text = """
1. Eligibility Criteria

The bidder should have 5 years experience.

2. Technical Specification

The system should support cloud deployment and provide ISO certified equipment.

3. Payment Terms

Payment will be made within 30 days.

4. General Conditions

The bidder shall maintain documentation.
"""

clauses = extract_clauses(sample_text)

print("=" * 50)
print("Extracted Clauses")
print("=" * 50)

for i, clause in enumerate(clauses, start=1):
    print(f"\nClause {i}")
    print("-" * 30)
    print(clause)

print("\nTotal:", len(clauses))