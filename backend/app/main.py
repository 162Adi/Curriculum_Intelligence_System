"""
Curriculum Intelligence System (CIS) — Main FastAPI Backend Application.
Provides RESTful APIs, LangGraph orchestration, WebSocket real-time streaming,
Argon2/JWT authentication, RBAC, and multi-agent coordination.
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

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import app.core.cython_compat  # noqa: F401
from app.core.config import settings
from app.database.session import init_db
from app.core.ws_manager import ws_manager

# API Routers
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.curriculum import router as curriculum_router
from app.api.analysis import router as analysis_router
from app.api.gaps import router as gaps_router
from app.api.recommendations import router as recommendations_router
from app.api.approvals import router as approvals_router
from app.api.reports import router as reports_router
from app.api.integrations import router as integrations_router
from app.api.memory import router as memory_router
from app.api.studio import router as studio_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager: initializes database on startup."""
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Bridging Academic Learning and Industry Requirements Through Agentic Intelligence.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Register API Routers under /api
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(curriculum_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(gaps_router, prefix="/api")
app.include_router(recommendations_router, prefix="/api")
app.include_router(approvals_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(integrations_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(studio_router, prefix="/api")


@app.get("/")
def root():
    """System health and metadata index."""
    return {
        "system": settings.APP_NAME,
        "tagline": "Bridging Academic Learning and Industry Requirements Through Agentic Intelligence.",
        "version": settings.APP_VERSION,
        "status": "OPERATIONAL",
        "documentation": "/docs",
        "mcp_server": settings.MCP_SERVER_URL,
        "openclaw_gateway": settings.OPENCLAW_GATEWAY_URL
    }


@app.websocket("/ws/executions/{execution_id}")
async def websocket_execution_stream(websocket: WebSocket, execution_id: str):
    """Real-time WebSocket endpoint streaming agent state changes to React Flow Agent Control Room."""
    await ws_manager.connect(websocket, execution_id)
    try:
        while True:
            # Keep socket open and receive any client ping/ack messages
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, execution_id)
    except Exception:
        ws_manager.disconnect(websocket, execution_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
