"""
=========================================================
TenderIQ Report Service
---------------------------------------------------------
Responsible for

1. Executive Summary
2. Statistics
3. Clause Analysis
4. Risk Summary
5. Recommendations
6. Final Report Generation
=========================================================
"""

# =========================================================
# Header
# =========================================================

def generate_header(tender1_name, tender2_name):

    return f"""
=========================================================
TenderIQ AI Comparison Report
=========================================================

Tender 1

{tender1_name}

Tender 2

{tender2_name}

=========================================================
"""

# =========================================================
# Executive Summary
# =========================================================

def generate_summary(comparison):

    similarity = comparison["similarity"]

    level = comparison["level"]

    if similarity >= 90:

        conclusion = "Highly Similar Documents"

        recommendation = (
            "These tenders are almost identical.\n"
            "Only a quick manual verification is recommended."
        )

    elif similarity >= 70:

        conclusion = "Good Overall Match"

        recommendation = (
            "Most clauses match successfully.\n"
            "Review financial and commercial clauses."
        )

    elif similarity >= 50:

        conclusion = "Moderately Similar Documents"

        recommendation = (
            "Several clauses differ.\n"
            "Carefully review eligibility and technical sections."
        )

    elif similarity >= 30:

        conclusion = "Low Similarity"

        recommendation = (
            "Large differences detected.\n"
            "Detailed manual verification is recommended."
        )

    else:

        conclusion = "Very Low Similarity"

        recommendation = (
            "The tenders differ significantly.\n"
            "Perform a complete clause-by-clause review."
        )

    return f"""
Overall Similarity

{similarity} %

Overall Match

{level}

=========================================================

Conclusion

{conclusion}

=========================================================

Recommendation

{recommendation}

=========================================================
"""

# =========================================================
# Statistics
# =========================================================

def generate_statistics(comparison):

    clause_results = comparison["clause_results"]

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    excellent = 0
    good = 0
    moderate = 0
    low = 0
    poor = 0

    for clause in clause_results:

        risk = clause["risk"]["level"]

        match = clause["level"]

        if risk == "Critical Risk":
            high_risk += 1

        elif risk == "High Risk":
            high_risk += 1

        elif risk == "Medium Risk":
            medium_risk += 1

        else:
            low_risk += 1

        if match == "Excellent Match":
            excellent += 1

        elif match == "Good Match":
            good += 1

        elif match == "Moderate Match":
            moderate += 1

        elif match == "Low Match":
            low += 1

        else:
            poor += 1

    return f"""
Statistics

Total Clauses

{comparison["total_clauses"]}

Matched Clauses

{comparison["matched_clauses"]}

Excellent Matches

{excellent}

Good Matches

{good}

Moderate Matches

{moderate}

Low Matches

{low}

Poor Matches

{poor}

High Risk Clauses

{high_risk}

Medium Risk Clauses

{medium_risk}

Low Risk Clauses

{low_risk}

=========================================================
"""

# =========================================================
# Clause Analysis
# =========================================================

def generate_clause_analysis(comparison):

    report = "\nClause Analysis\n"

    for index, clause in enumerate(
        comparison["clause_results"],
        start=1
    ):

        difference = clause["difference"]

        risk = clause["risk"]

        added = ", ".join(difference["added"][:5])

        if len(difference["added"]) > 5:
            added += "..." 
        else:
            "None"

        removed = ", ".join(difference["removed"][:5])

        if len(difference["removed"]) > 5:
            removed += "..."
        else:
            "None"

        report += f"""

----------------------------------------------------
Clause {index}
----------------------------------------------------

Original Clause

{clause["clause"]}

Matched Clause

{clause["best_match"]}

Similarity

{clause["similarity"]} %

Match Level

{clause["level"]}

Difference Summary

{difference["summary"]}

Added Keywords

{added}

Removed Keywords

{removed}

==================== RISK ====================

Risk Score

{risk["score"]}

Risk Level

{risk["level"]}

Risk Reason

{risk["reason"]}

Recommendation

{risk["recommendation"]}

====================================================
"""

    return report

# =========================================================
# Footer
# =========================================================

def generate_footer(comparison):

    return f"""

=========================================================

Total Clauses Compared

{comparison["matched_clauses"]}

Overall Similarity

{comparison["similarity"]} %

=========================================================

End of Report

=========================================================
"""

# =========================================================
# Main Generator
# =========================================================

def generate_report(

    tender1_name,

    tender2_name,

    comparison

):

    report = ""

    report += generate_header(

        tender1_name,

        tender2_name

    )

    report += generate_summary(

        comparison

    )

    report += generate_statistics(

        comparison

    )

    report += generate_clause_analysis(

        comparison

    )

    report += generate_footer(

        comparison

    )

    return report