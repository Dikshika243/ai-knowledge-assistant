import asyncio
import os
from pathlib import Path
from urllib import response

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_google_genai import ChatGoogleGenerativeAI
from sympy import content

load_dotenv()


async def main():
    server_path = Path(__file__).with_name("calculator_server.py")

    async with MCPAdapter(server_path) as adapter:
        tools = await adapter.list_tools()

        print("Available MCP tools:")
        for tool in tools:
            print("-", tool.name)

        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
        )

        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt="You are a helpful assistant.",
        )

        response = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Add 12 and 8, then multiply the result by 3.",
                    }
                ]
            }
        )

        print("\nFinal answer:")

    final_message = response["messages"][-1]
    content = final_message.content

    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block["text"])
    else:
        print(content)

if __name__ == "__main__":
    asyncio.run(main())
