"""
==========================================
Similarity Service
------------------------------------------
Responsible for:
1. TF-IDF Vectorization
2. Cosine Similarity Calculation
3. Similarity Score Formatting
==========================================
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(text1, text2):
    """
    Calculate similarity between two documents.

    Parameters
    ----------
    text1 : str
        First document

    text2 : str
        Second document

    Returns
    -------
    float
        Similarity percentage
    """

    # -----------------------------
    # Input Validation
    # -----------------------------

    if not text1 or not text2:
        return 0.0

    if not text1.strip() or not text2.strip():
        return 0.0

    # -----------------------------
    # TF-IDF Vectorization
    # -----------------------------

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [text1, text2]
    )

    # -----------------------------
    # Cosine Similarity
    # -----------------------------

    similarity_matrix = cosine_similarity(vectors)

    similarity_score = similarity_matrix[0][1]

    # -----------------------------
    # Convert into Percentage
    # -----------------------------

    similarity_percentage = similarity_score * 100

    return round(
        similarity_percentage,
        2
    )

def get_similarity_level(score):
    """
    Convert similarity percentage into readable category.
    """

    if score >= 90:
        return "Excellent Match"

    elif score >= 70:
        return "Good Match"

    elif score >= 50:
        return "Moderate Match"

    elif score >= 30:
        return "Low Match"

    return "Poor Match"

def get_similarity_color(score):
    """
    Used later for Dashboard UI.
    """

    if score >= 90:
        return "Green"

    elif score >= 70:
        return "SkyBlue"

    elif score >= 50:
        return "Orange"

    elif score >= 30:
        return "Yellow"

    return "Red"