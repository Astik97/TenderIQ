"""
=========================================================
TenderIQ Insight Service
---------------------------------------------------------
Responsible For

1. Strength Detection
2. Weakness Detection
3. Top Changes
4. Procurement Risk Summary
5. AI Insights
6. Final Recommendation
7. Tender Decision
8. Complete Insight Package
=========================================================
"""

def generate_strengths(clause_results):
    """
    Generate strengths of the compared tenders.
    """

    strengths = []

    excellent = [
        clause for clause in clause_results
        if clause["similarity"] >= 90
    ]

    if excellent:
        strengths.append(
            f"{len(excellent)} clauses are almost identical."
        )

    technical = [
        clause for clause in clause_results
        if clause["similarity"] >= 80
    ]

    if len(technical) >= 5:
        strengths.append(
            "Technical requirements are highly aligned."
        )

    low_risk = [
        clause for clause in clause_results
        if clause["risk"]["level"] in
        ["Very Low Risk", "Low Risk"]
    ]

    if len(low_risk) >= len(clause_results) * 0.7:
        strengths.append(
            "Most clauses have low procurement risk."
        )

    if not strengths:
        strengths.append(
            "No major strengths identified."
        )

    return strengths

def generate_weaknesses(clause_results):
    """
    Generate weaknesses.
    """

    weaknesses = []

    changed = [
        clause for clause in clause_results
        if clause["similarity"] < 60
    ]

    if changed:
        weaknesses.append(
            f"{len(changed)} clauses differ significantly."
        )

    high_risk = [
        clause for clause in clause_results
        if clause["risk"]["level"] in
        ["High Risk", "Critical Risk"]
    ]

    if high_risk:
        weaknesses.append(
            f"{len(high_risk)} clauses require manual review."
        )

    if not weaknesses:
        weaknesses.append(
            "No significant weaknesses detected."
        )

    return weaknesses

def generate_top_changes(clause_results, top_n=5):
    """
    Return clauses with the largest changes.
    """

    sorted_changes = sorted(
        clause_results,
        key=lambda x: x["similarity"]
    )

    results = []

    for clause in sorted_changes[:top_n]:

        results.append({

            "clause": clause["clause"][:80] + "...",

            "similarity": clause["similarity"],

            "risk": clause["risk"]["level"],

            "summary": clause["difference"]["summary"]

        })

    return results

def generate_procurement_risk_summary(clause_results):
    """
    Overall procurement risk.
    """

    high = 0
    critical = 0

    for clause in clause_results:

        level = clause["risk"]["level"]

        if level == "High Risk":
            high += 1

        elif level == "Critical Risk":
            critical += 1

    if critical >= 3:

        overall = "High"

    elif high >= 5:

        overall = "Medium"

    else:

        overall = "Low"

    return {

        "overall": overall,

        "high": high,

        "critical": critical

    }

def generate_ai_insights(comparison):
    """
    AI-generated observations.
    """

    similarity = comparison["similarity"]

    insights = []

    if similarity >= 90:

        insights.append(
            "Both tenders are highly similar."
        )

    elif similarity >= 70:

        insights.append(
            "Most technical clauses remain unchanged."
        )

    elif similarity >= 50:

        insights.append(
            "Several important clauses require review."
        )

    else:

        insights.append(
            "The tenders differ substantially."
        )

    insights.append(
        f"{comparison['matched_clauses']} clauses matched successfully."
    )

    return insights

def generate_final_recommendation(
    comparison,
    procurement_risk
):
    """
    Final recommendation.
    """

    similarity = comparison["similarity"]

    risk = procurement_risk["overall"]

    if similarity >= 90 and risk == "Low":

        return (
            "Safe to reuse this tender with minimal review."
        )

    if similarity >= 70:

        return (
            "Suitable for submission after reviewing changed clauses."
        )

    if similarity >= 50:

        return (
            "Manual verification is strongly recommended."
        )

    return (
        "Do not reuse without complete legal and technical review."
    )

def generate_tender_decision(
    comparison,
    procurement_risk
):
    """
    Final AI decision.
    """

    similarity = comparison["similarity"]

    risk = procurement_risk["overall"]

    if similarity >= 90 and risk == "Low":

        return "Safe to Bid"

    if similarity >= 70:

        return "Bid with Modifications"

    if similarity >= 50:

        return "High Risk"

    return "Not Recommended"

def generate_complete_insight(comparison):
    """
    Generate complete insight package.
    """

    clause_results = comparison["clause_results"]

    procurement_risk = generate_procurement_risk_summary(
        clause_results
    )

    return {

        "strengths":
        generate_strengths(clause_results),

        "weaknesses":
        generate_weaknesses(clause_results),

        "top_changes":
        generate_top_changes(clause_results),

        "procurement_risk":
        procurement_risk,

        "ai_insights":
        generate_ai_insights(comparison),

        "final_recommendation":
        generate_final_recommendation(
            comparison,
            procurement_risk
        ),

        "tender_decision":
        generate_tender_decision(
            comparison,
            procurement_risk
        )

    }