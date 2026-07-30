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
#  Risk Distribution
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
#  Calculate Risk Level
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
#  Count Match Levels
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
#  Highest Risk Clause
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
#  Major Differences
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
# Recommendation
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
#  Overall Assessment
# =========================================================

def generate_overall_assessment(result):
    """
    Generate an executive assessment paragraph.

    Returns
    -------
    str
    """

    similarity = result["similarity"]

    total = result["total_clauses"]

    matched = result["matched_clauses"]

    level = result["level"]

    if similarity >= 90:

        assessment = (
            "The two tender documents are highly consistent with only "
            "minor wording differences. Most contractual, technical and "
            "administrative clauses remain unchanged."
        )

    elif similarity >= 75:

        assessment = (
            "The tenders show good overall similarity. Most important "
            "clauses remain aligned, although a few sections require "
            "manual verification."
        )

    elif similarity >= 50:

        assessment = (
            "The tenders have moderate similarity. Several clauses differ "
            "in wording or content. A detailed manual review is recommended "
            "before making any procurement decision."
        )

    else:

        assessment = (
            "Significant differences exist between the two tenders. "
            "Multiple contractual or technical clauses have changed, "
            "requiring comprehensive review before proceeding."
        )

    return (
        f"{assessment} "
        f"The AI engine analyzed {total} clauses and matched "
        f"{matched} clauses with an overall similarity of "
        f"{similarity:.2f}% ({level})."
    )

# =========================================================
#  Key Findings
# =========================================================

def generate_key_findings(result):
    """
    Generate major AI findings.

    Returns
    -------
    list
    """

    findings = []

    findings.append(
        f"Analyzed {result['total_clauses']} clauses."
    )

    findings.append(
        f"Overall similarity is {result['similarity']:.2f}%."
    )

    findings.append(
        f"{result['matched_clauses']} clauses were successfully matched."
    )

    if result["similarity"] >= 85:

        findings.append(
            "Most contractual clauses remain unchanged."
        )

    elif result["similarity"] >= 60:

        findings.append(
            "Moderate clause differences detected."
        )

    else:

        findings.append(
            "Large structural differences detected."
        )

    return findings

# =========================================================
#  Positive Highlights
# =========================================================

def generate_positive_highlights(clause_results):
    """
    Highlight the strongest similarities.

    Returns
    -------
    list
    """

    highlights = []

    excellent = [
        clause
        for clause in clause_results
        if clause["similarity"] >= 90
    ]

    if excellent:

        highlights.append(
            f"{len(excellent)} clauses have Excellent similarity."
        )

    good = [
        clause
        for clause in clause_results
        if 75 <= clause["similarity"] < 90
    ]

    if good:

        highlights.append(
            f"{len(good)} clauses have Good similarity."
        )

    if not highlights:

        highlights.append(
            "No highly similar clauses were identified."
        )

    return highlights

# =========================================================
#  Critical Findings
# =========================================================

def generate_critical_findings(clause_results):
    """
    Identify important clause changes.

    Returns
    -------
    list
    """

    findings = []

    for clause in clause_results:

        risk = clause["risk"]["level"]

        if risk in ["Critical Risk", "High Risk"]:

            findings.append(

                f"{risk}: "

                f"{clause['clause'][:120]}..."

            )

    if not findings:

        findings.append(
            "No critical clause changes detected."
        )

    return findings[:5]

# =========================================================
#  Review Priority
# =========================================================

def generate_review_priority(clause_results):
    """
    Determine review priority.

    Returns
    -------
    dict
    """

    critical = 0

    high = 0

    medium = 0

    for clause in clause_results:

        level = clause["risk"]["level"]

        if level == "Critical Risk":

            critical += 1

        elif level == "High Risk":

            high += 1

        elif level == "Medium Risk":

            medium += 1

    if critical >= 1:

        priority = "URGENT"

        reason = (
            "Critical clause differences require immediate manual review."
        )

    elif high >= 3:

        priority = "HIGH"

        reason = (
            "Several high-risk clauses should be reviewed carefully."
        )

    elif medium >= 5:

        priority = "MEDIUM"

        reason = (
            "Moderate clause differences detected."
        )

    else:

        priority = "LOW"

        reason = (
            "Only minor differences were detected."
        )

    return {

        "priority": priority,

        "reason": reason

    }

# =========================================================
#  AI Recommendations
# =========================================================

