import logging
import os
import uuid

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session
)

from werkzeug.utils import secure_filename
from backend.utils.db import get_connection
from backend.services.dashboard_service import generate_dashboard_summary

from backend.services.document_service import (
    extract_pdf,
    extract_docx,
    extract_txt
)

from backend.services.text_preprocessing import clean_text
from backend.services.clause_extraction import extract_clauses

# =========================================================
# Logger
# =========================================================

logger = logging.getLogger(__name__)

# =========================================================
# Blueprint
# =========================================================

tender_bp = Blueprint("tender", __name__)

# =========================================================
# Configuration
# =========================================================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf","docx","txt"}

# =========================================================
# Helper Functions
# =========================================================

def allowed_file(filename):
    """
    Validate uploaded file extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS

# =========================================================
# Dashboard
# =========================================================

@tender_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        flash("Please login first.", "error")

        return redirect("/login")

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                tender_name,
                file_name,
                upload_date
            FROM tenders
            WHERE user_id=%s
            ORDER BY upload_date DESC
            """,
            (
                session["user_id"],
            )
        )

        tenders = cursor.fetchall()

        dashboard_summary = generate_dashboard_summary(session["user_id"])

        return render_template(
            "dashboard.html",
            tenders=tenders,
            dashboard_summary=dashboard_summary
        )

    except Exception as e:

        logger.exception("Dashboard Error")

        flash(f"Unable to load dashboard: {e}", "error")

        return redirect("/login")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# View Tender
# =========================================================

@tender_bp.route("/view/<int:tender_id>")
def view_tender(tender_id):

    if "user_id" not in session:

        flash("Please login first.", "error")

        return redirect("/login")

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                tender_name,
                file_name,
                extracted_text,
                upload_date
            FROM tenders
            WHERE id=%s
            AND user_id=%s
            """,
            (
                tender_id,
                session["user_id"]
            )
        )

        tender = cursor.fetchone()

        if tender is None:

            flash("Tender not found.", "error")

            return redirect("/dashboard")

        return render_template("view_tender.html", tender=tender)

    except Exception as e:

        logger.exception("View Tender Error")

        flash(f"Unable to open tender: {e}", "error")

        return redirect("/dashboard")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Delete Tender
# =========================================================

@tender_bp.route("/delete/<int:tender_id>")
def delete_tender(tender_id):

    if "user_id" not in session:

        flash("Please login first.", "error")

        return redirect("/login")

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT file_name
            FROM tenders
            WHERE id=%s
            AND user_id=%s
            """,
            (
                tender_id,
                session["user_id"]
            )
        )

        result = cursor.fetchone()

        if result is None:

            flash("Tender not found.", "error")

            return redirect("/dashboard")

        filepath = os.path.join(UPLOAD_FOLDER,result[0])

        if os.path.exists(filepath):

            try:
                os.remove(filepath)

            except Exception as e:
                logger.warning(f"Unable to delete file: {filepath} ({e})")

        cursor.execute(
            """
            DELETE FROM tenders
            WHERE id=%s
            AND user_id=%s
            """,
            (
                tender_id,
                session["user_id"]
            )
        )

        conn.commit()

        flash("Tender deleted successfully.", "success")

        return redirect("/dashboard")

    except Exception as e:

        if conn:
            conn.rollback()

        logger.exception("Delete Tender Error")

        flash(f"Unable to delete tender: {e}", "error")

        return redirect("/dashboard")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

# =========================================================
# Upload Tender Files
# =========================================================

