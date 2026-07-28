import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# Gemini
# ==========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# ==========================
# Embeddings
# ==========================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ==========================
# Chunking
# ==========================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# ==========================
# Vector Database
# ==========================

TOP_K = 3
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "knowledge_base"

# ==========================
# Documents
# ==========================

DOCUMENT_FOLDER = "./documents"

# ==========================
# Logging
# ==========================

LOG_LEVEL = "INFO"