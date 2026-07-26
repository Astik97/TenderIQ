"""
=========================================================
TenderIQ Embedding Service
---------------------------------------------------------
Responsible for

1. Loading Sentence Transformer model
2. Generating embeddings
3. Reusing the loaded model
=========================================================
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# Load Model (Loads Only Once)
# =========================================================

print("Loading Sentence Transformer Model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model Loaded Successfully.")

# =========================================================
# Generate Embedding
# =========================================================

def generate_embedding(text):
    """
    Generate embedding for a single clause.

    Parameters
    ----------
    text : str

    Returns
    -------
    numpy.ndarray
    """

    if not text or not text.strip():
        return None

    embedding = model.encode(text,
        convert_to_numpy=True,
        convert_to_tensor=False,
        normalize_embeddings=True)

    return embedding

# =========================================================
# Generate Multiple Embeddings
# =========================================================

def generate_embeddings(texts: list[str]):
    """
    Generate embeddings for multiple clauses.

    Parameters
    ----------
    texts : list[str]

    Returns
    -------
    numpy.ndarray
    """

    if not texts:
        return np.empty((0,384))

    embeddings = model.encode(texts,
        convert_to_numpy=True,
        convert_to_tensor=False,
        normalize_embeddings=True)

    return embeddings

# def calculate_embedding_similarity(embedding1, embedding2):
#     """
#     Cosine similarity between two embeddings.
#     """

#     score = cosine_similarity(
#         [embedding1],
#         [embedding2]
#     )[0][0]

#     return round(score * 100, 2)

# =========================================================
# Similarity Matrix
# =========================================================

def calculate_similarity_matrix(embeddings1, embeddings2):
    """
    Calculate cosine similarity matrix between
    all clauses of Tender A and Tender B.

    Parameters
    ----------
    embeddings1 : numpy.ndarray

    embeddings2 : numpy.ndarray

    Returns
    -------
    numpy.ndarray
    """

    if len(embeddings1) == 0 or len(embeddings2) == 0:
        return np.empty((0,0))

    return cosine_similarity(embeddings1,embeddings2)