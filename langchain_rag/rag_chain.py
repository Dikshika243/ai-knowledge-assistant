from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from services.conversation_memory_service import ConversationMemoryService
from langchain_core.messages import HumanMessage, AIMessage

from config import (
    CHROMA_PATH,
    EMBEDDING_MODEL,
)

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)

vector_store = Chroma(
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

prompt = PromptTemplate.from_template("""
You are a helpful document assistant.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer the question using ONLY the context and conversation history.
If the answer is not available, say you don't know.
""")

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def format_docs(documents):
    return "\n\n".join(doc.page_content for doc in documents)

def format_history(messages):
    return "\n".join(
        f"{type(message).__name__}: {message.content}"
        for message in messages
    )

from langchain_core.runnables import RunnableLambda

chain = (
    {
        "context": (
            RunnableLambda(lambda x: x["question"])
            | retriever
            | format_docs
        ),

        "question": RunnableLambda(
            lambda x: x["question"]
        ),

        "history": (
            RunnableLambda(lambda x: x["history"])
            | format_history
        )
    }
    | prompt
    | llm
    | StrOutputParser()
)

memory = ConversationMemoryService()

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break


    memory.add_user_message(question)

    answer = chain.invoke(
        {
            "question": question,
            "history": memory.get_history()
        }
            )

    memory.add_ai_message(
        AIMessage(content=answer)
    )

    print("\nAI:", answer)
    print()

    collection = vector_store._collection

    print("Documents in Chroma:", collection.count())