@tender_bp.route("/upload", methods=["POST"])
def upload():

    # -----------------------------------------------------
    # Authentication
    # -----------------------------------------------------

    if "user_id" not in session:

        flash("Please login first.", "error")

        return redirect("/login")

    # -----------------------------------------------------
    # Create Upload Folder
    # -----------------------------------------------------

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    files = request.files.getlist("tender_files")

    if not files:

        flash("No files selected.", "warning")

        return redirect("/dashboard")

    conn = None
    cursor = None

    uploaded_files = []
    duplicate_files = []
    invalid_files = []
    failed_files = []

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # =================================================
        # Process Every Uploaded File
        # =================================================

        for file in files:

            # --------------------------------------------
            # Empty Filename
            # --------------------------------------------

            if file.filename == "":

                continue

            filename = secure_filename(file.filename)

            logger.info(f"Processing : {filename}")

            # --------------------------------------------
            # File Validation
            # --------------------------------------------

            if not allowed_file(filename):

                invalid_files.append(filename)

                logger.warning(f"Invalid file : {filename}")

                continue

            # --------------------------------------------
            # Duplicate Check
            # --------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM tenders
                WHERE user_id=%s
                AND tender_name=%s
                """,
                (
                    session["user_id"],
                    filename
                )
            )

            if cursor.fetchone():

                duplicate_files.append(filename)

                logger.info(f"Duplicate skipped : {filename}")

                continue

            # --------------------------------------------
            # Generate Unique Filename
            # --------------------------------------------

            extension = filename.rsplit(".", 1)[1].lower()

            unique_filename = (f"{uuid.uuid4()}_{filename}")

            filepath = os.path.join(UPLOAD_FOLDER,unique_filename)

            # --------------------------------------------
            # Save Uploaded File
            # --------------------------------------------

            try:
                file.save(filepath)

            except Exception as e:

                logger.exception(f"Unable to save {filename}")

                failed_files.append(filename)

                continue

            # --------------------------------------------
            # Extract Document Text
            # --------------------------------------------

            try:

                if extension == "pdf":
                    raw_text = extract_pdf(filepath)

                elif extension == "docx":
                    raw_text = extract_docx(filepath)

                elif extension == "txt":
                    raw_text = extract_txt(filepath)

                else:
                    raw_text = ""

            except Exception as e:

                logger.exception(f"Extraction failed : {filename}")

                failed_files.append(filename)

                continue

            # --------------------------------------------
            # Clean Extracted Text
            # --------------------------------------------

            extracted_text = clean_text(raw_text)

            # --------------------------------------------
            # Clause Extraction
            # --------------------------------------------

            clauses = extract_clauses(extracted_text)

            logger.info(f"{filename} : {len(clauses)} clauses extracted")

            # --------------------------------------------
            # Skip Empty Documents
            # --------------------------------------------

            if not extracted_text.strip():

                logger.warning(f"No text extracted : {filename}")

                failed_files.append(filename)

                continue

            # --------------------------------------------
            # Database Insert
            # --------------------------------------------

            query = """
                INSERT INTO tenders
                (
                    user_id,
                    tender_name,
                    file_name,
                    extracted_text
                )
                VALUES
                (%s,%s,%s,%s)
            """

            # --------------------------------------------
            # Insert Into Database
            # --------------------------------------------

            try:

                cursor.execute(
                    query,
                    (
                        session["user_id"],
                        filename,
                        unique_filename,
                        extracted_text
                    )
                )

                uploaded_files.append(filename)

                logger.info(f"Successfully uploaded : {filename}")

            except Exception as e:

                logger.exception(f"Database insert failed : {filename}")

                failed_files.append(filename)

                # Remove saved file if database insert fails

                if os.path.exists(filepath):

                    try:
                        os.remove(filepath)

                    except Exception:
                        pass

                continue

        # =================================================
        # Commit Database
        # =================================================

        conn.commit()

        logger.info("Upload transaction committed.")

        # =================================================
        # Flash Messages
        # =================================================

        if uploaded_files:
            flash(f"{len(uploaded_files)} file(s) uploaded successfully.","success")

        if duplicate_files:
            flash(f"{len(duplicate_files)} duplicate file(s) skipped.","warning")

        if invalid_files:
            flash(f"{len(invalid_files)} invalid file(s) ignored.","warning")

        if failed_files:
            flash(f"{len(failed_files)} file(s) failed during processing.","error")

        if (
            not uploaded_files
            and not duplicate_files
            and not invalid_files
            and not failed_files
        ):

            flash("No files were processed.","warning")

    # =====================================================
    # Global Exception
    # =====================================================

    except Exception as e:

        if conn:
            conn.rollback()

        logger.exception("Upload Route Error")

        flash(f"Upload failed: {str(e)}","error")

    # =====================================================
    # Cleanup
    # =====================================================

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    # =====================================================
    # Upload Summary (Console)
    # =====================================================

    logger.info("=" * 60)
    logger.info("UPLOAD SUMMARY")
    logger.info("=" * 60)

    logger.info(f"Uploaded Files  : {len(uploaded_files)}")
    logger.info(f"Duplicate Files : {len(duplicate_files)}")
    logger.info(f"Invalid Files   : {len(invalid_files)}")
    logger.info(f"Failed Files    : {len(failed_files)}")

    if uploaded_files:
        logger.info("Uploaded:")

        for file in uploaded_files:
            logger.info(f"  ✔ {file}")

    if duplicate_files:
        logger.info("Duplicates:")

        for file in duplicate_files:
            logger.info(f"  ✖ {file}")

    if invalid_files:
        logger.info("Invalid:")

        for file in invalid_files:
            logger.info(f"  ✖ {file}")

    if failed_files:
        logger.info("Failed:")

        for file in failed_files:
            logger.info(f"  ✖ {file}")

    logger.info("=" * 60)

    return redirect("/dashboard")