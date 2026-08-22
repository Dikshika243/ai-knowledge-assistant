from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
import os

class Skill(BaseModel):

    name: str

class Resume(BaseModel):

    candidate: str

    skills: list[Skill]

class Address(BaseModel):

    city: str

    country: str

class Person(BaseModel):
    name: str

    age: int | None = None

    address: Address

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

structured_llm = llm.with_structured_output(Person)

result = structured_llm.invoke(
      """
    My name is Dikshika.

    I am 30 years old.

    I live in Surat, India.
    """
)

print(result)

print(result.address.city)