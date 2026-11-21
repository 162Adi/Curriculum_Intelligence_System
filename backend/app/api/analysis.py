"""
Curriculum Analysis Execution API: Start, monitor, and stream multi-agent execution.
"""

import asyncio
import uuid
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.database.session import get_db, SessionLocal
from app.models.users import User, RoleEnum
from app.models.curriculum import CurriculumVersion
from app.models.agent_history import AgentExecution, ExecutionEvent, WorkflowCheckpoint
from app.models.intelligence import GapResult, Recommendation, BenchmarkResult
from app.orchestration.graph import CurriculumIntelligenceOrchestrator
from app.auth.rbac import get_current_user, require_role, log_audit_event

router = APIRouter(prefix="/analysis", tags=["Curriculum Analysis"])


async def _run_analysis_background(curriculum_version_id: str, execution_id: str):
    """Background runner for full multi-agent orchestration."""
    with SessionLocal() as db:
        orchestrator = CurriculumIntelligenceOrchestrator(db)
        await orchestrator.run_analysis(curriculum_version_id, execution_id)


@router.post("/start")
async def start_analysis(
    payload: dict,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY]))
):
    """Launch full LangGraph multi-agent analysis on a curriculum version."""
    curriculum_version_id = payload.get("curriculum_version_id") or payload.get("curriculum_id")
    if not curriculum_version_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="curriculum_version_id required")

    curr = db.execute(select(CurriculumVersion).where(CurriculumVersion.id == curriculum_version_id)).scalar_one_or_none()
    if not curr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculum version not found")

    execution_id = f"EXEC-{uuid.uuid4().hex[:12].upper()}"

    # Update curriculum status
    curr.status = "ANALYSIS_RUNNING"
    db.commit()

    log_audit_event(
        db=db,
        action="ANALYSIS_STARTED",
        resource_type="CURRICULUM_VERSION",
        resource_id=curr.id,
        user_id=current_user.id,
        details={"execution_id": execution_id}
    )

    # Start background task
    background_tasks.add_task(_run_analysis_background, curriculum_version_id, execution_id)

    return {
        "execution_id": execution_id,
        "curriculum_version_id": curr.id,
        "status": "RUNNING",
        "message": "Curriculum analysis launched. Connect to /ws/executions/" + execution_id + " for real-time live events."
    }


@router.get("/{execution_id}/status")
@router.get("/{execution_id}")
def get_analysis_status(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get live execution state, checkpoints, and completed agent stages."""
    executions = db.execute(
        select(AgentExecution).where(AgentExecution.execution_id == execution_id)
    ).scalars().all()

    checkpoint = db.execute(
        select(WorkflowCheckpoint)
        .where(WorkflowCheckpoint.execution_id == execution_id)
        .order_by(desc(WorkflowCheckpoint.created_at))
    ).scalars().first()

    events_count = len(db.execute(
        select(ExecutionEvent).where(ExecutionEvent.execution_id == execution_id)
    ).scalars().all())

    is_complete = any(e.agent_name == "Recommendation Agent" and e.status == "COMPLETED" for e in executions)

    return {
        "execution_id": execution_id,
        "is_complete": is_complete,
        "status": "COMPLETED" if is_complete else "RUNNING",
        "total_agent_executions": len(executions),
        "total_events_emitted": events_count,
        "agents": [
            {
                "agent_name": e.agent_name,
                "status": e.status,
                "duration_ms": e.duration_ms,
                "created_at": e.created_at.isoformat()
            }
            for e in executions
        ],
        "latest_checkpoint": checkpoint.checkpoint_data if checkpoint else None
    }


@router.get("/{execution_id}/events")
def get_execution_events(
    execution_id: str,
    limit: int = 150,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve chronological log of all real backend execution events."""
    events = db.execute(
        select(ExecutionEvent)
        .where(ExecutionEvent.execution_id == execution_id)
        .order_by(ExecutionEvent.created_at.asc())
        .limit(limit)
    ).scalars().all()

    return [
        {
            "id": ev.id,
            "timestamp": ev.created_at.strftime("%H:%M:%S"),
            "stage": ev.stage,
            "agent_name": ev.agent_name,
            "event_type": ev.event_type,
            "message": ev.message,
            "payload": ev.payload
        }
        for ev in events
    ]


@router.get("/{execution_id}/results")
def get_analysis_results(
    execution_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve complete merged results from all analysis agents."""
    executions = db.execute(
        select(AgentExecution).where(AgentExecution.execution_id == execution_id)
    ).scalars().all()

    results_map = {}
    for ex in executions:
        results_map[ex.agent_name] = ex.output_payload

    return {
        "execution_id": execution_id,
        "curriculum_mapping": results_map.get("Curriculum Mapping Agent"),
        "industry_skills": results_map.get("Industry Skills Agent"),
        "academic_benchmarking": results_map.get("Academic Benchmarking Agent"),
        "gap_analysis": results_map.get("Gap Analysis Agent"),
        "recommendations": results_map.get("Recommendation Agent")
    }


@router.get("/{curriculum_id}/history")
def get_curriculum_analysis_history(
    curriculum_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve history of agent executions for a curriculum."""
    executions = db.execute(
        select(AgentExecution).order_by(desc(AgentExecution.created_at)).limit(20)
    ).scalars().all()
    return [
        {
            "id": e.id,
            "execution_id": e.execution_id,
            "agent_name": e.agent_name,
            "status": e.status,
            "duration_ms": e.duration_ms,
            "created_at": e.created_at.isoformat()
        }
        for e in executions
    ]
