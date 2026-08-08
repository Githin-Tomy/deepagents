"""Basic smoke tests for the project layout."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_expected_project_files_exist():
    """Ensure the application entry point and workspace are present."""
    assert (PROJECT_ROOT / "src" / "main.py").is_file()
    assert (PROJECT_ROOT / "workspace").is_dir()
