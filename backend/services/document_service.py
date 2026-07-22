import pdfplumber
import docx2txt

def extract_pdf(path):

    print("=" * 80)
    print("INSIDE extract_pdf()")
    print(path)
    print("=" * 80)

    text = ""
    
    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            print(f"Processing page {page.page_number}")

            page_text = page.extract_text(
                x_tolerance=2,
                y_tolerance=3
            )
            
            print(repr(page_text[:300]))

            if page_text:
                
                text += page_text + "\n"
                
    return text

def extract_docx(path):

    return docx2txt.process(path)

def extract_txt(path):

    with open(path,"r",encoding="utf-8") as file:

        return file.read()