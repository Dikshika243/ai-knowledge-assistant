import asyncio

from mcp.server import MCPServer


mcp = MCPServer("Calculator Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


async def main():
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())