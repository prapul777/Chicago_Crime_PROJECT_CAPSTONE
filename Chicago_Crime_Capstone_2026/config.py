"""
Chicago Crime Capstone - Flask Configuration

Centralizes project paths, Flask settings
and required resource validation.
"""

from pathlib import Path


# 1. PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "data" / "chicago_crime.db"

CHARTS_DIR = BASE_DIR / "static" / "charts"


# 2. FLASK CONFIGURATION

class Config:
    # Secret key for local development and CRUD flash messages.
    SECRET_KEY = "chicago-crime-capstone-local-dev"


# 3. RESOURCE VALIDATION

def validate_project_files():
    """Verify that the SQLite database and chart folder exist."""

    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(
            f"SQLite database not found: {DATABASE_PATH}"
        )

    if not CHARTS_DIR.is_dir():
        raise FileNotFoundError(
            f"Chart folder not found: {CHARTS_DIR}"
        )

    print("Database: Available")
    print("Charts folder: Available")
    print("Flask configuration: Ready")


# Run validation when this file is executed directly.
if __name__ == "__main__":
    validate_project_files()