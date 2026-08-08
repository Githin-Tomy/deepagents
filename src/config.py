import os
from deepagents.middleware.filesystem import FilesystemPermission
from dotenv import load_dotenv

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")
FINANCES_DIR = os.path.join(WORKSPACE_DIR, "finances")
REPORTS_DIR = os.path.join(WORKSPACE_DIR, "reports")

# Load existing environment for API keys (or local .env if it exists)
load_dotenv(os.path.join(BASE_DIR, "..", "langgraph-multiagents-mcp", ".env"))

# Database Configuration (Defaults to the local app.db from previous setup)
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "langgraph-multiagents-mcp", "data", "app.db"))
DB_URI = os.getenv("DATABASE_URI", f"sqlite:///{DB_PATH}")

# Model Configuration
FAST_MODEL = os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite")
REASONING_MODEL = os.getenv("GOOGLE_MODEL", "gemini-3.1-flash-lite")

# Permissions
PERMISSIONS = [
    FilesystemPermission(operations=["read", "write"], paths=["/workspace/finances/**", "/workspace/reports/**"], mode="allow"),
    FilesystemPermission(operations=["read", "write"], paths=["/**/.env", "/**/credentials.json"], mode="deny"),
]
