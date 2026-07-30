from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFService:

    def load(self, file_path: str) -> list[Document]:
        loader = PyPDFLoader(file_path)
        return loader.load()