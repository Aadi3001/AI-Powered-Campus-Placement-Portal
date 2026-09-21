import pymupdf
import re


def extract_text_from_pdf(file_path):
    """
    Opens a PDF file from disk and extracts all its text.
    """
    doc = pymupdf.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text


def extract_skills_from_text(text, skill_names):
    """
    Given resume text and a list of known skill names,
    return the list of skills actually mentioned in the text.
    Uses word-boundary matching to avoid partial-word false positives
    (e.g. "Java" incorrectly matching inside "JavaScript").
    """
    found_skills = []
    text_lower = text.lower()

    for skill in skill_names:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills