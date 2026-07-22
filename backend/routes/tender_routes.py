import os, uuid
from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    session,
    request
    )
from werkzeug.utils import secure_filename
from backend.utils.db import get_connection
from backend.services.document_service import (
    extract_pdf,
    extract_docx,
    extract_txt
)
from backend.services.text_preprocessing import clean_text
from backend.services.clause_extraction import extract_clauses, split_into_blocks

tender_bp = Blueprint("tender", __name__)

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}
def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS

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
        SELECT id, tender_name,file_name, upload_date
        FROM tenders
        WHERE user_id=%s
        ORDER BY upload_date DESC
    """, (session["user_id"],))

    tenders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        tenders=tenders
    )

@tender_bp.route('/view/<int:tender_id>')
def view_tender(tender_id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    SELECT
        tender_name,
        file_name,
        extracted_text,
        upload_date
        FROM tenders
        WHERE id=%s
        AND user_id=%s
    """

    cursor.execute(
        query,
        (tender_id, session['user_id'])
    )

    tender = cursor.fetchone()

    cursor.close()

    conn.close()

    if not tender:
        return "Tender not found."

    return render_template(
        "view_tender.html",
        tender=tender
    )

@tender_bp.route('/delete/<int:tender_id>')
def delete_tender(tender_id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT file_name
        FROM tenders
        WHERE id=%s
        AND user_id=%s
        """,
        (tender_id, session['user_id'])
    )

    result = cursor.fetchone()

    if not result:

        cursor.close()

        conn.close()

        return "Tender not found."

    filepath = os.path.join(
        "uploads",
        result[0]
    )

    if os.path.exists(filepath):

        os.remove(filepath)

    cursor.execute(
        """
        DELETE FROM tenders
        WHERE id=%s
        AND user_id=%s
        """,
        (tender_id, session['user_id'])
    )

    conn.commit()

    cursor.close()

    conn.close()

    return redirect('/dashboard')

# -------------------------------------------------
# Upload Tender Files
# -------------------------------------------------

@tender_bp.route("/upload", methods=["POST"])
def upload():

    print("\n")
    print("=" * 60)
    print("UPLOAD ROUTE HIT")
    print("=" * 60)

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

        if not allowed_file(file.filename):

            invalid_files.append(file.filename)
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

        unique_filename = str(uuid.uuid4()) + "_" + filename

        # -----------------------------
        # Save file
        # -----------------------------

        filepath = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        file.save(filepath)

        # -----------------------------
        # Extract text
        # -----------------------------

        print("=" * 80)
        print("ABOUT TO CALL extract_pdf()")
        print(filepath)
        print("=" * 80)

        if extension == "pdf":
            raw_text = extract_pdf(filepath)

        elif extension == "docx":
            raw_text = extract_docx(filepath)

        elif extension == "txt":
            raw_text = extract_txt(filepath)

        else:
            raw_text = ""

        # =============================
        # TEMPORARY DEBUG
        # =============================

        print("=" * 60)
        print("FIRST 60 LINES")
        print("=" * 60)

        lines = raw_text.split("\n")

        for i, line in enumerate(lines[:60], start=1):
            print(f"{i:02d}: {repr(line)}")

        blocks = split_into_blocks(raw_text)

        print("=" * 60)
        print("BLOCKS")
        print("=" * 60)

        print("Total Blocks:", len(blocks))

        for i, block in enumerate(blocks[:10]):

            print()

            print(f"BLOCK {i+1}")

            print("-" * 60)

            print(block[:500])

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

        print(extracted_text[:500])

        print("\nLength:", len(extracted_text))

        print("\n========== EXTRACTED CLAUSES ==========\n")

        print("\nTotal Extracted Clauses:", len(clauses))

        for clause, content in clauses.items():

            print(clause)

            print(content)

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
                unique_filename,
                extracted_text
            )
        )

        uploaded_files.append(unique_filename)

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