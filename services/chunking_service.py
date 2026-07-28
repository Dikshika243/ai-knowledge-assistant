from config import CHUNK_SIZE
from config import CHUNK_OVERLAP

class ChunkingService:

    @staticmethod
    def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(text[start:end])

            start += chunk_size - overlap

        return chunks