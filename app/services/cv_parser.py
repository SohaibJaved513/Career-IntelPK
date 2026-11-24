from pathlib import Path


def read_txt(path):
    return Path(path).read_text(encoding="utf-8", errors="ignore")


def read_pdf(path):
    import pdfplumber

    text = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")

    return "\n".join(text)


def read_docx(path):
    import docx

    document = docx.Document(path)
    return "\n".join([p.text for p in document.paragraphs])


def extract_text(path):
    ext = Path(path).suffix.lower()

    if ext == ".txt":
        return read_txt(path)

    if ext == ".pdf":
        return read_pdf(path)

    if ext == ".docx":
        return read_docx(path)

    return ""
