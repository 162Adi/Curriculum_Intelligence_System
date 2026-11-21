"""
Aggregated SQLAlchemy Models for Curriculum Intelligence System (CIS).
"""

from app.models.base import Base
from app.models.users import User, RoleEnum, AuditLog
from app.models.curriculum import (
    Department,
    Programme,
    CurriculumVersion,
    Course,
    CourseTopic,
    CourseOutcome,
)
from app.models.intelligence import (
    IndustrySnapshot,
    IndustryJob,
    IndustrySkill,
    AcademicStandard,
    BenchmarkDocument,
    BenchmarkResult,
    SkillMapping,
    GapResult,
    Recommendation,
)
from app.models.approvals import ApprovalRecord, Report, ReportVersion
from app.models.agent_history import (
    AgentExecution,
    WorkflowCheckpoint,
    ExecutionEvent,
    ToolInvocation,
    MemoryRecord,
)

__all__ = [
    "Base",
    "User",
    "RoleEnum",
    "AuditLog",
    "Department",
    "Programme",
    "CurriculumVersion",
    "Course",
    "CourseTopic",
    "CourseOutcome",
    "IndustrySnapshot",
    "IndustryJob",
    "IndustrySkill",
    "AcademicStandard",
    "BenchmarkDocument",
    "BenchmarkResult",
    "SkillMapping",
    "GapResult",
    "Recommendation",
    "ApprovalRecord",
    "Report",
    "ReportVersion",
    "AgentExecution",
    "WorkflowCheckpoint",
    "ExecutionEvent",
    "ToolInvocation",
    "MemoryRecord",
]
