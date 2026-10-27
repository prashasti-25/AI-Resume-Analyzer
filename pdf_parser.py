"""
resume_parser/pdf_parser.py
----------------------------
THIS IS THE MAIN FILE MEMBER 1's app.py CALLS.

Public contract (do not change without telling the team):

    resume_data = parse_resume(file)

    file can be either:
        - a file path (string), e.g. "instance/uploads/resume.pdf"
        - a file-like object with .read() (e.g. Flask's FileStorage)

    Returns a dict:
    {
        "raw_text": "...",
        "name": "...",
        "email": "...",
        "phone": "...",
        "skills": [...],
        "education": [...],
        "experience": [...]
    }
"""

import pdfplumber
from PyPDF2 import PdfReader

from resume_parser.information_extractor import extract_all
from resume_parser.skill_extractor import extract_skills


def _extract_text_with_pdfplumber(file):
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts).strip()


def _extract_text_with_pypdf2(file):
    """Fallback used only if pdfplumber fails (e.g. certain malformed PDFs)."""
    if hasattr(file, "seek"):
        file.seek(0)

    reader = PdfReader(file)
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts).strip()


def extract_text_from_pdf(file):
    """
    Extracts raw text from a PDF file. Tries pdfplumber first (better
    layout/whitespace handling), falls back to PyPDF2 if that fails
    or returns empty text (e.g. certain PDF encodings).
    """
    try:
        text = _extract_text_with_pdfplumber(file)
        if text:
            return text
    except Exception:
        pass

    try:
        if hasattr(file, "seek"):
            file.seek(0)
        text = _extract_text_with_pypdf2(file)
        return text
    except Exception as e:
        raise ValueError(f"Could not extract text from PDF: {e}")


def parse_resume(file):
    """
    Main function of the resume_parser module.
    Extracts raw text, then runs contact-info, education, experience,
    and skill extraction on top of it.
    """
    raw_text = extract_text_from_pdf(file)

    if not raw_text:
        raise ValueError(
            "No text could be extracted from this PDF. "
            "It may be a scanned image rather than a text-based PDF."
        )

    info = extract_all(raw_text)
    skills = extract_skills(raw_text)

    return {
        "raw_text": raw_text,
        "name": info["name"],
        "email": info["email"],
        "phone": info["phone"],
        "skills": skills,
        "education": info["education"],
        "experience": info["experience"],
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_parser.py <path_to_resume.pdf>")
    else:
        result = parse_resume(sys.argv[1])
        for key, value in result.items():
            print(f"\n--- {key} ---")
            print(value)
