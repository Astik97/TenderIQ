import time
from backend.services.semantic_similarity_service import *

clauses = ["Payment must be completed within 30 days."] * 1000

start = time.time()

embeddings = generate_embeddings(clauses)

end = time.time()

print(f"Embedding Time : {end-start:.2f} seconds")