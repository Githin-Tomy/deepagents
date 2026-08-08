from deepagents import SubAgent
from .config import FAST_MODEL, REASONING_MODEL

def get_subagents(mcp_tools: list) -> list[SubAgent]:
    quick_chat = SubAgent(
        name="quick_chat",
        description="Handles casual chat, greetings, simple questions, and basic category lookups.",
        system_prompt=(
            "You are a friendly personal finance assistant. Keep your answers concise and conversational. "
            "For complex analytics or large queries, you won't have the tools, so politely let the Orchestrator route them elsewhere."
        ),
        model=f"google_genai:{FAST_MODEL}",
        tools=[]
    )

    expense_analyst = SubAgent(
        name="expense_analyst",
        description=(
            "Handles robust expense analysis, calculating budgets, identifying spending trends, and managing "
            "large volumes of SQL data. Use this subagent for any complex finance analytics."
        ),
        system_prompt=(
            "You are an expert Expense Analyst. You have access to a SQL database via MCP tools and a local filesystem workspace. "
            "When a SQL query returns a massive amount of data, you MUST write the JSON/CSV output to the local "
            "workspace (`/workspace/finances/`) using `write_file` to avoid blowing up your context window. "
            "You can then use `grep` or `read_file` to analyze chunks of the data, or evaluate it to answer the user."
        ),
        model=f"google_genai:{REASONING_MODEL}",
        tools=mcp_tools
    )
    
    return [quick_chat, expense_analst]
