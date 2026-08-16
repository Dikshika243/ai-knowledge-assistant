import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from calculator_tool import calculator
from langchain_core.messages import ToolMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

llm_with_tools = llm.bind_tools(
    [calculator]
)

response = llm_with_tools.invoke(
    "What is 567 * 89?"
)
tool_call = response.tool_calls[0]

result = calculator.invoke(
    tool_call["args"]
)

tool_message = ToolMessage(
    content=str(result),
    tool_call_id=tool_call["id"]
)

final_response = llm_with_tools.invoke(

    [
        "What is 567 * 89?",
        response,
        tool_message
    ]

)
print(final_response.content)