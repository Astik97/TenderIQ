from flask import Blueprint
from flask import request
from backend.utils.db import get_connection
from backend.services.compare_service import (
    compare_tenders)

compare_bp = Blueprint('compare',__name__)

@compare_bp.route('/compare',methods=['POST'])
def compare():
    
    selected = request.form.getlist('selected_tenders')

    if len(selected) != 2:

        return """
        Please select exactly
        two tenders.
        """

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT extracted_text
    FROM tenders
    WHERE id=%s
    """

    cursor.execute(query,(selected[0],))

    text1 = cursor.fetchone()[0]

    cursor.execute(query,(selected[1],))

    text2 = cursor.fetchone()[0]

    similarity = compare_tenders(text1,text2)

    return f"""Similarity Score:{similarity}%"""

    # return f"""Selected Tender IDs:{selected}"""