import os
from werkzeug.utils import secure_filename

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

def generate_unique_filename(filename):

    import uuid

    filename = secure_filename(filename)

    return f"{uuid.uuid4()}_{filename}"

def get_file_extension(filename):

    return filename.rsplit(".", 1)[1].upper()