"""
=========================================================
TenderIQ Risk Service
---------------------------------------------------------
Responsible for

1. Risk Identification
2. Risk Classification
3. Risk Score
4. Risk Recommendation
=========================================================
"""

# =========================================================
# Risk Level
# =========================================================

def get_risk_level(similarity):

    if similarity >= 90:

        return "Very Low Risk"

    elif similarity >= 70:

        return "Low Risk"

    elif similarity >= 50:

        return "Medium Risk"

    elif similarity >= 30:

        return "High Risk"

    else:

        return "Critical Risk"

# =========================================================
# Risk Color
# =========================================================

def get_risk_color(level):

    colors = {

        "Very Low Risk": "green",

        "Low Risk": "blue",

        "Medium Risk": "yellow",

        "High Risk": "orange",

        "Critical Risk": "red"

    }

    return colors.get(level, "gray")

# =========================================================
# Risk Score
# =========================================================

def calculate_risk_score(similarity):

    """
    Higher similarity
    means lower risk.
    """

    return round(100 - similarity, 2)

# =========================================================
# Risk Reason
# =========================================================

def get_risk_reason(difference):

    added = difference.get("added", [])

    removed = difference.get("removed", [])

    if not added and not removed:

        return "No significant textual changes detected."

    reason = []

    if added:

        reason.append(

            f"Added keywords: {', '.join(added)}"

        )

    if removed:

        reason.append(

            f"Removed keywords: {', '.join(removed)}"

        )

    return " | ".join(reason)

# =========================================================
# Recommendation
# =========================================================

def get_recommendation(level):

    recommendations = {

        "Very Low Risk":

            "Clause is almost identical. Manual review is optional.",

        "Low Risk":

            "Minor wording changes detected. Quick verification recommended.",

        "Medium Risk":

            "Review this clause carefully before submitting the bid.",

        "High Risk":

            "Major changes detected. Detailed manual verification is recommended.",

        "Critical Risk":

            "Clause differs significantly. Immediate review is required."

    }

    return recommendations.get(

        level,

        "Review manually."

    )

# =========================================================
# Main Risk Analyzer
# =========================================================

def analyze_risk(similarity, difference):

    level = get_risk_level(

        similarity

    )

    return {

        "score": calculate_risk_score(

            similarity

        ),

        "level": level,

        "color": get_risk_color(

            level

        ),

        "reason": get_risk_reason(

            difference

        ),

        "recommendation": get_recommendation(

            level

        )

    }
