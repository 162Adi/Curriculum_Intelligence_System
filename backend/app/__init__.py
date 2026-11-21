"""
Curriculum Intelligence System (CIS) Backend Application Package.
"""
import sys
from pathlib import Path

# Automatically ensure project root (where openclaw and mcp_server reside) and backend are on sys.path
_current_file = Path(__file__).resolve()
_backend_dir = str(_current_file.parent.parent)         # D:\OG_Agentic\backend
_project_root = str(_current_file.parent.parent.parent)  # D:\OG_Agentic

for _p in [_project_root, _backend_dir]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Install cython fallback finder early
import app.core.cython_compat  # noqa: F401
