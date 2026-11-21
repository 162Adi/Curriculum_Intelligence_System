"""
Recommendations API: Faculty review, editing, granular approvals, and rejections.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.session import get_db
from app.models.users import User, RoleEnum
from app.models.intelligence import Recommendation, GapResult
from app.models.approvals import ApprovalRecord
from app.auth.rbac import get_current_user, require_role, log_audit_event

router = APIRouter(prefix="/recommendations", tags=["Recommendations & Faculty Review"])


@router.get("")
def list_recommendations(
    curriculum_version_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all recommendations with granular faculty approval statuses."""
    stmt = select(Recommendation)
    if curriculum_version_id:
        stmt = stmt.where(Recommendation.curriculum_version_id == curriculum_version_id)
    if status_filter:
        stmt = stmt.where(Recommendation.status == status_filter)
    if category:
        stmt = stmt.where(Recommendation.category == category)

    recs = db.execute(stmt).scalars().all()

    return [
        {
            "id": r.id,
            "recommendation_id": r.recommendation_id,
            "curriculum_version_id": r.curriculum_version_id,
            "gap_id": r.gap.gap_id if r.gap else None,
            "gap_title": r.gap.title if r.gap else None,
            "category": r.category,
            "title": r.title,
            "description": r.description,
            "affected_semester": r.affected_semester,
            "affected_course_title": r.course.course_title if r.course else None,
            "rationale": r.rationale,
            "industry_evidence": r.industry_evidence,
            "academic_reference": r.academic_reference,
            "estimated_effort": r.estimated_effort,
            "expected_benefit": r.expected_benefit,
            "priority": r.priority,
            "status": r.status,  # DRAFT, SUBMITTED, UNDER_REVIEW, APPROVED, REJECTED, NEEDS_REVISION
            "faculty_notes": r.faculty_notes,
            "created_at": r.created_at.isoformat()
        }
        for r in recs
    ]


