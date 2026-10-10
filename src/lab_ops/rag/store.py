# src/lab_ops/rag/store.py
from pathlib import Path
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from pypdf import PdfReader

DB_PATH = Path("~/.lab-ops/db").expanduser()

# Configure LanceDB to use OpenAI's text-embedding-3-small model automatically
func = get_registry().get("openai").create(name="text-embedding-3-small")


class DocumentChunk(LanceModel):
    id: str
    filename: str
    chunk_id: int
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()


def get_or_create_table():
    """Initializes local LanceDB database and returns the literature table."""
    DB_PATH.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(DB_PATH))

    # Opens or creates table using the DocumentChunk schema
    return db.create_table("literature", schema=DocumentChunk, exist_ok=True)


def ingest_pdf(pdf_path: Path, chunk_size: int = 1000, overlap: int = 200) -> int:
    """Parses a PDF paper, splits text into overlapping chunks, and stores in LanceDB."""
    pdf_path = pdf_path.expanduser()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    full_text = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_text.append(f"[Page {page_num + 1}]\n{text}")

    combined_text = "\n".join(full_text)

    chunks = []
    start = 0
    chunk_idx = 0
    while start < len(combined_text):
        end = start + chunk_size
        chunk_str = combined_text[start:end]
        chunks.append(
            {
                "id": f"{pdf_path.stem}_{chunk_idx}",
                "filename": pdf_path.name,
                "chunk_id": chunk_idx,
                "text": chunk_str,
            }
        )
        start += chunk_size - overlap
        chunk_idx += 1

    table = get_or_create_table()
    # LanceDB automatically computes and stores embeddings for the 'text' field
    table.add(chunks)
    return len(chunks)
