import pymupdf  # PyMuPDF
import re

def extract_pdf(file_bytes: bytes) -> str:
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        pages = [page.get_text() for page in doc]
    
    text = " ".join(pages)
    # Combine regex passes into one pattern
    text = re.sub(r'(\w+)-\n\s*(\w+)', r'\1\2', text)
    return re.sub(r'\s+', ' ', text).strip()

    
def extract_text(file_bytes: bytes) -> str:
    # Use errors="ignore" or "replace" to prevent decoding crashes
    return file_bytes.decode("utf-8", errors="replace").strip()