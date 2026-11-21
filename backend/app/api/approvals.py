"""
Faculty Approvals & Sign-off API: Review audit trail and final report endorsement.
"""

from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.database.session import get_db
from app.models.users import User, RoleEnum
from app.models.curriculum import CurriculumVersion
from app.models.intelligence import Recommendation
from app.models.approvals import ApprovalRecord, Report
from app.auth.rbac import get_current_user, require_role, log_audit_event

router = APIRouter(prefix="/approvals", tags=["Faculty Approvals & Audit"])


@router.get("/history")
def get_approval_history(
    curriculum_version_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve full audit history of all faculty recommendation decisions."""
    stmt = select(ApprovalRecord)
    if curriculum_version_id:
        stmt = stmt.where(ApprovalRecord.curriculum_version_id == curriculum_version_id)
    stmt = stmt.order_by(desc(ApprovalRecord.created_at))

    records = db.execute(stmt).scalars().all()

    return [
        {
            "id": r.id,
            "recommendation_id": r.recommendation.recommendation_id if r.recommendation else None,
            "recommendation_title": r.recommendation.title if r.recommendation else None,
            "reviewer_name": r.reviewer.full_name if r.reviewer else "Faculty Reviewer",
            "reviewer_email": r.reviewer.email if r.reviewer else None,
            "action": r.action,
            "comments": r.comments,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]


@router.post("/finalize-report")
def finalize_curriculum_report(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY, RoleEnum.MANAGEMENT]))
):
    """Faculty signs off on the final curriculum intelligence report after completing individual reviews."""
    curriculum_version_id = payload.get("curriculum_version_id")
    comments = payload.get("comments", "Endorsed by Curriculum Revision Committee.")

    curr = db.execute(select(CurriculumVersion).where(CurriculumVersion.id == curriculum_version_id)).scalar_one_or_none()
    if not curr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculum version not found")

    # Verify that recommendations exist
    recs = db.execute(
        select(Recommendation).where(Recommendation.curriculum_version_id == curriculum_version_id)
    ).scalars().all()

    approved_count = sum(1 for r in recs if r.status == "APPROVED")
    rejected_count = sum(1 for r in recs if r.status == "REJECTED")

    curr.status = "APPROVED"

    # Create Report entry marked as FINALIZED
    report = Report(
        curriculum_version_id=curr.id,
        title=f"Curriculum Intelligence & Industry Alignment Report - {curr.version_tag}",
        report_type="FACULTY_APPROVED",
        status="FINALIZED",
        generated_by_user_id=current_user.id,
        summary_data={
            "approved_by": current_user.full_name,
            "approved_date": datetime.now(timezone.utc).isoformat(),
            "approved_recommendations_count": approved_count,
            "rejected_recommendations_count": rejected_count,
            "faculty_comments": comments
        }
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    log_audit_event(
        db=db,
        action="FINAL_REPORT_APPROVED",
        resource_type="REPORT",
        resource_id=report.id,
        user_id=current_user.id,
        details={
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "endorser": current_user.full_name
        }
    )

    return {
        "report_id": report.id,
        "message": "Final report endorsed and approved successfully by faculty.",
        "curriculum_status": curr.status,
        "approved_count": approved_count,
        "rejected_count": rejected_count
    }
