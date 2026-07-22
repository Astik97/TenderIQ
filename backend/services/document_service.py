import pdfplumber
import docx2txt

def extract_pdf(path):

    text = ""
    
    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text(x_tolerance=2,y_tolerance=3)

            if page_text:

                text += page_text + "\n"
                
    return text

def extract_docx(path):

    return docx2txt.process(path)

def extract_txt(path):

    with open(path,"r",encoding="utf-8") as file:

        return file.read()