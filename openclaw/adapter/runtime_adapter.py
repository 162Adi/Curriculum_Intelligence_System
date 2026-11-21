"""
CIS Dedicated OpenClaw Adapter.
Handles Gateway connection, token authentication, session mapping,
and delegated agent dispatch to the OpenClaw runtime service.
"""

from typing import Dict, Any, Optional
import httpx
from app.core.config import settings


class OpenClawRuntimeAdapter:
    """Official CIS Adapter communicating with the separately running OpenClaw Gateway service."""

    @classmethod
    def create_worker_payload(cls, session_id: str, task_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format an OpenClaw worker task payload."""
        return {
            "session_id": session_id,
            "task_name": task_name,
            "gateway_port": 18789,
            "state": "INITIALIZED",
            "params": params or {}
        }

    @classmethod
    def get_gateway_url(cls) -> str:
        return settings.OPENCLAW_GATEWAY_URL

    @classmethod
    async def check_connection(cls) -> Dict[str, Any]:
        """Test actual connection to the running OpenClaw Gateway service."""
        url = cls.get_gateway_url()
        headers = {}
        if settings.OPENCLAW_GATEWAY_TOKEN:
            headers["Authorization"] = f"Bearer {settings.OPENCLAW_GATEWAY_TOKEN}"

        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(f"{url}/health", headers=headers)
                if resp.status_code == 200:
                    status_resp = await client.get(f"{url}/status", headers=headers)
                    details = status_resp.json() if status_resp.status_code == 200 else resp.json()
                    return {
                        "status": "CONNECTED",
                        "is_live": True,
                        "gateway_url": url,
                        "details": details,
                        "message": "Connected to running OpenClaw Gateway service."
                    }
                else:
                    return {
                        "status": "AUTH_REQUIRED" if resp.status_code in [401, 403] else "ERROR",
                        "is_live": False,
                        "gateway_url": url,
                        "message": f"Gateway responded with status code {resp.status_code}."
                    }
        except Exception as e:
            return {
                "status": "DISCONNECTED",
                "is_live": False,
                "gateway_url": url,
                "message": f"Cannot reach OpenClaw service at {url}. Start via: python openclaw/gateway_service.py"
            }

    @classmethod
    async def dispatch_task(cls, agent_type: str, task_prompt: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Dispatch a task to the OpenClaw Gateway runtime."""
        url = cls.get_gateway_url()
        headers = {"Content-Type": "application/json"}
        if settings.OPENCLAW_GATEWAY_TOKEN:
            headers["Authorization"] = f"Bearer {settings.OPENCLAW_GATEWAY_TOKEN}"

        payload = {
            "agent_type": agent_type,
            "task_prompt": task_prompt,
            "session_id": session_id
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(f"{url}/v1/agent/dispatch", json=payload, headers=headers)
                if resp.status_code == 200:
                    return resp.json()
                else:
                    return {
                        "status": "ERROR",
                        "code": resp.status_code,
                        "message": f"OpenClaw dispatch failed: {resp.text}"
                    }
        except Exception as e:
            return {
                "status": "DISCONNECTED",
                "message": f"Could not dispatch to OpenClaw runtime: {str(e)}"
            }
