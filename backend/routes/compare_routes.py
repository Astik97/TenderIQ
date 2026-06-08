from flask import Blueprint
from flask import request

compare_bp = Blueprint('compare',__name__)

@compare_bp.route('/compare',methods=['POST'])
def compare():
    selected = request.form.getlist('selected_tenders')

    return f"""Selected Tender IDs:{selected}"""