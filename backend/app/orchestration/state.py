"""
Typed State Definition for LangGraph Curriculum Intelligence Workflow.
"""

from typing import Dict, Any, List, Optional, TypedDict


class CurriculumWorkflowState(TypedDict):
    """Shared typed state passed between nodes in the LangGraph execution graph."""
    execution_id: str
    curriculum_version_id: str
    current_stage: str
    stages_completed: List[str]
    curriculum_mapping: Optional[Dict[str, Any]]
    industry_skills: Optional[Dict[str, Any]]
    academic_benchmarking: Optional[Dict[str, Any]]
    merged_parallel_data: Optional[Dict[str, Any]]
    gap_analysis: Optional[Dict[str, Any]]
    recommendations: Optional[Dict[str, Any]]
    safety_and_governance: Optional[Dict[str, Any]]
    quality_evaluation: Optional[Dict[str, Any]]
    execution_events: List[Dict[str, Any]]
    is_completed: bool
    error: Optional[str]
