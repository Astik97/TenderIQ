import os
import uuid
from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from backend.utils.db import get_connection
from backend.services.document_service import (
    extract_pdf,
    extract_docx,
    extract_txt
)
from backend.services.text_preprocessing import clean_text

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
        try:
            if file.filename == '':
                continue
        except Exception as e:
            print(f"Error processing file: {e}")

        unique_filename = str(uuid.uuid4()) + "_" + file.filename
        filepath = os.path.join('uploads', unique_filename)
        file.save(filepath)

        allowed_extensions = ["pdf", "docx", "txt"]

        extension = file.filename.split('.')[-1].lower()

        if extension not in allowed_extensions:
            print(f"{file.filename} is not a supported file type.")
            continue

        if extension == "pdf":
            extracted_text = extract_pdf(filepath)
        
        elif extension == "docx":
            extracted_text = extract_docx(filepath)
            
        elif extension == "txt":
            extracted_text = extract_txt(filepath)

        else:
            extracted_text = ""

        extracted_text = clean_text(extracted_text)

        query = """
        INSERT INTO tenders
        (user_id,tender_name,file_name,extracted_text)
        VALUES(%s,%s,%s,%s)
        """

        cursor.execute(query,
                   (session['user_id'],
                    file.filename,
                    unique_filename,
                    extracted_text))

    conn.commit()

    cursor.close()
    conn.close()
    
    return redirect('/dashboard')