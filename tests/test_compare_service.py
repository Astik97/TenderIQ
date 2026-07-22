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

print("\nSimilarity :", result["similarity"])

print("\nLevel :", result["level"])

print("\nColor :", result["color"])

for i, clause in enumerate(result["clause_results"], 
                           start=1):

    print(f"\nClause {i}")

    print("="*50)

    print("COMPARISON CLAUSE METRICS")

    print("="*50)

    print("\nOriginal :",clause["clause"])

    print("\nMatched With :",clause["best_match"])

    print("\nSimilarity :", clause["similarity"])

    print("\nLevel :", clause["level"])

    print("\nColor :",clause["color"])

    print("="*50)

    print("COMPARISON DIFFERENCE METRICS")

    print("="*50)
    
    print("\nChanged :",clause["difference"]["changed"])

    print("\nAdded :",clause["difference"]["added"])

    print("\nRemoved :",clause["difference"]["removed"])

    print("\nSummary :",clause["difference"]["summary"])

    print("="*50)

    print("COMPARISON RISK METRICS")

    print("="*50)
    
    print("\nRisk Score :",clause["risk"]["score"])

    print("\nRisk Level :",clause["risk"]["level"])

    print("\nRisk Color :",clause["risk"]["color"])

    print("\nRisk Reason :",clause["risk"]["reason"])

    print("\nRecommendation :",clause["risk"]["recommendation"])