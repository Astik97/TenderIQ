"""
=========================================================
TenderIQ Analytics Service
---------------------------------------------------------
Responsible for

1. Similarity Distribution
2. Risk Distribution
3. Clause Statistics
4. Dashboard Statistics
5. Analytics Summary
=========================================================
"""

from statistics import mean

# =========================================================
# Similarity Distribution
# =========================================================

def calculate_similarity_distribution(clause_results):
    """
    Count clauses by similarity level.
    """

    distribution = {

        "Excellent": 0,

        "Good": 0,

        "Moderate": 0,

        "Poor": 0

    }

    for clause in clause_results:

        similarity = clause["similarity"]

        if similarity >= 90:

            distribution["Excellent"] += 1

        elif similarity >= 70:

            distribution["Good"] += 1

        elif similarity >= 50:

            distribution["Moderate"] += 1

        else:

            distribution["Poor"] += 1

    return distribution

# =========================================================
# Risk Distribution
# =========================================================

def calculate_risk_distribution(clause_results):
    """
    Count clauses by risk level.
    """

    distribution = {

        "Very Low Risk":0,

        "Low Risk":0,

        "Medium Risk":0,

        "High Risk":0,

        "Critical Risk":0

    }

    for clause in clause_results:

        level = clause["risk"]["level"]

        if level in distribution:

            distribution[level] += 1

    return distribution

# =========================================================
# Clause Statistics
# =========================================================

def calculate_clause_statistics(clause_results):
    """
    Calculate similarity statistics.
    """

    if not clause_results:

        return {

            "highest_similarity":0,

            "lowest_similarity":0,

            "average_similarity":0

        }

    similarities = [

        clause["similarity"]

        for clause in clause_results

    ]

    return {

        "highest_similarity": round(max(similarities),2),

        "lowest_similarity": round(min(similarities),2),

        "average_similarity": round(mean(similarities),2)

    }

# =========================================================
# Dashboard Statistics
# =========================================================

def calculate_dashboard_statistics(result):
    """
    Overall dashboard statistics.
    """

    clause_results = result["clause_results"]

    statistics = calculate_clause_statistics(clause_results)

    return {

        "total_clauses": result["total_clauses"],

        "matched_clauses": result["matched_clauses"],

        "overall_similarity": result["similarity"],

        "weighted_similarity": result["weighted_similarity"],

        "highest_similarity": statistics["highest_similarity"],

        "lowest_similarity": statistics["lowest_similarity"],

        "average_similarity": statistics["average_similarity"]

    }

# =========================================================
# Generate Analytics
# =========================================================

def generate_analytics(result):
    """
    Generate complete analytics package.
    """

    clause_results = result["clause_results"]

    return {

        "similarity_distribution": calculate_similarity_distribution(clause_results),

        "risk_distribution": calculate_risk_distribution(clause_results),

        "clause_statistics": calculate_clause_statistics(clause_results),

        "dashboard_statistics": calculate_dashboard_statistics(result)

    }