def generate_ai_recommendations(clause_results):
    """
    Generate clause-specific recommendations.

    Returns
    -------
    list
    """

    recommendations = []

    critical_count = 0
    high_count = 0

    for clause in clause_results:

        risk = clause["risk"]["level"]

        if risk == "Critical Risk":

            critical_count += 1

        elif risk == "High Risk":

            high_count += 1

    if critical_count:

        recommendations.append(
            "Immediately review all Critical Risk clauses before submission."
        )

    if high_count:

        recommendations.append(
            "Verify payment terms, eligibility criteria and compliance requirements."
        )

    recommendations.append(
        "Review all manually modified clauses."
    )

    recommendations.append(
        "Validate technical specifications with the original tender."
    )

    recommendations.append(
        "Cross-check important contractual obligations before bidding."
    )

    return recommendations

# =========================================================
#  Confidence Score
# =========================================================

def generate_confidence_score(result):
    """
    Estimate AI confidence based on
    similarity and number of clauses.

    Returns
    -------
    float
    """

    similarity = result["similarity"]

    clauses = result["total_clauses"]

    confidence = similarity

    if clauses > 1000:

        confidence += 4

    elif clauses > 500:

        confidence += 2

    confidence = min(confidence, 99.9)

    return round(confidence, 2)

# =========================================================
#  Process Summary
# =========================================================

def generate_processing_summary(result):
    """
    Describe how the AI comparison was performed.

    Returns
    -------
    str
    """

    return (

        "Comparison performed using Sentence Transformers "

        "(all-MiniLM-L6-v2) semantic embeddings, "

        "cosine similarity optimization, clause extraction, "

        "risk analysis and AI-assisted executive summarization."

    )

# =========================================================
# Generate AI Executive Summary
# =========================================================

def generate_ai_summary(result):
    """
    Generate the complete AI Executive Summary.

    Parameters
    ----------
    result : dict
        Output returned by compare_tenders()

    Returns
    -------
    dict
    """

    clause_results = result["clause_results"]

    # -----------------------------------------------------
    # Core Analysis
    # -----------------------------------------------------

    best_clause = find_best_clause(clause_results)

    highest_risk_clause = find_highest_risk_clause(clause_results)

    risk_level = calculate_risk_level(clause_results)

    major_differences = extract_major_differences(clause_results)

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    risk_distribution = calculate_risk_distribution(clause_results)

    match_distribution = count_match_levels(clause_results)

    # -----------------------------------------------------
    # AI Insights
    # -----------------------------------------------------

    overall_assessment = generate_overall_assessment(result)

    key_findings = generate_key_findings(result)

    positive_highlights = generate_positive_highlights(clause_results)

    critical_findings = generate_critical_findings(clause_results)

    review_priority = generate_review_priority(clause_results)

    recommendation = generate_recommendation(result["similarity"],risk_level)

    recommendations = generate_ai_recommendations(clause_results)

    # -----------------------------------------------------
    # AI Metadata
    # -----------------------------------------------------

    confidence_score = generate_confidence_score(result)

    processing_summary = generate_processing_summary(result)

    # -----------------------------------------------------
    # Weighted Service
    # -----------------------------------------------------

    weighted_similarity = result["weighted_similarity"]

    weight_summary = result["weight_summary"]

    # -----------------------------------------------------
    # Final Summary
    # -----------------------------------------------------

    return {

        # ==========================================
        # Executive Overview
        # ==========================================

        "overall_similarity": result["similarity"],

        "overall_assessment": overall_assessment,

        "risk_level": risk_level,

        "confidence_score": confidence_score,

        "processing_summary": processing_summary,

        # ==========================================
        # Statistics
        # ==========================================

        "total_clauses": result["total_clauses"],

        "matched_clauses": result["matched_clauses"],

        "risk_distribution": risk_distribution,

        "match_distribution": match_distribution,

        # ==========================================
        # Clause Analysis
        # ==========================================

        "highest_matching_clause": best_clause,

        "highest_risk_clause": highest_risk_clause,

        "major_differences": major_differences,

        # ==========================================
        # AI Findings
        # ==========================================

        "key_findings": key_findings,

        "positive_highlights": positive_highlights,

        "critical_findings": critical_findings,

        # ==========================================
        # Weighted Service
        # ==========================================

        "weighted_similarity": weighted_similarity,

        "weight_summary": weight_summary,

        "difference_percentage": weight_summary["difference_percentage"],

        # ==========================================
        # Review & Recommendation
        # ==========================================

        "review_priority": review_priority,

        "recommendation": recommendation,

        "recommendations": recommendations

    }