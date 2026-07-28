from services.ai_service import AIService
from services.chunking_service import ChunkingService
from services.document_indexing_service import DocumentIndexingService
from services.embedding_service import EmbeddingService
from services.intent_service import IntentService
from services.pdf_service import PDFService
from prompts.prompt_builder import PromptBuilder
from services.vector_db_service import VectorDBService


def main():

    # Create services
    pdf_service = PDFService()
    chunking_service = ChunkingService()
    embedding_service = EmbeddingService()
    vector_db_service = VectorDBService()
    ai_service = AIService()

    document_indexing_service = DocumentIndexingService(
        pdf_service=pdf_service,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
        vector_db_service=vector_db_service
    )

    # Index all documents
    document_indexing_service.index_documents()

    print("\nYou can now ask multiple questions.")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        # Handle greetings / thanks etc.
        intent_response = IntentService.get_response(question)

        if intent_response:
            print(f"\nAI: {intent_response}\n")
            continue

        # Generate embedding for the question
        query_embedding = embedding_service.generate_embedding(question)

        # Search vector database
        results = vector_db_service.search(query_embedding)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        # Debug (remove later if desired)
        print("\nRetrieved Chunks:\n")

        for metadata, document in zip(metadatas, documents):
            print(f"Document : {metadata['document']}")
            print(f"Chunk    : {metadata['chunk']}")
            print("-" * 40)
            print(document[:200])
            print()

        # Build prompt
        context = "\n\n".join(documents)

        prompt = PromptBuilder.build_prompt(
            question=question,
            context_documents=documents
        )

        try:
            answer = ai_service.generate_answer(prompt)
            print(f"\nAI: {answer}\n")

        except Exception as ex:
            print(f"\nError: {ex}\n")
            print("Please try again later.\n")


if __name__ == "__main__":
    main()