"""
=========================================================
TenderIQ Semantic Search Service
---------------------------------------------------------
Responsible for

1. Keyword Search
2. Semantic Search
3. Clause Ranking
4. Search Summary
=========================================================
"""

from backend.utils.db import get_connection
from backend.services.embedding_service import generate_embedding
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# Keyword Search
# =========================================================

def search_by_keyword(user_id, keyword):
    """
    Search uploaded tenders using a keyword.

    Parameters
    ----------
    user_id : int

    keyword : str

    Returns
    -------
    list
    """

    if not keyword or not keyword.strip():
        return []

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id,
        tender_name,
        extracted_text,
        upload_date
        FROM tenders
        WHERE user_id = %s
        AND 
        (
            tender_name LIKE %s

            OR

            extracted_text LIKE %s
        )

        ORDER BY upload_date DESC
        """

        pattern = f"%{keyword}%"

        cursor.execute(query,(user_id,pattern,pattern))

        results = cursor.fetchall()

        return results

    except Exception as e:
        
        print(f"[Search Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Semantic Search
# =========================================================

def search_by_embedding(user_id, query, threshold=50):
    """
    Performs semantic search using Sentence Transformer embeddings.

    Parameters
    ----------
    user_id : int

    query : str

    threshold : float
        Minimum similarity percentage.

    Returns
    -------
    list
    """

    if not query or not query.strip():
        return []

    conn = None
    cursor = None

    try:

        # ----------------------------------
        # Query Embedding
        # ----------------------------------

        query_embedding = generate_embedding(query)

        if query_embedding is None:
            return []

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        query_sql = """
        SELECT id,
        tender_name,
        extracted_text,
        upload_date
        FROM tenders
        WHERE user_id = %s
        """

        cursor.execute(query_sql, (user_id,))

        tenders = cursor.fetchall()

        results = []

        # ----------------------------------
        # Compare Query Against Every Tender
        # ----------------------------------

        for tender in tenders:

            text = tender.get("extracted_text", "")

            if not text.strip():
                continue

            document_embedding = generate_embedding(text)

            score = cosine_similarity(
                [query_embedding],
                [document_embedding]
            )[0][0]

            similarity = round(score * 100, 2)

            if similarity >= threshold:

                results.append({

                    "id": tender["id"],

                    "tender_name": tender["tender_name"],

                    "similarity": similarity,

                    "upload_date": tender["upload_date"]

                })

        # ----------------------------------
        # Highest Similarity First
        # ----------------------------------

        results.sort(key=lambda x: x["similarity"],reverse=True)

        return results

    except Exception as e:

        print(f"[Search Service] {e}")

        return []

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Search Clauses
# =========================================================

def search_clauses(user_id, query, threshold=50):
    """
    Performs complete search using

    1. Keyword Search
    2. Semantic Search

    Parameters
    ----------
    user_id : int

    query : str

    threshold : float

    Returns
    -------
    list
    """

    # --------------------------------------
    # Keyword Results
    # --------------------------------------

    keyword_results = search_by_keyword(user_id,query)

    # --------------------------------------
    # Semantic Results
    # --------------------------------------

    semantic_results = search_by_embedding(user_id,query,threshold)

    # --------------------------------------
    # Merge Results
    # --------------------------------------

    merged = {}

    # Add keyword matches first

    for result in keyword_results:

        merged[result["id"]] = {

            "id": result["id"],

            "tender_name": result["tender_name"],

            "upload_date": result["upload_date"],

            "similarity": 100,

            "search_type": "Keyword"

        }

    # Add semantic matches

    for result in semantic_results:

        tender_id = result["id"]

        if tender_id in merged:

            merged[tender_id]["similarity"] = max(

                merged[tender_id]["similarity"],

                result["similarity"])

            merged[tender_id]["search_type"] = "Keyword + Semantic"

        else:

            merged[tender_id] = {

                "id": tender_id,

                "tender_name": result["tender_name"],

                "upload_date": result["upload_date"],

                "similarity": result["similarity"],

                "search_type": "Semantic"

            }

    return list(merged.values())


# =========================================================
# Rank Search Results
# =========================================================

def rank_search_results(results):
    """
    Sort search results by similarity.

    Parameters
    ----------
    results : list

    Returns
    -------
    list
    """

    if not results:
        return []

    ranked = sorted(results,
        key=lambda x: (x["similarity"],x["upload_date"]),
        reverse=True
    )

    return ranked

# =========================================================
# Search Summary
# =========================================================

def generate_search_summary(results):
    """
    Generate summary for search results.

    Parameters
    ----------
    results : list

    Returns
    -------
    dict
    """

    if not results:

        return {

            "total_results": 0,

            "keyword_matches": 0,

            "semantic_matches": 0,

            "hybrid_matches": 0,

            "highest_similarity": 0,

            "average_similarity": 0,

            "best_match": None

        }

    # --------------------------------------
    # Count Search Types
    # --------------------------------------

    keyword_matches = 0
    semantic_matches = 0
    hybrid_matches = 0

    similarities = []

    for result in results:

        similarities.append(result["similarity"])

        search_type = result.get("search_type", "")

        if search_type == "Keyword":
            keyword_matches += 1

        elif search_type == "Semantic":
            semantic_matches += 1

        elif search_type == "Keyword + Semantic":
            hybrid_matches += 1

    # --------------------------------------
    # Best Match
    # --------------------------------------

    best_match = max(results,key=lambda x: x["similarity"])

    # --------------------------------------
    # Summary
    # --------------------------------------

    return {

        "total_results": len(results),

        "keyword_matches": keyword_matches,

        "semantic_matches": semantic_matches,

        "hybrid_matches": hybrid_matches,

        "highest_similarity": round(max(similarities), 2),

        "average_similarity": round(sum(similarities) / len(similarities),2),

        "best_match": best_match

    }