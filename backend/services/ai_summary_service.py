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

MAX_DISPLAY_ITEMS = 5

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
    Calculate overall project risk based on clause level risks.
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

    return max(clause_results,
        key=lambda x: x.get("similarity", 0))

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

    return max(clause_results,
        key=lambda x: priority.get(x.get("risk", {}).get("level", "Low"), 0)
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

        if len(differences) >= MAX_DISPLAY_ITEMS:

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

    similarity = result.get("similarity", 0)

    total = result.get("total_clauses", 0)

    matched = result.get("matched_clauses", 0)

    level = result.get("level","Unknown")

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

    findings = [
    f"Analyzed {result.get('total_clauses', 0)} clauses.",
    f"Overall similarity is {result.get('similarity', 0):.2f}%.",
    f"{result.get('matched_clauses', 0)} clauses were successfully matched."
]
    overall_similarity = result.get("similarity", 0)

    if overall_similarity >= 85:

        findings.append("Most contractual clauses remain unchanged.")

    elif overall_similarity >= 60:

        findings.append("Moderate clause differences detected.")

    else:

        findings.append("Large structural differences detected.")

    return findings

# =========================================================
# Positive Highlights
# =========================================================

def generate_positive_highlights(result):
    """
    Generate positive business highlights.

    Returns
    -------
    list
    """

    clause_results = result.get("clause_results", [])

    overall_similarity = result.get("similarity", 0)

    weighted_similarity = result.get("weighted_similarity", 0)

    highlights = []

    excellent = 0
    good = 0

    for clause in clause_results:

        similarity = clause.get("similarity", 0)

        if similarity >= 90:
            excellent += 1

        elif similarity >= 75:
            good += 1

    # Overall Similarity
    if overall_similarity >= 90:

        highlights.append(
            "Excellent overall similarity between both tenders."
        )

    elif overall_similarity >= 75:

        highlights.append(
            "Strong semantic similarity across most clauses."
        )

    # Weighted Similarity
    if weighted_similarity >= 85:

        highlights.append(
            "High-priority business clauses are well aligned."
        )

    # Clause Match Statistics
    if excellent > 0:

        highlights.append(
            f"{excellent} clauses achieved Excellent similarity."
        )

    if good > 0:

        highlights.append(
            f"{good} clauses achieved Good similarity."
        )

    if not highlights:

        highlights.append(
            "No significant positive highlights were identified."
        )

    return highlights[:MAX_DISPLAY_ITEMS]

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

        risk = clause.get("risk", {}).get("level", "Low")

        if risk in ["Critical Risk", "High Risk"]:

            findings.append(f"{risk}: "

                f"{clause['clause'][:120]}...")

    if not findings:

        findings.append("No critical clause changes detected.")

    return findings[:MAX_DISPLAY_ITEMS]

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

        level = clause.get("risk", {}).get("level", "Low")

        if level == "Critical Risk":

            critical += 1

        elif level == "High Risk":

            high += 1

        elif level == "Medium Risk":

            medium += 1

    if critical >= 1:

        priority = "URGENT"

        reason = ("Critical clause differences require immediate manual review.")

    elif high >= 3:

        priority = "HIGH"

        reason = ("Several high-risk clauses should be reviewed carefully.")

    elif medium >= 5:

        priority = "MEDIUM"

        reason = ("Moderate clause differences detected.")

    else:

        priority = "LOW"

        reason = ("Only minor differences were detected.")

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

        risk = clause.get("risk", {}).get("level", "Low")

        if risk == "Critical Risk":

            critical_count += 1

        elif risk == "High Risk":

            high_count += 1

    if critical_count:

        recommendations.append("Immediately review all Critical Risk clauses before submission.")

    if high_count:

        recommendations.append("Verify payment terms,"
        "eligibility criteria and compliance requirements.")

    recommendations.extend([
    "Review all manually modified clauses.",
    "Validate technical specifications with the original tender.",
    "Cross-check important contractual obligations before bidding."
])

    return recommendations

# =========================================================
#  Confidence Score
# =========================================================

def generate_confidence_score(result,
        weighted_similarity):
    """
    Estimate AI confidence using:

    - Overall Similarity
    - Weighted Similarity
    - Number of Clauses
    
    It is based on similarity and number of clauses.

    Returns
    -------
    float
    """

    total_clauses = result.get("total_clauses", 0)

    matched_clauses = result.get("matched_clauses", 0)

    if total_clauses:

        clause_coverage = (matched_clauses / total_clauses) * 100

    else:

        clause_coverage = 0

    confidence = (weighted_similarity * 0.70 + clause_coverage * 0.30)

    confidence = max(60, min(confidence, 99.9))

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

    clause_results = result.get("clause_results", [])

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

    positive_highlights = generate_positive_highlights(result)

    critical_findings = generate_critical_findings(clause_results)

    review_priority = generate_review_priority(clause_results)

    recommendation = generate_recommendation(result.get("similarity", 0),risk_level)

    recommendations = generate_ai_recommendations(clause_results)

    # -----------------------------------------------------
    # Weighted Service
    # -----------------------------------------------------

    weighted_similarity = result.get("weighted_similarity", 0)

    weight_summary = result.get("weight_summary", {})

    # -----------------------------------------------------
    # AI Metadata
    # -----------------------------------------------------

    confidence_score = generate_confidence_score(result,weighted_similarity)

    processing_summary = generate_processing_summary(result)

    # -----------------------------------------
    # Summary Cards
    # -----------------------------------------

    summary_cards = [

    {
        "title": "Document Difference",
        "value": f"{weight_summary.get('difference_percentage', 0)}%"
    },

    {
        "title": "Critical Clauses",
        "value": f"{weight_summary.get('critical_clauses', 0)}/{result.get('total_clauses', 0)}",
        "small": f"{weight_summary.get('critical_percentage', 0)}%"
    },

    {
        "title": "High Priority Clauses",
        "value": weight_summary.get("high_priority_clauses", 0)
    },

    {
        "title": "Medium Priority Clauses",
        "value": weight_summary.get("medium_priority_clauses", 0)
    },

    {
        "title": "Low Priority Clauses",
        "value": weight_summary.get("low_priority_clauses", 0)
    },

    {
        "title": "Risk Level",
        "value": risk_level
    }

]

    # -----------------------------------------------------
    # Dashboard Statistics Cards
    # -----------------------------------------------------

    dashboard_cards = [

        {
            "title": "Weighted Similarity",
            "value": f"{weighted_similarity}%"
        },

        {
            "title": "Total Clauses",
            "value": result.get("total_clauses", 0)
        },

        {
            "title": "Matched Clauses",
            "value": result.get("matched_clauses", 0)
        },

        {
            "title": "Confidence Score",
            "value": f"{confidence_score}%"
        }

    ]
    
    # -----------------------------------------------------
    # Final Summary
    # -----------------------------------------------------

    return {

        # ==========================================
        # Executive Overview
        # ==========================================

        "overall_similarity": result.get("similarity", 0),

        "overall_assessment": overall_assessment,

        "risk_level": risk_level,

        "confidence_score": confidence_score,

        "processing_summary": processing_summary,

        # ==========================================
        # Statistics
        # ==========================================

        "total_clauses": result.get("total_clauses", 0),

        "matched_clauses": result.get("matched_clauses", 0),

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

        "difference_percentage": weight_summary.get("difference_percentage", 0),

        # ==========================================
        # Review & Recommendation
        # ==========================================

        "review_priority": review_priority,

        "recommendation": recommendation,

        "recommendations": recommendations,

        # ==========================================
        # Dynamic Cards
        # ==========================================

        "summary_cards": summary_cards,

        "dashboard_cards":dashboard_cards

    }