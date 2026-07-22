from backend.services.difference_service import compare_clauses

clause1 = """ 
The bidder should have 5 years experience. 
"""

clause2 = """ 
The bidder should have 8 years experience. 
"""

result = compare_clauses(clause1,clause2)

print("=" * 50)

print("Difference Result")

print("=" * 50)

for key, value in result.items():
    print(f"{key}: {value}")