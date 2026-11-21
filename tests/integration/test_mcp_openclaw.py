"""
Integration tests for the official MCP Server and OpenClaw Runtime Adapter.
"""
import pytest
from mcp_server.server import invoke_mcp_tool, ToolInvocationRequest, MCP_TOOLS
from openclaw.adapter.runtime_adapter import OpenClawRuntimeAdapter


def test_mcp_tool_catalog():
    """Verify official MCP Server registers all required curriculum intelligence tools."""
    tool_names = [t["name"] if isinstance(t, dict) else t for t in MCP_TOOLS]
    assert "calculate_curriculum_gaps" in tool_names
    assert "search_industry_jobs" in tool_names
    assert "retrieve_academic_standard" in tool_names
    assert "map_course_topics" in tool_names
    assert "generate_curriculum_report" in tool_names


def test_mcp_gap_tool_execution():
    """Test invoking calculate_curriculum_gaps via MCP JSON-RPC tool invocation."""
    req = ToolInvocationRequest(
        tool_name="calculate_curriculum_gaps",
        arguments={"importance_score": 0.85, "coverage_score": 0.20}
    )
    res = invoke_mcp_tool(req)
    assert res["status"] == "SUCCESS"
    # 0.85 * (1 - 0.20) = 0.68
    assert res["result"]["gap_score"] == 0.68
    assert res["result"]["severity"] == "HIGH"


def test_openclaw_adapter_interface():
    """Verify OpenClaw adapter session and runtime endpoints."""
    session = OpenClawRuntimeAdapter.create_worker_payload(
        session_id="SESSION-TEST-001",
        task_name="CURRICULUM_BENCHMARK",
        params={"discipline": "Computer Science"}
    )
    assert session["session_id"] == "SESSION-TEST-001"
    assert session["gateway_port"] == 18789
    assert session["state"] == "INITIALIZED"
