from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    session
)

from backend.models import comparison
from backend.utils.db import get_connection
from backend.services.compare_service import compare_tenders
from backend.services.report_service import generate_report

compare_bp = Blueprint("compare",__name__)

@compare_bp.route("/compare", methods=["POST"])
def compare():

    # -----------------------------------------
    # Get Selected Tender IDs
    # -----------------------------------------

    selected = request.form.getlist(
        "selected_tenders"
    )

    if len(selected) != 2:

        flash(
            "Please select exactly two tenders.",
            "error"
        )

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

        cursor.execute(
            query,
            (selected[0],)
        )

        row1 = cursor.fetchone()

        if row1 is None:

            flash(
                "First tender not found.",
                "error"
            )

            return redirect("/dashboard")

        tender_name1 = row1[0]

        text1 = row1[1]

        # -----------------------------
        # Tender 2
        # -----------------------------

        cursor.execute(
            query,
            (selected[1],)
        )

        row2 = cursor.fetchone()

        if row2 is None:

            flash(
                "Second tender not found.",
                "error"
            )

            return redirect("/dashboard")

        tender_name2 = row2[0]

        text2 = row2[1]

    except Exception as e:

        flash(
            f"Database Error : {e}",
            "error"
        )

        return redirect("/dashboard")

    # -----------------------------------------
    # Compare
    # -----------------------------------------

    comparison = compare_tenders(
        text1,
        text2,

    )

    print("\n========== COMPARISON RESULT ==========\n")
    
    print(comparison)
    
    similarity = comparison["similarity"]
    
    level = comparison["level"]
    
    color = comparison["color"]
    
    clause_results = comparison["clause_results"]

    # -----------------------------------------
    # Report
    # -----------------------------------------

    report = generate_report(

        tender_name1,

        tender_name2,

        comparison

    )

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
        similarity,
        level,
        report
    )
)
    
    conn.commit()
    
    cursor.close()
    conn.close()

    # -----------------------------------------
    # Render Compare Page
    # -----------------------------------------

    return render_template(

        "compare.html",

        tender1=tender_name1,

        tender2=tender_name2,

        comparison=comparison,

        similarity=similarity,

        level=level,

        color=color,

        clause_results=clause_results,

        report=report

    )