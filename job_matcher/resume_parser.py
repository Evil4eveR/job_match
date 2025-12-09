from pathlib import Path
from typing import Optional

import PyPDF2

def load_resume_text(path: str) -> str:
    """
    Reads your resume from PDF or TXT and returns it as plain text.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Resume file not found: {file_path.resolve()}")

    if file_path.suffix.lower() == ".pdf":
        return _load_pdf(file_path)
    else:
        # for .txt or other text formats
        return file_path.read_text(encoding="utf-8", errors="ignore")

def _load_pdf(file_path: Path) -> str:
    text_parts = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text: Optional[str] = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)
