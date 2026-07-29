"""
=========================================================
AI Executive Summary Service
=========================================================

This service converts clause comparison results into
a professional executive summary.

Input:
    clause_results

Output:
    summary dictionary

Used by:
    compare_service.py
"""

# =========================================================
# Risk Distribution
# =========================================================

def calculate_risk_distribution(clause_results):

    distribution = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for clause in clause_results:

        risk = clause.get("risk", {}).get("level", "Low")

        if risk in distribution:
            distribution[risk] += 1

    return distribution

# =========================================================
# AI Executive Summary Service
# =========================================================

def calculate_risk_level(clause_results):
    """
    Calculate overall project risk based on
    clause level risks.
    """

    risk_count = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for clause in clause_results:

        risk = clause.get("risk", {}).get("level", "Low")

        if risk in risk_count:
            risk_count[risk] += 1

    if risk_count["Critical"] >= 3:
        return "Critical"

    if risk_count["High"] >= 5:
        return "High"

    if risk_count["Medium"] >= 5:
        return "Medium"

    return "Low"

# =========================================================
# Count Match Levels
# =========================================================

def count_match_levels(clause_results):

    levels = {
        "Excellent": 0,
        "Good": 0,
        "Moderate": 0,
        "Poor": 0
    }

    for clause in clause_results:

        level = clause.get("level", "Poor")

        if "Excellent" in level:
            levels["Excellent"] += 1

        elif "Good" in level:
            levels["Good"] += 1

        elif "Moderate" in level:
            levels["Moderate"] += 1

        else:
            levels["Poor"] += 1

    return levels

# =========================================================
# Highest Matching Clause
# =========================================================

def find_best_clause(clause_results):

    if not clause_results:
        return None

    return max(
        clause_results,
        key=lambda x: x["similarity"]
    )

# =========================================================
# Highest Risk Clause
# =========================================================

def find_highest_risk_clause(clause_results):

    priority = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    if not clause_results:
        return None

    return max(
        clause_results,
        key=lambda x: priority.get(
            x["risk"]["level"],
            0
        )
    )

# =========================================================
# Major Differences
# =========================================================

def extract_major_differences(clause_results):

    differences = []

    for clause in clause_results:

        diff = clause.get("difference", {})

        if diff.get("changed", False):

            summary = diff.get("summary", "")

            if summary and summary not in differences:
                differences.append(summary)

        if len(differences) == 5:
            break

    return differences

# =========================================================
# AI Recommendation
# =========================================================

def generate_recommendation(overall_similarity,risk_level):

    if overall_similarity >= 90:

        return (
            "The tenders are highly similar. "
            "Minor verification before submission is sufficient."
        )

    elif overall_similarity >= 75:

        return (
            "Most clauses are similar. "
            "Review payment terms, eligibility and timelines."
        )

    elif overall_similarity >= 50:

        return (
            "Moderate similarity detected. "
            "Manual review is strongly recommended."
        )

    elif risk_level == "Critical":

        return (
            "Critical differences detected. "
            "Do not proceed without detailed review."
        )

    else:

        return (
            "Large differences detected between the tenders. "
            "Carefully verify all important clauses."
        )

# =========================================================
# Generate Executive Summary
# =========================================================

def generate_ai_summary(result):
    """
    Generate complete executive summary.

    result = compare_tenders(...)
    """

    clause_results = result["clause_results"]

    best_clause = find_best_clause(clause_results)

    highest_risk = find_highest_risk_clause(clause_results)

    risk_level = calculate_risk_level(clause_results)

    match_levels = count_match_levels(clause_results)

    differences = extract_major_differences(clause_results)

    recommendation = generate_recommendation(result["similarity"],risk_level)

    return {

        "overall_similarity": result["similarity"],

        "risk_level": risk_level,

        "total_clauses": result["total_clauses"],

        "matched_clauses": result["matched_clauses"],

        "highest_matching_clause": best_clause,

        "highest_risk_clause": highest_risk,

        "major_differences": differences,

        "match_distribution": match_levels,

        "recommendation": recommendation
    }