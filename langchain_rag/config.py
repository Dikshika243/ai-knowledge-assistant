from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DOCUMENT_FOLDER = BASE_DIR / "documents"

CHROMA_PATH = BASE_DIR / "langchain_chroma"

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "all-MiniLM-L6-v2"