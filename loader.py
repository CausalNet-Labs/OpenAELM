"""
==============================================================================
loader.py
Advanced Employment & Labor Model (AELM)
File Loader
==============================================================================
"""

from pathlib import Path
from pypdf import PdfReader
from docx import Document

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}


class FileLoader:

    @staticmethod
    def load(path: str) -> str:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        ext = path.suffix.lower()

        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {ext}")

        if ext in (".txt", ".md"):
            return FileLoader._load_text(path)

        if ext == ".pdf":
            return FileLoader._load_pdf(path)

        if ext == ".docx":
            return FileLoader._load_docx(path)

        raise ValueError("Unsupported file type.")

    @staticmethod
    def _load_text(path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="ignore")

    @staticmethod
    def _load_pdf(path: Path) -> str:
        reader = PdfReader(str(path))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n".join(pages)

    @staticmethod
    def _load_docx(path: Path) -> str:
        doc = Document(str(path))
        return "\n".join(
            p.text for p in doc.paragraphs if p.text.strip()
        )


def load_resume(path: str) -> str:
    return FileLoader.load(path)


def load_job(path: str) -> str:
    return FileLoader.load(path)


if __name__ == "__main__":
    while True:
        filename = input("File (or 'exit'): ").strip()

        if filename.lower() == "exit":
            break

        try:
            text = FileLoader.load(filename)
            print("=" * 60)
            print(text[:2000])
            print("=" * 60)
            print(f"Characters: {len(text)}")
        except Exception as e:
            print(f"Error: {e}")
