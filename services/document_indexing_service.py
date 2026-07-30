from pathlib import Path
from config import DOCUMENT_FOLDER
from services.pdf_service import PDFService
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.vector_db_service import VectorDBService
from services.ai_service import AIService
from services.prompt_service import PromptService

class DocumentIndexingService:

    def __init__(
        self,
        pdf_service: PDFService,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_db_service: VectorDBService,
        ai_service: AIService,
        prompt_service: PromptService
    ):
        self.pdf_service = pdf_service
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service
        self.ai_service = ai_service
        self.prompt_service = prompt_service

    def index_documents(self):
        """
        Reads all PDFs from the documents folder,
        generates embeddings, and stores them in ChromaDB.
        """

        # Start with a clean collection
        self.vector_db_service.reset_collection()

        pdf_files = list(Path(DOCUMENT_FOLDER).glob("*.pdf"))

        if not pdf_files:
            print(f"No PDF files found in '{DOCUMENT_FOLDER}'.")
            return

        total_documents = 0
        total_chunks = 0

        for pdf_path in pdf_files:

            print(f"\nIndexing: {pdf_path.name}")

            # Extract text
            text = self.pdf_service.extract_text(str(pdf_path))

            if not text.strip():
                print(f"Skipping {pdf_path.name} (no text found)")
                continue

            # Create chunks
            chunks = self.chunking_service.chunk_text(text)

            print(f"Created {len(chunks)} chunks")

            # Store each chunk
            for index, chunk in enumerate(chunks):

                embedding = self.embedding_service.generate_embedding(chunk)

                self.vector_db_service.add_document(
                    document_id=f"{pdf_path.stem}_{index}",
                    chunk=chunk,
                    embedding=embedding,
                    document_name=pdf_path.name,
                    chunk_number=index
                )

            total_documents += 1
            total_chunks += len(chunks)

        print("\nIndexing completed successfully!")
        print(f"Documents indexed : {total_documents}")
        print(f"Total chunks      : {total_chunks}")