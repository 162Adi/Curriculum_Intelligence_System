"""
End-to-End Test for the Curriculum Intelligence System Orchestration Pipeline.
Executes the LangGraph Multi-Agent Workflow on real curriculum data.
"""
import pytest
from app.orchestration.graph import CurriculumOrchestrator


def test_full_curriculum_analysis_pipeline(db_session, sample_curriculum):
    """
    Executes:
    1. Curriculum Mapping Agent (Normalizes syllabus structure)
    2. Parallel Swarm (Industry Skills, Academic Benchmarks, Prerequisites, Deep Research)
    3. Coordinator Convergence (Synthesizes evidence)
    4. Deterministic Gap Engine (Computes Gap = Importance * (1 - Coverage))
    5. Recommendation Agent (Generates DRAFT proposals)
    6. Quality & Safety Verification (Checks citations, hallucination, injections)
    """
    orchestrator = CurriculumOrchestrator(db_session)
    result = orchestrator.run_analysis_sync(
        curriculum_version_id=sample_curriculum.id,
        execution_id="E2E-TEST-EXEC-001"
    )

    assert result["is_completed"] is True
    assert "MAPPING" in result["stages_completed"]
    assert "PARALLEL_SWARM" in result["stages_completed"]
    assert "GAP_ANALYSIS" in result["stages_completed"]
    assert "RECOMMENDATIONS" in result["stages_completed"]
    assert "VERIFICATION" in result["stages_completed"]

    assert result["gap_analysis"]["total_gaps_identified"] > 0
    assert result["recommendations"]["total_recommendations"] > 0
    assert result["quality_evaluation"]["overall_quality_score"] >= 95.0
