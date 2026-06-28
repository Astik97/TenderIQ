import os
from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import request
from werkzeug.utils import secure_filename
from backend.utils.db import get_connection
from backend.services.document_service import (
    extract_pdf,
    extract_docx,
    extract_txt
)
from backend.services.text_preprocessing import clean_text
from backend.services.clause_extraction import extract_clauses

tender_bp = Blueprint("tender", __name__)

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

# -------------------------------------------------
# Dashboard
# -------------------------------------------------

@tender_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, tender_name
        FROM tenders
        WHERE user_id=%s
    """, (session["user_id"],))

    tenders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        tenders=tenders
    )

# -------------------------------------------------
# Upload Tender Files
# -------------------------------------------------

@tender_bp.route("/upload", methods=["POST"])
def upload():

    if "user_id" not in session:
        return redirect("/login")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    files = request.files.getlist("tender_files")

    conn = get_connection()
    cursor = conn.cursor()

    uploaded_files = []
    duplicate_files = []
    invalid_files = []

    for file in files:

        # -----------------------------
        # Skip empty filename
        # -----------------------------

        if file.filename == "":
            continue

        filename = secure_filename(file.filename)

        # -----------------------------
        # Check duplicate in database
        # -----------------------------

        cursor.execute("""
            SELECT id
            FROM tenders
            WHERE user_id=%s
            AND tender_name=%s
        """,
        (
            session["user_id"],
            filename
        ))

        existing = cursor.fetchone()

        if existing:
            duplicate_files.append(filename)
            print(f"{filename} already exists.")
            continue

        # -----------------------------
        # Check file extension
        # -----------------------------

        extension = filename.split(".")[-1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            invalid_files.append(filename)
            print(f"{filename} is not supported.")
            continue

        # -----------------------------
        # Save file
        # -----------------------------

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        # -----------------------------
        # Extract text
        # -----------------------------

        if extension == "pdf":
            raw_text = extract_pdf(filepath)

        elif extension == "docx":
            raw_text = extract_docx(filepath)

        elif extension == "txt":
            raw_text = extract_txt(filepath)

        else:
            raw_text = ""

        # -----------------------------
        # Text Preprocessing
        # -----------------------------

        extracted_text = clean_text(raw_text)

        # -----------------------------
        # Clause Extraction
        # -----------------------------

        clauses = extract_clauses(raw_text)

        # -----------------------------
        # Debug Output
        # -----------------------------

        print("\n========== CLEANED TEXT ==========\n")
        print(extracted_text)

        print("\n========== EXTRACTED CLAUSES ==========\n")

        for clause, content in clauses.items():

            print(clause)

            print("-" * 40)

            print(content)

            print("=" * 60)

        # -----------------------------
        # Store in Database
        # -----------------------------

        query = """
        INSERT INTO tenders
        (
            user_id,
            tender_name,
            file_name,
            extracted_text
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            query,
            (
                session["user_id"],
                filename,
                filename,
                extracted_text
            )
        )

        uploaded_files.append(filename)

    conn.commit()

    cursor.close()

    conn.close()

    # -----------------------------
    # Upload Summary
    # -----------------------------

    print("\n===============================")

    print("UPLOAD SUMMARY")

    print("===============================\n")

    if uploaded_files:
        print("Uploaded Files")
    for file in uploaded_files:
        print("✔", file)
    print()

    if duplicate_files:
        print("Duplicate Files")
    for file in duplicate_files:
        print("✖", file)
    print()
    
    if invalid_files:
        print("Invalid Files")
    for file in invalid_files:
        print("✖", file)
    print()

    if not uploaded_files and not duplicate_files and not invalid_files:
        print("No files were processed.")

    print()

    return redirect("/dashboard")
