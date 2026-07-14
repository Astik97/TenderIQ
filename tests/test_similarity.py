from backend.services.similarity_service import (
    calculate_similarity,
    get_similarity_level,
    get_similarity_color
)

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

score = calculate_similarity(
    text1,
    text2
)

print("=" * 50)
print("Similarity Score")
print("=" * 50)

print(score)

print()

print("Level :",
      get_similarity_level(score))

print()

print("Color :",
      get_similarity_color(score))