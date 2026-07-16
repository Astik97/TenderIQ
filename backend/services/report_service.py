"""
=========================================================
TenderIQ Report Service
=========================================================

Responsibilities

1. Generate Overall Report
2. Generate Clause Analysis
3. Generate Recommendation
4. Return Complete Report
=========================================================
"""

# =========================================================
# Report Header
# =========================================================

def generate_header():

    return (
        "\n"
        "=========================================================\n"
        "TenderIQ AI Comparison Report\n"
        "=========================================================\n"
    )


# =========================================================
# Executive Summary
# =========================================================

def generate_summary(
        tender1,
        tender2,
        comparison
):

    summary = (
        f"\nTender 1 : {tender1}\n"
        f"Tender 2 : {tender2}\n\n"
        f"Overall Similarity : {comparison['similarity']}%\n"
        f"Overall Match      : {comparison['level']}\n"
    )

    return summary

# =========================================================
# Statistics
# =========================================================

def generate_statistics(comparison):

    stats = (
        "\n=========================================================\n"
        "Statistics\n"
        "=========================================================\n"
        f"Total Clauses     : {comparison['total_clauses']}\n"
        f"Matched Clauses   : {comparison['matched_clauses']}\n"
        f"Overall Similarity: {comparison['similarity']}%\n"
    )

    return stats

# =========================================================
# Clause Analysis
# =========================================================

def generate_clause_analysis(comparison):

    report = (
        "\n=========================================================\n"
        "Clause Analysis\n"
        "=========================================================\n"
    )

    for index, clause in enumerate(
        comparison["clause_results"],
        start=1
    ):

        difference = clause["difference"]

        report += (
            f"\n---------------------------------------------------------\n"
            f"Clause {index}\n"
            f"---------------------------------------------------------\n"

            f"Original Clause\n"
            f"{clause['clause']}\n\n"

            f"Best Match\n"
            f"{clause['best_match']}\n\n"

            f"Similarity\n"
            f"{clause['similarity']}%\n\n"

            f"Match Level\n"
            f"{clause['level']}\n\n"

            f"Changed\n"
            f"{difference['changed']}\n\n"

            f"Added\n"
            f"{', '.join(difference['added']) if difference['added'] else 'None'}\n\n"

            f"Removed\n"
            f"{', '.join(difference['removed']) if difference['removed'] else 'None'}\n\n"

            f"Difference Summary\n"
            f"{difference['summary']}\n"
        )

    return report


# =========================================================
# Overall Conclusion
# =========================================================

def get_conclusion(similarity):

    if similarity >= 90:
        return "Excellent Match"

    elif similarity >= 70:
        return "Good Match"

    elif similarity >= 50:
        return "Moderate Match"

    elif similarity >= 30:
        return "Low Match"
    
    else:
        return "Poor Match"

# =========================================================
# Recommendation
# =========================================================

def generate_recommendation(comparison):

    score = comparison["similarity"]

    if score >= 90:

        recommendation = (
            "Excellent Match.\n"
            "Only minor verification is recommended."
        )

    elif score >= 70:

        recommendation = (
            "Good Match.\n"
            "Review important commercial clauses."
        )

    elif score >= 50:

        recommendation = (
            "Moderate Match.\n"
            "Carefully review technical and eligibility sections."
        )

    elif score >= 30:

        recommendation = (
            "Low Match.\n"
            "Significant manual review is recommended."
        )

    else:

        recommendation = (
            "Poor match.\n"
            "These tenders appear substantially different."
        )

    return (
        f"{recommendation}\n"
    )
    
# =========================================================
# Clause Report
# =========================================================

def generate_clause_report(clause_results):

    report = ""

    for index, clause in enumerate(clause_results, start=1):

        difference = clause["difference"]

        report += f"""
----------------------------------------------------
Clause {index}
----------------------------------------------------

Original Clause

{clause['clause']}

Best Match

{clause['best_match']}

Similarity

{clause['similarity']} %

Level

{clause['level']}

Changed

{difference['changed']}

Added

{', '.join(difference["added"]) if difference["added"] else "None"}

Removed

{', '.join(difference["removed"]) if difference["removed"] else "None"}

Difference Summary

{difference["summary"]}
"""
   
    return report

# =========================================================
# Main Report Generator
# =========================================================

def generate_report(

        tender1_name,
        tender2_name,
        comparison_result
    ):

    similarity = comparison_result["similarity"]

    clause_results = comparison_result["clause_results"]

    conclusion = get_conclusion(similarity)

    recommendation = generate_recommendation(comparison_result)

    clause_report = generate_clause_report(clause_results)

    report = f"""
=========================================================
TenderIQ AI Comparison Report
=========================================================

Tender 1

{tender1_name}

Tender 2

{tender2_name}

=========================================================

Overall Similarity

{similarity} %

Overall Match

{comparison_result['level']}

=========================================================

Conclusion

{conclusion}

=========================================================

Recommendation

{recommendation}

=========================================================

Clause Analysis

{clause_report}

=========================================================

Total Clauses Compared

{comparison_result['matched_clauses']}

=========================================================
End of Report
=========================================================
"""

    return report