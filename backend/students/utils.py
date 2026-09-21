import pymupdf


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