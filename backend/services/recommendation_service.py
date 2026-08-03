"""
=========================================================
TenderIQ Recommendation Service
---------------------------------------------------------
Responsible for

1. Clause Recommendations
2. Priority Actions
3. Submission Checklist
4. Final Recommendation
5. Recommendation Summary
=========================================================
"""

PRIORITY_ACTIONS = {

        "payment":
        "Review Payment Terms.",

        "eligibility":
        "Verify Eligibility Criteria.",

        "emd":
        "Verify EMD Amount.",

        "earnest money":
        "Verify Earnest Money Deposit.",

        "bid security":
        "Check Bid Security Requirements.",

        "technical":
        "Review Technical Specifications.",

        "specification":
        "Review Technical Specifications.",

        "delivery":
        "Verify Delivery Timeline.",

        "warranty":
        "Review Warranty Conditions.",

        "penalty":
        "Review Penalty Clause.",

        "termination":
        "Verify Contract Termination Conditions.",

        "experience":
        "Check Experience Requirements."

}

CHECKLIST_ITEMS = {

        "payment":
        "Review Payment Terms",

        "eligibility":
        "Verify Eligibility",

        "emd":
        "Verify EMD",

        "technical":
        "Check Technical Specifications",

        "delivery":
        "Verify Delivery Timeline",

        "warranty":
        "Review Warranty",

        "experience":
        "Verify Experience Criteria",

        "contract":
        "Review Contract Conditions"
}

from backend.services.weight_service import get_clause_weight

# =========================================================
# Generate Clause Recommendations
# =========================================================

def generate_clause_recommendations(clause_results):
    """
    Generate recommendation for every clause.

    Returns
    -------
    list
    """

    recommendations = []

    for clause in clause_results:

        similarity = clause.get("similarity", 0)

        weight = get_clause_weight(clause.get("clause", ""))

        risk = clause.get("risk", {}).get("level", "Very Low Risk")

        # ------------------------------------
        # Recommendation
        # ------------------------------------

        if weight >= 10:

            if similarity < 80:

                action = ("Critical clause. Immediate manual verification required.")

            else:

                action = ("Critical clause appears acceptable. Verify before submission.")

        elif weight >= 8:

            if similarity < 75:

                action = ("Review this important clause carefully.")

            else:

                action = ("Minor verification recommended.")

        elif weight >= 5:

            action = ("General review recommended.")

        else:

            action = ("Low priority clause. Review if necessary.")

        recommendations.append({

            "clause": clause.get("clause", ""),

            "similarity": similarity,

            "weight": weight,

            "risk": risk,

            "recommendation": action

        })

    return recommendations

# =========================================================
# Priority Actions
# =========================================================

def generate_priority_actions(clause_results):
    """
    Generate highest priority actions.

    Returns
    -------
    list
    """

    actions = []

    for clause in clause_results:

        if clause.get("similarity", 0) >= 80:

            continue

        text = clause.get("clause", "").lower()

        for keyword, action in PRIORITY_ACTIONS.items():

            if keyword in text:

                if action not in actions:

                    actions.append(action)
                    
    return actions

# =========================================================
# Submission Checklist
# =========================================================

def generate_submission_checklist(clause_results):
    """
    Generate submission checklist.

    Returns
    -------
    list
    """

    checklist = []

    completed = set()

    for clause in clause_results:

        text = clause.get("clause", "").lower()

        for keyword, item in CHECKLIST_ITEMS.items():

            if keyword in text and item not in completed:

                checklist.append({

                    "task": item,

                    "status": "Pending"

                })

                completed.add(item)

    return checklist

# =========================================================
# Final Recommendation
# =========================================================

def generate_final_recommendation(result, ai_summary):
    """
    Generate final executive recommendation.

    Returns
    -------
    str
    """

    similarity = result.get("weighted_similarity", 0)

    risk = ai_summary.get("risk_level", "Low Risk")

    if risk == "Critical":

        return (
            "Significant differences were identified in critical "
            "contractual clauses. Submission is not recommended "
            "until these clauses are carefully verified."
        )

    elif similarity >= 90:

        return (
            "The compared tenders are highly similar. "
            "Only a brief manual verification of critical clauses "
            "is recommended before submission."
        )

    elif similarity >= 75:

        return (
            "The tenders demonstrate strong similarity. "
            "Review payment terms, eligibility criteria, "
            "and delivery conditions before submission."
        )

    elif similarity >= 50:

        return (
            "The tenders show moderate similarity. "
            "A detailed manual review of important clauses "
            "is strongly recommended."
        )

    else:

        return (
            "The compared tenders differ substantially. "
            "Perform a complete clause-by-clause review "
            "before making any procurement decision."
        )

# =========================================================
# Recommendation Summary
# =========================================================

def generate_recommendation_summary(result, ai_summary):
    """
    Generate complete recommendation package.

    Returns
    -------
    dict
    """

    clause_results = result.get("clause_results", [])

    clause_recommendations = generate_clause_recommendations(clause_results)

    priority_actions = generate_priority_actions(clause_results)

    submission_checklist = generate_submission_checklist(clause_results)

    final_recommendation = generate_final_recommendation(result, ai_summary)

    return {

        "clause_recommendations": clause_recommendations,

        "priority_actions": priority_actions,

        "submission_checklist": submission_checklist,

        "final_recommendation": final_recommendation

    }