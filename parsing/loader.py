"""File loading for resumes and job descriptions.

TXT/MD work with the standard library alone. PDF and DOCX support is
optional — the program stays usable without those packages installed.
"""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}


def load_file(path_str: str) -> str:
    path = Path(path_str).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if ext in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="ignore")
    if ext == ".pdf":
        return _load_pdf(path)
    return _load_docx(path)


def _load_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "PDF support requires the optional 'pypdf' package "
            "(pip install pypdf). Alternatively, save the file as .txt."
        ) from exc

    reader = PdfReader(str(path))
    pages = [p.extract_text() for p in reader.pages if p.extract_text()]
    return "\n".join(pages)


def _load_docx(path: Path) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError(
            "DOCX support requires the optional 'python-docx' package "
            "(pip install python-docx). Alternatively, save the file as .txt."
        ) from exc

    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
