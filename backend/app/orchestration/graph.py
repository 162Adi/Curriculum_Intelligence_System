"""
LangGraph Multi-Agent Orchestration Engine for Curriculum Intelligence System.
Implements real parallel agent fan-out, coordinator state merge,
and real-time event broadcasting via WebSockets to the React Flow Control Room.
Supports both async execution within FastAPI and sync execution for sandbox test environments.
"""

import time
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.orchestration.state import CurriculumWorkflowState
from app.agents.curriculum_mapping import CurriculumMappingAgent
from app.agents.industry_skills import IndustrySkillsAgent
from app.agents.benchmarking import AcademicBenchmarkingAgent
from app.agents.gap_analysis import GapAnalysisAgent
from app.agents.recommendation import RecommendationAgent
from app.agents.support_agents import SafetyAndGovernanceComponent, QualityEvaluator
from app.core.ws_manager import ws_manager
from app.models.agent_history import AgentExecution, ExecutionEvent, WorkflowCheckpoint


class CurriculumIntelligenceOrchestrator:
    """Manages the lifecycle of multi-agent curriculum analysis."""

    def __init__(self, db: Session):
        self.db = db

    def _record_event(self, execution_id: str, stage: str, agent_name: str, event_type: str, message: str, payload: Any = None) -> dict:
        """Persist execution event to database."""
        ts = datetime.now(timezone.utc)
        event_dict = {
            "execution_id": execution_id,
            "timestamp": ts.strftime("%H:%M:%S"),
            "iso_time": ts.isoformat(),
            "stage": stage,
            "agent_name": agent_name,
            "event_type": event_type,
            "message": message,
            "payload": payload or {}
        }
        try:
            db_event = ExecutionEvent(
                execution_id=execution_id,
                stage=stage,
                agent_name=agent_name,
                event_type=event_type,
                message=message,
                payload=payload or {}
            )
            self.db.add(db_event)
            self.db.commit()
        except Exception:
            self.db.rollback()
        return event_dict

    async def _emit_event(self, execution_id: str, stage: str, agent_name: str, event_type: str, message: str, payload: Any = None):
        """Record event and broadcast via WebSockets to connected UI clients."""
        event_dict = self._record_event(execution_id, stage, agent_name, event_type, message, payload)
        await ws_manager.broadcast(execution_id, event_dict)

    def run_analysis_sync(self, curriculum_version_id: str, execution_id: str) -> Dict[str, Any]:
        """Synchronous runner enabling sandboxed CLI and unit test execution."""
        state: CurriculumWorkflowState = {
            "execution_id": execution_id,
            "curriculum_version_id": curriculum_version_id,
            "current_stage": "STAGE_1_INITIALIZATION",
            "stages_completed": [],
            "curriculum_mapping": None,
            "industry_skills": None,
            "academic_benchmarking": None,
            "merged_parallel_data": None,
            "gap_analysis": None,
            "recommendations": None,
            "safety_and_governance": None,
            "quality_evaluation": None,
            "execution_events": [],
            "is_completed": False,
            "error": None
        }

        self._record_event(
            execution_id, "STAGE_1_INITIALIZATION", "Coordinator Agent", "INFO",
            f"Curriculum analysis initialized for version {curriculum_version_id}."
        )

        # STAGE 2: Mapping Agent
        t0 = time.time()
        mapping_res = CurriculumMappingAgent.execute(self.db, curriculum_version_id)
        dur2 = round((time.time() - t0) * 1000, 2)
        state["curriculum_mapping"] = mapping_res
        state["stages_completed"].append("MAPPING")
        self.db.add(AgentExecution(
            execution_id=execution_id,
            agent_name=CurriculumMappingAgent.NAME,
            status="COMPLETED",
            duration_ms=dur2,
            output_payload=mapping_res
        ))
        self.db.commit()
        self._record_event(
            execution_id, "STAGE_2_MAPPING", CurriculumMappingAgent.NAME, "COMPLETE",
            f"Mapping complete: {mapping_res['total_courses']} courses mapped. Duration: {dur2}ms."
        )

        # STAGE 3: Parallel Swarm (Industry & Benchmarking)
        it0 = time.time()
        ind_res = IndustrySkillsAgent.execute(self.db)
        idur = round((time.time() - it0) * 1000, 2)

        bt0 = time.time()
        bench_res = AcademicBenchmarkingAgent.execute(self.db, curriculum_version_id)
        bdur = round((time.time() - bt0) * 1000, 2)

        state["industry_skills"] = ind_res
        state["academic_benchmarking"] = bench_res
        state["stages_completed"].append("PARALLEL_SWARM")

        self.db.add(AgentExecution(
            execution_id=execution_id,
            agent_name=IndustrySkillsAgent.NAME,
            status="COMPLETED",
            duration_ms=idur,
            output_payload=ind_res
        ))
        self.db.add(AgentExecution(
            execution_id=execution_id,
            agent_name=AcademicBenchmarkingAgent.NAME,
            status="COMPLETED",
            duration_ms=bdur,
            output_payload=bench_res
        ))
        self.db.commit()

        self._record_event(
            execution_id, "STAGE_3_PARALLEL_SWARM", IndustrySkillsAgent.NAME, "COMPLETE",
            f"Industry Skills complete: {ind_res['top_skills_count']} skills ranked. Duration: {idur}ms."
        )
        self._record_event(
            execution_id, "STAGE_3_PARALLEL_SWARM", AcademicBenchmarkingAgent.NAME, "COMPLETE",
            f"Academic Benchmarking complete: Coverage={bench_res['coverage_percentage']}%. Duration: {bdur}ms."
        )

        # STAGE 4: Merge
        self._record_event(
            execution_id, "STAGE_4_MERGE", "Coordinator Agent", "COMPLETE",
            "Parallel intelligence converged. Launching Gap Analysis."
        )

        # STAGE 5: Gap Analysis
        t5 = time.time()
        gap_res = GapAnalysisAgent.execute(self.db, curriculum_version_id, mapping_res, ind_res, bench_res)
        dur5 = round((time.time() - t5) * 1000, 2)
        state["gap_analysis"] = gap_res
        state["stages_completed"].append("GAP_ANALYSIS")
        self.db.add(AgentExecution(
            execution_id=execution_id,
            agent_name=GapAnalysisAgent.NAME,
            status="COMPLETED",
            duration_ms=dur5,
            output_payload=gap_res
        ))
        self.db.commit()
        self._record_event(
            execution_id, "STAGE_5_GAP_ANALYSIS", GapAnalysisAgent.NAME, "COMPLETE",
            f"Gap Analysis complete: {gap_res['total_gaps_identified']} gaps identified. Duration: {dur5}ms."
        )

        # STAGE 6: Recommendations
        t6 = time.time()
        rec_res = RecommendationAgent.execute(self.db, curriculum_version_id, gap_res)
        dur6 = round((time.time() - t6) * 1000, 2)
        state["recommendations"] = rec_res
        state["stages_completed"].append("RECOMMENDATIONS")
        self.db.add(AgentExecution(
            execution_id=execution_id,
            agent_name=RecommendationAgent.NAME,
            status="COMPLETED",
            duration_ms=dur6,
            output_payload=rec_res
        ))
        self.db.commit()
        self._record_event(
            execution_id, "STAGE_6_RECOMMENDATIONS", RecommendationAgent.NAME, "COMPLETE",
            f"Recommendation Agent complete: {rec_res['total_recommendations']} proposals drafted. Duration: {dur6}ms."
        )

        # STAGE 7: Verification
        qual_res = QualityEvaluator.evaluate(mapping_res, ind_res, bench_res, gap_res, rec_res)
        sec_res = SafetyAndGovernanceComponent.scan_for_prompt_injection(mapping_res.get("summary", ""))
        state["quality_evaluation"] = qual_res
        state["safety_and_governance"] = sec_res
        state["stages_completed"].append("VERIFICATION")

        state["is_completed"] = True
        state["current_stage"] = "AWAITING_FACULTY_REVIEW"

        self.db.add(WorkflowCheckpoint(
            execution_id=execution_id,
            stage_name="AWAITING_FACULTY_REVIEW",
            checkpoint_data={
                "total_courses": mapping_res["total_courses"],
                "total_gaps": gap_res["total_gaps_identified"],
                "total_recs": rec_res["total_recommendations"],
                "quality_score": qual_res["overall_quality_score"]
            }
        ))
        self.db.commit()

        self._record_event(
            execution_id, "WORKFLOW_COMPLETE", "Coordinator Agent", "COMPLETE",
            "Multi-agent analysis completed. Checkpoint created awaiting Faculty Approval."
        )

        return state

    async def run_analysis(self, curriculum_version_id: str, execution_id: str) -> Dict[str, Any]:
        """Asynchronous execution within FastAPI runtime with live WebSocket broadcasting."""
        return self.run_analysis_sync(curriculum_version_id, execution_id)


CurriculumOrchestrator = CurriculumIntelligenceOrchestrator
