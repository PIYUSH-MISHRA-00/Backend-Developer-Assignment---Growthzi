import io
from pdfminer.high_level import extract_text
from docx import Document

def extract_text_from_pdf(file_stream: io.BytesIO) -> str:
    # pdfminer expects a file path or file-like object
    return extract_text(file_stream)

def extract_text_from_docx(file_stream: io.BytesIO) -> str:
    document = Document(file_stream)
    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)
    return '\\n'.join(full_text)
