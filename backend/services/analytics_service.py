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
from backend.services.weight_service import get_clause_weight

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

    if not clause_results:
        return distribution

    for clause in clause_results:
        similarity = clause.get("similarity", 0)

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

    risk_level = {
        "Very Low Risk":0,
        "Low Risk":0,
        "Medium Risk":0,
        "High Risk":0,
        "Critical Risk":0
    }
    
    if not clause_results:
        return risk_level

    for clause in clause_results:
        level = clause.get("risk", {}).get("level", "Very Low Risk")

        if level in risk_level:
            risk_level[level] += 1

    return risk_level

# ========================================================
# Match Distribution
# ========================================================

def calculate_match_distribution(clause_results):
    """
    Count clauses by match level.
    """

    distribution = {
        "Excellent": 0,
        "Good": 0,
        "Moderate": 0,
        "Poor": 0
    }

    if not clause_results:
        return distribution

    for clause in clause_results:
        level = clause.get("match_level", "Poor")

        if level in distribution:
            distribution[level] += 1

    return distribution

# =======================================================
# Priority Distribution
# =======================================================

def calculate_priority_distribution(clause_results):
    """
    Count clauses by priority level.
    """

    distribution = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
        "Very Low": 0
    }

    if not clause_results:
        return distribution

    for clause in clause_results:
        weight = get_clause_weight(clause.get("clause", ""))

        if weight >= 10:
            distribution["Critical"] += 1

        elif weight >= 8:
            distribution["High"] += 1

        elif weight >= 5:
            distribution["Medium"] += 1

        else:
            distribution["Very Low"] += 1

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
        clause.get("similarity", 0)
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

    clause_results = result.get("clause_results", [])

    statistics = calculate_clause_statistics(clause_results)

    return {

        "total_clauses": result.get("total_clauses", 0),

        "matched_clauses": result.get("matched_clauses", 0),

        "overall_similarity": result.get("similarity", 0),

        "weighted_similarity": result.get("weighted_similarity", 0),

        "highest_similarity": statistics.get("highest_similarity", 0),

        "lowest_similarity": statistics.get("lowest_similarity", 0),

        "average_similarity": statistics.get("average_similarity", 0)

    }

# =========================================================
# Generate Analytics
# =========================================================

def generate_analytics_summary(result):
    """
    Generate complete analytics package.
    """

    clause_results = result.get("clause_results", [])

    return {

        "similarity_distribution": calculate_similarity_distribution(clause_results),

        "risk_distribution": calculate_risk_distribution(clause_results),

        "clause_statistics": calculate_clause_statistics(clause_results),

        "match_distribution": calculate_match_distribution(clause_results),

        "priority_distribution": calculate_priority_distribution(clause_results),

        "dashboard_statistics": calculate_dashboard_statistics(result)

    }