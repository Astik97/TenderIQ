from backend.utils.helpers import allowed_file
from backend.utils.helpers import generate_unique_filename

print(allowed_file("sample.pdf"))

print(allowed_file("virus.exe"))

print(generate_unique_filename("Tender.pdf"))