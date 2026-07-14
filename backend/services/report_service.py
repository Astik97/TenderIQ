"""
=========================================================
TenderIQ
Report Service
Milestone 5
=========================================================

Responsibilities

1. Generate Overall Report
2. Generate Clause Analysis
3. Generate Recommendation
4. Return Complete Report
=========================================================
"""

# =========================================================
# Overall Conclusion
# =========================================================

def get_conclusion(similarity):

    if similarity >= 80:
        return "Highly Similar Documents"

    elif similarity >= 60:
        return "Moderately Similar Documents"

    elif similarity >= 40:
        return "Low Similarity"

    else:
        return "Very Different Documents"

# =========================================================
# Recommendation
# =========================================================

def get_recommendation(similarity):

    if similarity >= 80:

        return (
            "Both tenders are highly similar. "
            "They can be reused with only minor modifications."
        )

    elif similarity >= 60:

        return (
            "Many requirements overlap, "
            "but several important differences exist."
        )

    elif similarity >= 40:

        return (
            "Only a limited number of clauses match. "
            "A detailed review is recommended."
        )

    else:

        return (
            "These tenders appear to serve different purposes. "
            "Reuse is not recommended."
        )

# =========================================================
# Clause Report
# =========================================================

def generate_clause_report(clause_results):

    report = ""

    for index, clause in enumerate(clause_results, start=1):

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

    recommendation = get_recommendation(similarity)

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