from services.ai_service import AIService
from services.embedding_service import EmbeddingService
from services.prompt_service import PromptService
from services.vector_db_service import VectorDBService
from models.search_result import SearchResult


class QueryService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_db_service: VectorDBService,
        prompt_service: PromptService,
        ai_service: AIService,
    ):
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service
        self.prompt_service = prompt_service
        self.ai_service = ai_service

    def ask(self, question: str) -> str:
        search_result = self._retrieve_documents(question)

        self._print_debug_info(search_result)

        prompt = self._build_prompt(question, search_result.documents)

        return self._generate_answer(prompt)

    def _retrieve_documents(self, question: str):
        
        query_embedding = self.embedding_service.generate_embedding(question)

        results = self.vector_db_service.search(query_embedding)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        return SearchResult(
            documents = documents, 
            metadatas = metadatas
        )

    def _print_debug_info(self, result: SearchResult):
        print("\nRetrieved Chunks:\n")

        for metadata, document in zip(result.metadatas, result.documents):

            print(f"Document : {metadata['document']}")
            print(f"Chunk    : {metadata['chunk']}")
            print("-" * 40)
            print(document[:200])
            print()

    def _build_prompt(self, question: str, documents):

        return self.prompt_service.build_prompt(
            question=question,
            context_documents=documents
        )

    def _generate_answer(self, prompt: str):
        return self.ai_service.generate_answer(prompt)