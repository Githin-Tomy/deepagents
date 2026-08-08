import os
import sys
import asyncio

# Add parent directory to path so imports work correctly when running from CLI
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from src.config import BASE_DIR, PERMISSIONS, REASONING_MODEL
from src.subagents import get_subagents
from src.db import get_mcp_tools

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

async def run_cli():
    print("\n" + "="*50)
    print("Welcome to the Unified Personal Finance OS (MCP Powered)!")
    print("="*50)
    print("Connecting to local SQL MCP Server...")
    
    # Initialize the FilesystemBackend pointing to the finance_os root
    fs_backend = FilesystemBackend(root_dir=BASE_DIR)
    checkpointer = MemorySaver()
    
    # Connect to MCP server and get tools
    async with get_mcp_tools() as mcp_tools:
        print("Successfully connected to MCP Server!")
        print("Type 'exit' to quit.\n")
        
        subagents = get_subagents(mcp_tools)
        
        # Master Orchestrator Agent
        agent = create_deep_agent(
            name="Unified-Finance-OS",
            model=f"google_genai:{REASONING_MODEL}",
            system_prompt=(
                "You are the master Orchestrator for the Unified Personal Finance OS. "
                "You have access to two powerful subagents: 'quick_chat' and 'expense_analyst'. "
                "Route casual questions, general knowledge, or simple finance definitions to 'quick_chat'. "
                "Delegate all database lookups, financial analytics, budgets, and reporting to 'expense_analyst'. "
                "Do not try to answer complex finance questions yourself or guess database structure; always delegate!"
            ),
            subagents=subagents,
            backend=fs_backend,
            permissions=PERMISSIONS,
            interrupt_on={"write_file": True},
            checkpointer=checkpointer,
            debug=True
        )
        
        config = {"configurable": {"thread_id": "cli-session-1"}}
        loop = asyncio.get_running_loop()
        
        while True:
            try:
                state = agent.get_state(config)
                
                # If there are pending tasks in the graph (i.e. it's interrupted)
                if state.next:
                    approval = await loop.run_in_executor(None, input, "\n[SYSTEM] Agent wants to execute a tool. Type 'approve' or provide feedback: ")
                    
                    if approval.lower() == 'approve':
                        stream = agent.astream(Command(resume={"decisions": [{"type": "approve"}]}), config=config, stream_mode="values")
                    elif approval.lower() in ["exit", "quit"]:
                        break
                    else:
                        # Feed the human response back into the state as a message
                        stream = agent.astream(Command(resume={"decisions": [{"type": "reject", "message": approval}]}), config=config, stream_mode="values")
                else:
                    user_input = await loop.run_in_executor(None, input, "\nYou: ")
                    if user_input.lower() in ["exit", "quit"]:
                        break
                        
                    stream = agent.astream({"messages": [("user", user_input)]}, config=config, stream_mode="values")
                    
                # Execute agent asynchronously
                async for event in stream:
                    messages = event.get("messages", [])
                    if messages:
                        last_message = messages[-1]
                        if last_message.type == "ai" and last_message.content:
                            print(f"\n[AI]: {last_message.content}")
                            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"\nError: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_cli())
    except KeyboardInterrupt:
        pass
