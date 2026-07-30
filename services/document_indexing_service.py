from pathlib import Path

from config import DOCUMENT_FOLDER
from services.pdf_service import PDFService
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.vector_db_service import VectorDBService


class DocumentIndexingService:

    def __init__(
        self,
        pdf_service: PDFService,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_db_service: VectorDBService,
    ):
        self.pdf_service = pdf_service
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service

    def index_documents(self):
        """
        Reads all PDFs from the documents folder,
        splits them into chunks, generates embeddings,
        and stores them in ChromaDB.
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

            # Load PDF as LangChain Documents
            documents = self.pdf_service.load(str(pdf_path))

            if not documents:
                print(f"Skipping {pdf_path.name} (no text found)")
                continue

            # Split into smaller Document chunks
            chunks = self.chunking_service.chunk_documents(documents)

            print(f"Created {len(chunks)} chunks")

            # Generate embeddings and store them
            for index, chunk in enumerate(chunks):

                embedding = self.embedding_service.generate_embedding(
                    chunk.page_content
                )

                self.vector_db_service.add_document(
                    document_id=f"{pdf_path.stem}_{index}",
                    chunk=chunk.page_content,
                    embedding=embedding,
                    document_name=chunk.metadata.get("source", pdf_path.name),
                    chunk_number=index,
                )

            total_documents += 1
            total_chunks += len(chunks)

        print("\nIndexing completed successfully!")
        print(f"Documents indexed : {total_documents}")
        print(f"Total chunks      : {total_chunks}")