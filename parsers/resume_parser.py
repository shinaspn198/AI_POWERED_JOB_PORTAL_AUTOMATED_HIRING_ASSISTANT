import pdfplumber
from docx import Document

from parsers.text_cleaner import TextCleaner
from parsers.section_detector import SectionDetector
from parsers.candidate_extractor import CandidateExtractor


import os

def extract_text(file_path_or_text: str) -> str:
    # If the input is raw resume text rather than an existing file path
    if "\n" in file_path_or_text or not os.path.exists(file_path_or_text):
        if not file_path_or_text.lower().endswith((".pdf", ".docx", ".doc", ".txt")):
            return file_path_or_text

    file_path = file_path_or_text
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found at: {file_path}")

    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif file_path.lower().endswith(".docx"):
        document = Document(file_path)
        return "\n".join([paragraph.text for paragraph in document.paragraphs])

    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        # Fallback to reading as text if possible
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            raise ValueError(f"Unsupported File format: {file_path}")


def parse_resume(file_path):

    raw_text = extract_text(file_path)

    cleaned_text = TextCleaner.clean(raw_text)

    detector = SectionDetector()

    sections = detector.detect_sections(cleaned_text)

    candidate = CandidateExtractor.extract(sections)

    return candidate