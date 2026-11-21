"""
Gap Analysis API: Retrieve and inspect identified curriculum gaps with score breakdown.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.session import get_db
from app.models.users import User
from app.models.intelligence import GapResult
from app.auth.rbac import get_current_user

router = APIRouter(prefix="/gaps", tags=["Gap Analysis"])


@router.get("")
def list_gaps(
    curriculum_version_id: Optional[str] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve ranked curriculum gaps with score breakdowns."""
    stmt = select(GapResult)
    if curriculum_version_id:
        stmt = stmt.where(GapResult.curriculum_version_id == curriculum_version_id)
    if category:
        stmt = stmt.where(GapResult.category == category)
    if severity:
        stmt = stmt.where(GapResult.severity == severity)

    stmt = stmt.order_by(GapResult.gap_score.desc())
    gaps = db.execute(stmt).scalars().all()

    return [
        {
            "id": g.id,
            "gap_id": g.gap_id,
            "curriculum_version_id": g.curriculum_version_id,
            "title": g.title,
            "description": g.description,
            "category": g.category,
            "affected_semester": g.affected_semester,
            "affected_course_title": g.course.course_title if g.course else "General Core / New Elective",
            "related_skills": g.related_skills,
            "related_benchmark_ref": g.related_benchmark_ref,
            "importance_score": g.importance_score,
            "coverage_score": g.coverage_score,
            "gap_score": g.gap_score,
            "severity": g.severity,
            "priority_rank": g.priority_rank,
            "supporting_evidence": g.supporting_evidence,
            "recommended_action": g.recommended_action
        }
        for g in gaps
    ]


@router.get("/by-curriculum/{curriculum_id}")
@router.get("/{gap_id}")
def get_gap_detail(
    gap_id: str,
    curriculum_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve detailed analysis for a specific gap, or all gaps if curriculum_id is provided."""
    target_id = curriculum_id or gap_id
    
    # Check if target_id corresponds to a curriculum version
    curr_gaps = db.execute(
        select(GapResult).where(GapResult.curriculum_version_id == target_id).order_by(GapResult.gap_score.desc())
    ).scalars().all()
    if curr_gaps:
        return [
            {
                "id": g.id,
                "gap_id": g.gap_id,
                "curriculum_version_id": g.curriculum_version_id,
                "title": g.title,
                "description": g.description,
                "category": g.category,
                "affected_semester": g.affected_semester,
                "affected_course_title": g.course.course_title if g.course else "General Core / New Elective",
                "related_skills": g.related_skills,
                "related_benchmark_ref": g.related_benchmark_ref,
                "importance_score": g.importance_score,
                "coverage_score": g.coverage_score,
                "gap_score": g.gap_score,
                "severity": g.severity,
                "priority_rank": g.priority_rank,
                "supporting_evidence": g.supporting_evidence,
                "recommended_action": g.recommended_action
            }
            for g in curr_gaps
        ]

    # Individual gap lookup
    gap = db.execute(select(GapResult).where(GapResult.id == target_id)).scalar_one_or_none()
    if not gap:
        gap = db.execute(select(GapResult).where(GapResult.gap_id == target_id)).scalar_one_or_none()
    if not gap:
        # Fall back to returning all gaps or empty list
        all_gaps = db.execute(select(GapResult).order_by(GapResult.gap_score.desc())).scalars().all()
        if all_gaps:
            return [
                {
                    "id": g.id,
                    "gap_id": g.gap_id,
                    "curriculum_version_id": g.curriculum_version_id,
                    "title": g.title,
                    "description": g.description,
                    "category": g.category,
                    "affected_semester": g.affected_semester,
                    "affected_course_title": g.course.course_title if g.course else "General Core / New Elective",
                    "related_skills": g.related_skills,
                    "related_benchmark_ref": g.related_benchmark_ref,
                    "importance_score": g.importance_score,
                    "coverage_score": g.coverage_score,
                    "gap_score": g.gap_score,
                    "severity": g.severity,
                    "priority_rank": g.priority_rank,
                    "supporting_evidence": g.supporting_evidence,
                    "recommended_action": g.recommended_action
                }
                for g in all_gaps
            ]
        return []

    return {
        "id": gap.id,
        "gap_id": gap.gap_id,
        "title": gap.title,
        "description": gap.description,
        "category": gap.category,
        "affected_semester": gap.affected_semester,
        "affected_course": gap.course.course_title if gap.course else None,
        "score_formula": "Gap Score = Importance * (1.0 - Coverage)",
        "importance_score": gap.importance_score,
        "coverage_score": gap.coverage_score,
        "gap_score": gap.gap_score,
        "severity": gap.severity,
        "priority_rank": gap.priority_rank,
        "supporting_evidence": gap.supporting_evidence,
        "recommended_action": gap.recommended_action
    }
