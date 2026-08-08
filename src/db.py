import contextlib
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools

# The SSE URL for the local SQL MCP server
MCP_SERVER_URL = "http://localhost:8000/sse"

@contextlib.asynccontextmanager
async def get_mcp_tools():
    """
    Connects to the local SQL MCP server via SSE and yields the loaded LangChain tools.
    Must be used in an async with block to keep the session alive.
    """
    async with sse_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            yield tools
