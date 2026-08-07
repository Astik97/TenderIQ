"""
=========================================================
TenderIQ Compare Routes
=========================================================
"""

from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    session
)

from backend.utils.ui_setup import(
    get_risk_badge, 
    get_risk_icon, 
    get_risk_class
)

from backend.services.ranking_service import (
    get_highest_matching_clauses,
    get_highest_risk_clauses,
    get_lowest_matching_clauses,
    get_ranking_summary
)

from backend.services.chart_service import generate_chart_data
from backend.services.recommendation_service import generate_recommendation_summary
from backend.services.analytics_service import generate_analytics_summary
from backend.utils.db import get_connection
from backend.services.compare_service import compare_tenders
from backend.services.report_service import generate_report
from backend.services.ai_summary_service import generate_ai_summary
from backend.services.insight_service import generate_complete_insight

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

    tender1_id, tender2_id = selected

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

        cursor.execute(query,(tender1_id,))

        row1 = cursor.fetchone()

        if row1 is None:

            flash("First tender not found.","error")

            return redirect("/dashboard")

        tender_name1, text1 = row1

        # -----------------------------
        # Tender 2
        # -----------------------------

        cursor.execute(query,(tender2_id,))

        row2 = cursor.fetchone()

        if row2 is None:

            flash("Second tender not found.","error")

            return redirect("/dashboard")

        tender_name2, text2 = row2

        cursor.close()
        conn.close()

        cursor = None
        conn = None

    except Exception as e:

        flash(f"Database Error : {e}","error")

        return redirect("/dashboard")

    # -----------------------------------------
    # Compare
    # -----------------------------------------

    comparison = compare_tenders(text1,text2)

    similarity = comparison.get("similarity", 0)

    match_level = comparison.get("level", "Unknown")

    total_clauses = comparison.get("total_clauses", 0)

    matched_clauses = comparison.get("matched_clauses", 0)

    clause_results = comparison.get("clause_results", [])

    for clause in clause_results:

        risk = clause.get("risk", {})

        risk_level = risk.get("level", "Very Low Risk")

        clause["risk_badge"] = get_risk_badge(risk_level)

        clause["risk_icon"] = get_risk_icon(risk_level)

        clause["risk_class"] = get_risk_class(risk_level)

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
    
    ai_summary = generate_ai_summary(comparison)

    risk_level = ai_summary.get("risk_level", "Very Low Risk")

    ai_summary["risk_badge"] = get_risk_badge(risk_level)

    ai_summary["risk_icon"] = get_risk_icon(risk_level)

    # -----------------------------------------
    # Recommendation Summary
    # -----------------------------------------

    recommendation_summary = generate_recommendation_summary(comparison, ai_summary)

    # -----------------------------------------
    # Analytics
    # -----------------------------------------

    analytics = generate_analytics_summary(comparison)

    # -----------------------------------------
    # AI Insight Engine
    # -----------------------------------------

    insight = generate_complete_insight(comparison)

    # -----------------------------------------
    # Chart Data
    # -----------------------------------------

    chart_data = generate_chart_data(comparison,analytics)

    # -----------------------------------------
    # Comparison Result
    # -----------------------------------------

    print("========== COMPARISON RESULT ==========")

    print(f"Similarity Score: {similarity}")

    print(f"Match Level: {match_level}")

    print(f"Total Clauses: {total_clauses}")

    print(f"Matched Clauses: {matched_clauses}")

    print(f"Total Risks: {len(clause_results)}")
        
    # -----------------------------------------
    # Report
    # -----------------------------------------
    try:

        report = generate_report(
            tender_name1,
            tender_name2,
            comparison
        )

    except Exception as e:

        report = "Report generation failed. Please try again later."

        flash(f"Failed to generate report: {e}", "error")

    try:

        conn = get_connection()
        cursor = conn.cursor()

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
            session.get("user_id"),
            tender1_id,
            tender2_id,
            similarity,
            match_level,
            report
        )
    )
        
        conn.commit()

    except Exception as e:

        if conn:
            
            conn.rollback()

        flash(f"Failed to save comparison report: {e}", "error")

    finally:

        if cursor:
            cursor.close()

        if conn:
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

        insight=insight,

        chart_data=chart_data,

        ai_engine=ai_engine,

        ai_summary=ai_summary,

        recommendation_summary=recommendation_summary

)