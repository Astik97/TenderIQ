from backend.services.compare_service import compare_tenders

text1 = """
Python
Flask
MySQL
Docker
"""

text2 = """
Python
Flask
PostgreSQL
Docker
"""

result = compare_tenders(
    text1,
    text2
)

print("="*50)

print("Comparison Result")

print("="*50)

print()

print(result)

print()

print("Similarity :", result["similarity"])

print("Level :", result["level"])

print("Color :", result["color"])