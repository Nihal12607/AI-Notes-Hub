import pymupdf  
import re

def extract_pdf(file_bytes: bytes) -> str:
    text_parts = []
    
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text()
            
            # Apply regex per page to prevent memory spikes on huge documents
            page_text = re.sub(r'(\w+)-\n\s*(\w+)', r'\1\2', page_text)
            page_text = re.sub(r'\s+', ' ', page_text).strip()
            
            if page_text:
                text_parts.append(page_text)
    
    return " ".join(text_parts)

def extract_text(file_bytes: bytes) -> str:
    # Use errors="ignore" or "replace" to prevent decoding crashes
    return file_bytes.decode("utf-8", errors="replace").strip()