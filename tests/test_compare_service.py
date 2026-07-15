from backend.services.compare_service import compare_tenders

text1 = """
Eligibility Criteria

Company should have 5 years experience.

Technical Specification

ISO Certified.

Payment Terms

30 days.
"""

text2 = """
Eligibility

Minimum experience 4 years.

Technical

ISO Certified Company.

Payment

Payment within 45 days.
"""

result = compare_tenders(text1, text2)

print("=" * 60)
print("OVERALL RESULT")
print("=" * 60)

print("Similarity :", result["similarity"])
print("Level      :", result["level"])
print("Color      :", result["color"])

print("\n")

print("=" * 60)
print("CLAUSE COMPARISON")
print("=" * 60)

for i, clause in enumerate(result["clause_results"], start=1):

    print(f"\nClause {i}")

    print("-" * 40)

    print("Original :")

    print(clause["clause"])

    print("\nMatched With :")

    print(clause["best_match"])

    print("\nSimilarity :", clause["similarity"])

    print("Level      :", clause["level"])
    
    print("Changed :")

    print(
        clause["difference"]["changed"]
    )

    print("Added :")

    print(
        clause["difference"]["added"]
    )

    print("Removed :")

    print(
        clause["difference"]["removed"]
    )

    print("Summary :")

    print(
        clause["difference"]["summary"]
    )

print()

print(result["clause_results"][0].keys())

print("=" * 60)

print("Returned Dictionary Keys")

print("=" * 60)

print(result.keys())
