"""
=========================================================
TenderIQ Compare Service
=========================================================
"""

from flask import(Blueprint,request,render_template,flash,redirect,session)

from backend.services.chart_service import (generate_chart_data)

from backend.services.recommendation_service import (generate_recommendation_summary)

from backend.services.analytics_service import (generate_analytics)

from backend.services.ranking_service import (
    get_highest_matching_clauses,
    get_highest_risk_clauses,
    get_lowest_matching_clauses,
    get_ranking_summary
)

from backend.utils.db import get_connection

from backend.services.compare_service import compare_tenders

from backend.services.report_service import generate_report

compare_bp = Blueprint("compare",__name__)

@compare_bp.route("/compare", methods=["POST"])
def compare():

    # -----------------------------------------
    # Get Selected Tender IDs
    # -----------------------------------------

    selected = request.form.getlist("selected_tenders")

    if len(selected) != 2:

        flash("Please select exactly two tenders.","error")

        return redirect("/dashboard")

    conn = None
    
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor()

        query = """
        SELECT
        tender_name,
        extracted_text
        FROM tenders
        WHERE id=%s
        """

        # -----------------------------
        # Tender 1
        # -----------------------------

        cursor.execute(query,(selected[0],))

        row1 = cursor.fetchone()

        if row1 is None:

            flash("First tender not found.","error")

            return redirect("/dashboard")

        tender_name1 = row1[0]

        text1 = row1[1]

        # -----------------------------
        # Tender 2
        # -----------------------------

        cursor.execute(query,(selected[1],))

        row2 = cursor.fetchone()

        if row2 is None:

            flash("Second tender not found.","error")

            return redirect("/dashboard")

        tender_name2 = row2[0]

        text2 = row2[1]

    except Exception as e:

        flash(f"Database Error : {e}","error")

        return redirect("/dashboard")

    # -----------------------------------------
    # Compare
    # -----------------------------------------

    comparison = compare_tenders(text1,text2)

    clause_results = comparison["clause_results"]

    # -----------------------------------------
    # Ranking Service
    # -----------------------------------------

    highest_matches = get_highest_matching_clauses(clause_results)

    highest_risks = get_highest_risk_clauses(clause_results)

    lowest_matches = get_lowest_matching_clauses(clause_results)

    ranking_summary = get_ranking_summary(clause_results)

    # -----------------------------------------
    # AI Summary
    # -----------------------------------------
    
    ai_summary = comparison["ai_summary"]

    # -----------------------------------------
    # Recommendation Summary
    # -----------------------------------------

    recommendation_summary = generate_recommendation_summary(comparison, ai_summary)

    # -----------------------------------------
    # Analytics
    # -----------------------------------------

    analytics = generate_analytics(comparison)

    # -----------------------------------------
    # Chart Data
    # -----------------------------------------

    chart_data = generate_chart_data(comparison,analytics)

    # -----------------------------------------
    # Comparison Result
    # -----------------------------------------

    print("\n========== COMPARISON RESULT ==========\n")

    print(f"Similarity : {comparison['similarity']}%")
    
    print(f"Match Level : {comparison['level']}")

    print(f"Total Clauses : {comparison['total_clauses']}")

    print(f"Matched Clauses : {comparison['matched_clauses']}")

    print(f"Total Risks : {len(comparison['clause_results'])}")

    # -----------------------------------------
    # Report
    # -----------------------------------------

    report = generate_report(tender_name1,tender_name2,comparison)

    cursor.execute(
    """
    INSERT INTO comparison_reports
    (
        user_id,
        tender1_id,
        tender2_id,
        similarity_score,
        match_level,
        analysis_report
    )
    VALUES
    (%s,%s,%s,%s,%s,%s)
    """,
    (
        session["user_id"],
        selected[0],
        selected[1],
        comparison["similarity"],
        comparison["level"],
        report
    )

)
    
    conn.commit()
    
    cursor.close()

    conn.close()

    # ----------------------------------------
    # AI-Engine
    # ----------------------------------------

    ai_engine = "Sentence Transformers(all-MiniLM-L6-v2) + Cosine Similarity"

    # -----------------------------------------
    # Render Compare Page
    # -----------------------------------------

    return render_template(

        "compare.html",

        tender1=tender_name1,

        tender2=tender_name2,

        comparison=comparison,

        highest_matches=highest_matches,

        highest_risks=highest_risks,

        lowest_matches=lowest_matches,

        ranking_summary=ranking_summary,

        report=report,

        analytics=analytics,

        chart_data=chart_data,

        ai_engine=ai_engine,

        ai_summary=ai_summary,

        recommendation_summary=recommendation_summary

)