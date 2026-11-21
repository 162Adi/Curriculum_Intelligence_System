"""
Integrations API: Health diagnostics, MCP Tool Registry & Invocation, and OpenClaw Runtime.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from app.core.config import settings
from app.integrations.health import IntegrationHealthService
from openclaw.adapter.runtime_adapter import OpenClawRuntimeAdapter
from app.auth.rbac import get_current_user
from app.models.users import User

router = APIRouter(prefix="/integrations", tags=["Integrations & Protocols"])


@router.get("/health")
async def get_integration_health(current_user: User = Depends(get_current_user)):
    """Check health and live connectivity for all external systems, MCP, and OpenClaw."""
    return await IntegrationHealthService.check_all()


@router.get("/mcp/tools")
async def get_mcp_tools(current_user: User = Depends(get_current_user)):
    """Query official MCP server for available tool schemas, capabilities, and permissions."""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get(f"{settings.MCP_SERVER_URL}/mcp/tools")
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass

    # Fallback to local server schema if mcp server process is currently starting
    from mcp_server.server import MCP_TOOLS, MCP_RESOURCES, MCP_PROMPTS
    return {"tools": MCP_TOOLS, "resources": MCP_RESOURCES, "prompts": MCP_PROMPTS, "source": "in-process"}


@router.post("/mcp/invoke")
async def invoke_mcp_tool(payload: dict, current_user: User = Depends(get_current_user)):
    """Execute an MCP tool via the MCP protocol."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(f"{settings.MCP_SERVER_URL}/mcp/invoke", json=payload)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass

    # Direct fallback runner
    t_name = payload.get("tool_name")
    args = payload.get("arguments", {})
    from mcp_server.server import invoke_mcp_tool as local_invoker, ToolInvocationRequest
    req = ToolInvocationRequest(tool_name=t_name, arguments=args)
    return local_invoker(req)


@router.get("/openclaw/status")
async def get_openclaw_status(current_user: User = Depends(get_current_user)):
    """Check live connection status to the OpenClaw Gateway service."""
    return await OpenClawRuntimeAdapter.check_connection()


@router.post("/openclaw/dispatch")
async def dispatch_openclaw_task(payload: dict, current_user: User = Depends(get_current_user)):
    """Dispatch an autonomous agent task to the OpenClaw Gateway runtime."""
    agent_type = payload.get("agent_type", "deep-research-worker")
    task_prompt = payload.get("task_prompt", "Analyze curriculum gap")
    session_id = payload.get("session_id")

    return await OpenClawRuntimeAdapter.dispatch_task(agent_type, task_prompt, session_id)
