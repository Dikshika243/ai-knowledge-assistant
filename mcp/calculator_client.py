import asyncio
from unittest import result

from mcp import Client, StdioServerParameters


server = StdioServerParameters(
    command=r"D:\AI-Engineering\.venv\Scripts\python.exe",
    args=["mcp/calculator_server.py"],
)


async def main():
    async with Client(server) as client:
        result = await client.list_tools()
        for tool in result.tools:
            print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())