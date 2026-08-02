from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    CHROMA_PATH,
    DOCUMENT_FOLDER,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL
)


def load_documents():

    documents = []

    pdf_files = Path(DOCUMENT_FOLDER).glob("*.pdf")

    for pdf_file in pdf_files:

        print(f"Loading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))

        documents.extend(loader.load())

    return documents


if __name__ == "__main__":

    documents = load_documents()

    print(f"\nLoaded {len(documents)} pages.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    print(f"\nCreated {len(chunks)} chunks.\n")

    first_chunk = chunks[0]

    print("===== First Chunk =====\n")
    print(first_chunk.page_content)

    print("\n===== Metadata =====")
    print(first_chunk.metadata)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=str(CHROMA_PATH)
)

print("Indexing completed!")
print(f"Stored {len(chunks)} chunks.")