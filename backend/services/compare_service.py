"""
=========================================================
TenderIQ Compare Service
=========================================================

Responsibilities

1. Extract clauses from both tenders
2. Compare every clause
3. Find best matching clause
4. Calculate overall similarity
5. Return complete comparison result
=========================================================
"""

from backend.services.clause_service import extract_clauses

from backend.services.difference_service import (
    compare_clauses as compare_clause_difference
)

from backend.services.risk_service import analyze_risk

from backend.services.embedding_service import (
    generate_embeddings,
    calculate_similarity_matrix
)

from backend.services.similarity_service import (
    get_similarity_level,
    get_similarity_color
)

# =========================================================
# Compare Individual Clauses
# =========================================================

def compare_clauses(clauses1, clauses2,similarity_matrix):
    """
    Compare every clause from Tender A
    against every clause from Tender B.

    Returns

    [
        {
            clause,
            best_match,
            similarity,
            level,
            color
        }
    ]
    """

    comparison_results = []

    for i, clause1 in enumerate(clauses1):

        if (i + 1) % 100 == 0:
            print(f"Comparing clause {i+1}/{len(clauses1)}")

        best_score = 0
        best_clause = ""

        # ----------------------------------
        # Best Match
        # ----------------------------------

        if similarity_matrix.shape[1] == 0:
            continue

        best_index = similarity_matrix[i].argmax()

        best_score = round(similarity_matrix[i][best_index] * 100,2)

        best_clause = clauses2[best_index]

        # ----------------------------------
        # Difference
        # ----------------------------------

        difference = compare_clause_difference(clause1, best_clause)

        # ----------------------------------
        # Risk
        # ----------------------------------

        risk = analyze_risk(best_score, difference)

        comparison_results.append({

            "clause": clause1,

            "best_match": best_clause,

            "similarity": best_score,

            "level": get_similarity_level(best_score),

            "color": get_similarity_color(best_score),

            "difference": difference,

            "risk": risk

        })

    return comparison_results

# =========================================================
# Overall Similarity
# =========================================================

def calculate_overall_similarity(clause_results):

    """Average similarity of all matched clauses."""

    if not clause_results:
        return 0

    total = 0

    for result in clause_results:

        total += result["similarity"]

    return round(total / len(clause_results),2)

# =========================================================
# Main Compare Function
# =========================================================

def compare_tenders(text1, text2):

    """Main function called from compare_routes.py"""

    # --------------------------------------
    # Extract Clauses
    # --------------------------------------

    clauses1 = extract_clauses(text1)

    clauses2 = extract_clauses(text2)

    embeddings1 = generate_embeddings(clauses1)

    embeddings2 = generate_embeddings(clauses2)

    similarity_matrix = calculate_similarity_matrix(embeddings1,embeddings2)

    # --------------------------------------
    # Clause Comparison
    # --------------------------------------

    clause_results = compare_clauses(clauses1,clauses2,similarity_matrix)

    # --------------------------------------
    # Overall Similarity
    # --------------------------------------

    overall_similarity = calculate_overall_similarity(clause_results)

    # --------------------------------------
    # Final Result
    # --------------------------------------

    return {

        "similarity": overall_similarity,

        "level": get_similarity_level(overall_similarity),

        "color": get_similarity_color(overall_similarity),

        "total_clauses": len(clauses1),

        "tender1_clauses":len(clauses1),

        "tender2_clauses": len(clauses2),

        "matched_clauses": len(clause_results),

        "clause_results": clause_results

    }