@router.get("/by-curriculum/{curriculum_id}")
@router.get("/{recommendation_id}")
def get_recommendations_or_detail(
    recommendation_id: str,
    curriculum_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve detailed recommendation, or all recommendations if curriculum_id is provided."""
    target_id = curriculum_id or recommendation_id

    # Check if target_id is a curriculum_version_id
    curr_recs = db.execute(
        select(Recommendation).where(Recommendation.curriculum_version_id == target_id)
    ).scalars().all()
    if curr_recs:
        return [
            {
                "id": r.id,
                "recommendation_id": r.recommendation_id,
                "curriculum_version_id": r.curriculum_version_id,
                "gap_id": r.gap.gap_id if r.gap else None,
                "gap_title": r.gap.title if r.gap else None,
                "category": r.category,
                "title": r.title,
                "description": r.description,
                "affected_semester": r.affected_semester,
                "affected_course_title": r.course.course_title if r.course else None,
                "rationale": r.rationale,
                "industry_evidence": r.industry_evidence,
                "academic_reference": r.academic_reference,
                "estimated_effort": r.estimated_effort,
                "expected_benefit": r.expected_benefit,
                "priority": r.priority,
                "status": r.status,
                "approval_status": r.status,
                "faculty_notes": r.faculty_notes,
                "created_at": r.created_at.isoformat()
            }
            for r in curr_recs
        ]

    rec = db.execute(select(Recommendation).where(Recommendation.id == target_id)).scalar_one_or_none()
    if not rec:
        rec = db.execute(select(Recommendation).where(Recommendation.recommendation_id == target_id)).scalar_one_or_none()
    if not rec:
        # Fallback to returning all existing recommendations if any
        all_recs = db.execute(select(Recommendation)).scalars().all()
        if all_recs:
            return [
                {
                    "id": r.id,
                    "recommendation_id": r.recommendation_id,
                    "curriculum_version_id": r.curriculum_version_id,
                    "gap_id": r.gap.gap_id if r.gap else None,
                    "gap_title": r.gap.title if r.gap else None,
                    "category": r.category,
                    "title": r.title,
                    "description": r.description,
                    "affected_semester": r.affected_semester,
                    "affected_course_title": r.course.course_title if r.course else None,
                    "rationale": r.rationale,
                    "industry_evidence": r.industry_evidence,
                    "academic_reference": r.academic_reference,
                    "estimated_effort": r.estimated_effort,
                    "expected_benefit": r.expected_benefit,
                    "priority": r.priority,
                    "status": r.status,
                    "approval_status": r.status,
                    "faculty_notes": r.faculty_notes,
                    "created_at": r.created_at.isoformat()
                }
                for r in all_recs
            ]
        return []

    return {
        "id": rec.id,
        "recommendation_id": rec.recommendation_id,
        "title": rec.title,
        "description": rec.description,
        "category": rec.category,
        "priority": rec.priority,
        "status": rec.status,
        "approval_status": rec.status
    }


@router.patch("/{recommendation_id}")
def edit_recommendation(
    recommendation_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY]))
):
    """Faculty edits recommendation draft content, semester, effort, or notes."""
    rec = db.execute(select(Recommendation).where(Recommendation.id == recommendation_id)).scalar_one_or_none()
    if not rec:
        rec = db.execute(select(Recommendation).where(Recommendation.recommendation_id == recommendation_id)).scalar_one_or_none()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    for field in ["title", "description", "category", "estimated_effort", "expected_benefit", "priority", "faculty_notes"]:
        if field in payload and payload[field] is not None:
            setattr(rec, field, payload[field])

    if "affected_semester" in payload and payload["affected_semester"] is not None:
        rec.affected_semester = int(payload["affected_semester"])

    db.commit()
    db.refresh(rec)

    log_audit_event(
        db=db,
        action="RECOMMENDATION_EDITED_BY_FACULTY",
        resource_type="RECOMMENDATION",
        resource_id=rec.id,
        user_id=current_user.id
    )

    return {"message": "Recommendation proposal updated successfully", "id": rec.id}


@router.post("/{recommendation_id}/approve")
def approve_recommendation(
    recommendation_id: str,
    payload: dict = {},
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY]))
):
    """Faculty formally approves a curriculum recommendation."""
    rec = db.execute(select(Recommendation).where(Recommendation.id == recommendation_id)).scalar_one_or_none()
    if not rec:
        rec = db.execute(select(Recommendation).where(Recommendation.recommendation_id == recommendation_id)).scalar_one_or_none()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    old_status = rec.status
    rec.status = "APPROVED"
    if payload.get("comments"):
        rec.faculty_notes = payload.get("comments")

    # Record granular approval decision
    record = ApprovalRecord(
        recommendation_id=rec.id,
        curriculum_version_id=rec.curriculum_version_id,
        reviewer_id=current_user.id,
        action="APPROVED",
        comments=payload.get("comments", "Approved by Faculty Committee."),
        previous_state={"status": old_status},
        new_state={"status": "APPROVED"}
    )
    db.add(record)
    db.commit()

    log_audit_event(
        db=db,
        action="RECOMMENDATION_APPROVED",
        resource_type="RECOMMENDATION",
        resource_id=rec.id,
        user_id=current_user.id,
        details={"reviewer": current_user.full_name}
    )

    return {"message": f"Recommendation {rec.recommendation_id} approved.", "status": rec.status}


@router.post("/{recommendation_id}/reject")
def reject_recommendation(
    recommendation_id: str,
    payload: dict = {},
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY]))
):
    """Faculty rejects a curriculum recommendation with justification."""
    rec = db.execute(select(Recommendation).where(Recommendation.id == recommendation_id)).scalar_one_or_none()
    if not rec:
        rec = db.execute(select(Recommendation).where(Recommendation.recommendation_id == recommendation_id)).scalar_one_or_none()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    old_status = rec.status
    rec.status = "REJECTED"
    if payload.get("comments"):
        rec.faculty_notes = payload.get("comments")

    record = ApprovalRecord(
        recommendation_id=rec.id,
        curriculum_version_id=rec.curriculum_version_id,
        reviewer_id=current_user.id,
        action="REJECTED",
        comments=payload.get("comments", "Rejected by Faculty Committee."),
        previous_state={"status": old_status},
        new_state={"status": "REJECTED"}
    )
    db.add(record)
    db.commit()

    log_audit_event(
        db=db,
        action="RECOMMENDATION_REJECTED",
        resource_type="RECOMMENDATION",
        resource_id=rec.id,
        user_id=current_user.id,
        details={"reason": payload.get("comments")}
    )

    return {"message": f"Recommendation {rec.recommendation_id} rejected.", "status": rec.status}
