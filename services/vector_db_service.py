import chromadb
from config import CHROMA_PATH
from config import COLLECTION_NAME
from config import TOP_K


class VectorDBService:

    def __init__(self):

        # Creates a local persistent database
        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        # Creates the collection if it doesn't exist.
        # Otherwise, returns the existing collection.
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def add_document(
            self,
            document_id: str,
            chunk: str,
            embedding,
            document_name: str,
            chunk_number: int):

        self.collection.add(
            ids=[document_id],
            documents=[chunk],
            embeddings=[embedding.tolist()],
            metadatas=[
                {
                    "document": document_name,
                    "chunk": chunk_number
                }
            ]
        )

    def get_all_documents(self):

        return self.collection.get(
            include=["documents", "embeddings"]
        )
    def search(self, query_embedding):

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=TOP_K
        )

        return results
    def reset_collection(self):
        try:
            self.client.delete_collection("knowledge_base")
        except Exception:
            # Ignore if the collection doesn't exist
            pass

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )