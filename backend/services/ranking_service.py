"""
=========================================================
TenderIQ Ranking Service

Responsible for ranking compared clauses based on similarity and risk.

This service DOES NOT perform comparison.

It only sorts existing comparison results.

=========================================================
"""
DEFAULT_TOP_N = 5
# =========================================================
# Highest Matching Clause Ranking
# =========================================================

def get_highest_matching_clauses(
        clause_results, 
        top_n=DEFAULT_TOP_N):
    """
    Returns the top N highest matching clauses.

    Parameters
    ----------
    clause_results : list

    top_n : int

    Returns
    -------
    list
    """

    if not clause_results:
        
        return []

    ranked = sorted(

        clause_results,

        key=lambda x: x.get("similarity", 0),

        reverse=True

    )

    return ranked[:top_n]

# =========================================================
# Lowest Matching Clause Ranking
# =========================================================

def get_lowest_matching_clauses(
        clause_results, 
        top_n=DEFAULT_TOP_N):
    """
    Returns the lowest similarity clauses.

    Parameters
    ----------
    clause_results : list

    top_n : int

    Returns
    -------
    list
    """

    if not clause_results:

        return []

    ranked = sorted(

        clause_results,

        key=lambda x: x.get("similarity", 0)

    )

    return ranked[:top_n]

# =========================================================
# Highest Risk Clause Ranking
# =========================================================

def get_highest_risk_clauses(
        clause_results, 
        top_n=DEFAULT_TOP_N):
    """
    Returns clauses having the highest risk.

    Risk Priority

    Critical
    High
    Medium
    Low
    """

    if not clause_results:

        return []

    risk_priority = {

    "Critical Risk":5,

    "High Risk":4,

    "Medium Risk":3,

    "Low Risk":2,

    "Very Low Risk":1

}

    ranked = sorted(

        clause_results,

        key=lambda x: (

            risk_priority.get(
                x.get("risk", {}).get("level", "Very Low Risk"), 
                1),

                -x.get("similarity", 0)),

                reverse=True
    )

    return ranked[:top_n]

# =========================================================
# Summary Statistics
# =========================================================

def get_ranking_summary(clause_results):
    """
    Returns a summary dictionary used by
    AI Executive Summary.

    Returns
    -------
    dict
    """

    if not clause_results:

        return {

            "highest_match": None,

            "lowest_match": None,

            "highest_risk": None

        }

    highest_match = get_highest_matching_clauses(

        clause_results,

        top_n=1

    )[0]

    lowest_match = get_lowest_matching_clauses(

        clause_results,

        top_n=1

    )[0]

    highest_risk = get_highest_risk_clauses(

        clause_results,

        top_n=1

    )[0]

    return {

        "highest_match": highest_match,

        "lowest_match": lowest_match,

        "highest_risk": highest_risk

    }