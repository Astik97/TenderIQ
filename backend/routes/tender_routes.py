from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
import os
from flask import request
from backend.utils.db import get_connection

tender_bp = Blueprint('tender', __name__)

@tender_bp.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT id,tender_name
                   FROM tenders WHERE user_id=%s """,
                   (session['user_id'],))
    
    tenders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard.html',tenders=tenders)

@tender_bp.route('/upload', methods=['POST'])
def upload():

    if 'user_id' not in session:
        return redirect('/login')
    
    files = request.files.getlist('tender_files')
    os.makedirs('uploads', exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    for file in files:
        if file.filename == '':
            continue

        filepath = os.path.join('uploads',file.filename)
        file.save(filepath)

        query = """
        INSERT INTO tenders 
        (user_id, tender_name,file_name) 
        VALUES (%s,%s,%s)
        """
        cursor.execute(query,(session['user_id'],file.filename,filepath))

    conn.commit()

    cursor.close()
    conn.close()
    
    return redirect('/dashboard')