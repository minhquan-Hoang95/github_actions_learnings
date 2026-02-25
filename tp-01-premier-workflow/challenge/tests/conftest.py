"""Pytest test configuration."""

from pathlib import Path
import sys

# Ensure the project root is importable so `src` package resolves in tests.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
