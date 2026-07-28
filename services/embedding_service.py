from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def generate_embedding(self, text: str):
        return self.model.encode(text)