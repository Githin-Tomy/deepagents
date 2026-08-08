# Unified Personal Finance OS (DeepAgents & MCP)

This directory contains a complete **Unified Personal Finance OS** powered by the **DeepAgents** (`deepagents`) framework. It acts as an advanced orchestrator that delegates tasks to specialized subagents.

## What You Will Learn Here

- **DeepAgents Orchestration:** How to use `deepagents.create_deep_agent` to rapidly build a scalable AI OS that delegates user requests to specialized `SubAgent` profiles (e.g., `quick_chat` vs `expense_analyst`).
- **MCP SSE Integration:** How to connect a DeepAgents graph to a local Model Context Protocol (MCP) server over Server-Sent Events (SSE) and dynamically load `SQLDatabaseToolkit` tools.
- **Filesystem & Security Policies:** Implementing `FilesystemBackend` and `FilesystemPermission` rules to securely constrain the AI's file access to specific `/workspace/` directories, completely sandboxing it from credential files.
- **Human-in-the-Loop (HITL):** Using `interrupt_on` configurations with a Checkpointer (`MemorySaver`) to pause agent execution before destructive or critical actions (like writing files) so a human can approve or reject the action.

## Prerequisites

Ensure you have installed the project dependencies, particularly `deepagents`, `langchain-mcp-adapters`, and `langgraph`.

## Setup Instructions

1. **Environment Variables**:
   Copy the example environment file and add your `GOOGLE_API_KEY`. You can also configure the default `GOOGLE_MODEL`.
   ```bash
   cp .env.example .env
   ```

2. **Ensure Database Exists**:
   This OS analyzes the database located in `../langgraph-multiagents-mcp/data/app.db`. If you haven't already, navigate to that folder and run the `scripts/setup_db.py` script.

3. **Start the MCP Server**:
   In a separate terminal, start the MCP server located in the `sql-mcp-server` directory.
   ```bash
   cd ../sql-mcp-server
   python server.py --db-path "../langgraph-multiagents-mcp/data/app.db" --transport sse --port 8000
   ```

4. **Run the OS**:
   Launch the interactive asynchronous CLI orchestrator.
   ```bash
   python src/main.py
   ```

## Try the Human-In-The-Loop Feature

To trigger the Human-In-The-Loop functionality, ask the AI to perform a filesystem write action. For example:
> *"Analyze my expenses for April 2026 and save a detailed summary report to a markdown file."*

The graph will pause execution and ask for your approval in the CLI (`approve` or provide feedback to `reject`) before proceeding!
