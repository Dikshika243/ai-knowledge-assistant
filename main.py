from services.ai_service import AIService
from services.chunking_service import ChunkingService
from services.document_indexing_service import DocumentIndexingService
from services.embedding_service import EmbeddingService
from services.intent_service import IntentService
from services.pdf_service import PDFService
from services.prompt_service import PromptService
from services.vector_db_service import VectorDBService
from services.query_service import QueryService


def main():

    # Create services
    pdf_service = PDFService()
    chunking_service = ChunkingService()
    embedding_service = EmbeddingService()
    vector_db_service = VectorDBService()
    ai_service = AIService()
    prompt_service = PromptService()

    document_indexing_service = DocumentIndexingService(
        pdf_service=pdf_service,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
        vector_db_service=vector_db_service
    )

    query_service = QueryService(
    embedding_service=embedding_service,
    vector_db_service=vector_db_service,
    prompt_service=prompt_service,
    ai_service=ai_service,
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
       

        try:
            answer = query_service.ask(question)
            print(f"\nAI: {answer}\n")

        except Exception as ex:
            print(f"\nError: {ex}\n")
            print("Please try again later.\n")


if __name__ == "__main__":
    main()