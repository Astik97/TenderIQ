"""
=========================================================
TenderIQ Semantic Similarity Service
---------------------------------------------------------
Responsibilities

1. Load Sentence Transformer model
2. Generate clause embeddings
3. Calculate cosine similarity
=========================================================
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading AI Model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("AI Model Loaded Successfully")

# =========================================================
# Generate Single Embedding
# =========================================================

def generate_embedding(text):

    if not text:
        return None

    return model.encode(text,
        convert_to_numpy=True
    )

# =========================================================
# Generate Multiple Embeddings
# =========================================================

def generate_embeddings(texts):

    if not texts:
        return []

    return model.encode(texts,
        convert_to_numpy=True
    )

# =========================================================
# Cosine Similarity
# =========================================================

def calculate_similarity(embedding1, embedding2):

    similarity = cosine_similarity(

        [embedding1],

        [embedding2]

    )[0][0]

    return round(similarity * 100, 2)