from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect
)

from backend.utils.db import get_connection
from backend.services.compare_service import compare_tenders
from backend.services.report_service import generate_report

compare_bp = Blueprint('compare',__name__)

@compare_bp.route('/compare',methods=['POST'])
def compare():

    selected = request.form.getlist(
        'selected_tenders'
    )

    if len(selected) != 2:

        flash("Please select exactly two tenders.", "error")
        
        return redirect('/dashboard')

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT tender_name, extracted_text
    FROM tenders
    WHERE id=%s
    """

    cursor.execute(query, (selected[0],))
    row1 = cursor.fetchone()

    tender_name1 = row1[0]
    text1 = row1[1]

    cursor.execute(query, (selected[1],))
    row2 = cursor.fetchone()

    tender_name2 = row2[0]
    text2 = row2[1]

    cursor.close()
    conn.close()

    similarity = compare_tenders(
        text1,
        text2
    )

    # tender_name1 = tender_name1,
    # tender_name2 = tender_name2,

    report = generate_report(
        tender_name1,
        tender_name2,
        similarity
    )

    return render_template(
        "compare.html",
        similarity=similarity,
        tender1=tender_name1,
        tender2=tender_name2,
        report=report
    )
