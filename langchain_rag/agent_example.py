from dotenv import load_dotenv
import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from calculator_tool import calculator

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

agent = create_agent(
    model=model,
    tools=[calculator],
    system_prompt="You are a helpful assistant."
)

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is 567 * 89?"
            }
        ]
    }
)


messages = response["messages"]

final_answer = messages[-1]

print(final_answer.content)