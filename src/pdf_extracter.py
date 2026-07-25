import pymupdf  # PyMuPDF
import re

def extract_pdf(file_bytes: bytes) -> str:
    doc = pymupdf.open(stream=file_bytes, filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    # Clean the text
    text = re.sub(r'(\w+)-\n\s*(\w+)', r'\1\2', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def extract_text(file_bytes:bytes):
    return file_bytes.decode("utf-8").strip()