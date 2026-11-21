"""
Agent execution history, live workflow checkpoints, tool invocations, and memory records.
"""

import uuid
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, Integer, Float, ForeignKey, JSON, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class AgentExecution(Base):
    __tablename__ = "agent_executions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    agent_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="WAITING")  # WAITING, RUNNING, COMPLETED, FAILED, RETRIED
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    input_payload: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    output_payload: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    token_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class WorkflowCheckpoint(Base):
    __tablename__ = "workflow_checkpoints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    stage_name: Mapped[str] = mapped_column(String(100), nullable=False)
    checkpoint_data: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)


class ExecutionEvent(Base):
    __tablename__ = "execution_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    stage: Mapped[str] = mapped_column(String(100), nullable=False)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), default="INFO")  # INFO, TOOL_CALL, MEMORY_READ, WARNING, ERROR, COMPLETE
    message: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)


class ToolInvocation(Base):
    __tablename__ = "tool_invocations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    caller_agent: Mapped[str] = mapped_column(String(100), nullable=False)
    input_args: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    output_result: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    duration_ms: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="SUCCESS")  # SUCCESS, ERROR


class MemoryRecord(Base):
    __tablename__ = "memory_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    memory_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # SHORT_TERM, LONG_TERM, SEMANTIC
    scope_type: Mapped[str] = mapped_column(String(50), default="PROGRAMME")  # GLOBAL, DEPARTMENT, PROGRAMME, VERSION
    scope_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    key: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    embedding_json: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)  # Stores vector embedding array
    access_count: Mapped[int] = mapped_column(Integer, default=0)
    last_accessed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
