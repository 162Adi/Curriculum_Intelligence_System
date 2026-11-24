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


@router.post("/recommendations/{recommendation_id}")
def submit_recommendation_decision(
    recommendation_id: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY, RoleEnum.MANAGEMENT]))
):
    """Faculty or Board of Studies member approves, rejects, or requests revision on a recommendation."""
    raw_decision = payload.get("decision", "APPROVED").upper()
    comments = payload.get("comments", "")

    rec = db.execute(select(Recommendation).where(Recommendation.id == recommendation_id)).scalar_one_or_none()
    if not rec:
        rec = db.execute(select(Recommendation).where(Recommendation.recommendation_id == recommendation_id)).scalar_one_or_none()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    old_status = rec.status
    if raw_decision in ["APPROVED", "APPROVE"]:
        new_status = "APPROVED"
    elif raw_decision in ["REJECTED", "REJECT"]:
        new_status = "REJECTED"
    elif raw_decision in ["REVISE", "REVISION", "NEEDS_REVISION"]:
        new_status = "NEEDS_REVISION"
    else:
        new_status = raw_decision

    rec.status = new_status
    if comments:
        rec.faculty_notes = comments

    # Record granular approval decision in audit table
    record = ApprovalRecord(
        recommendation_id=rec.id,
        curriculum_version_id=rec.curriculum_version_id,
        reviewer_id=current_user.id,
        action=new_status,
        comments=comments or f"Marked as {new_status} by {current_user.full_name}.",
        previous_state={"status": old_status},
        new_state={"status": new_status}
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    db.refresh(rec)

    log_audit_event(
        db=db,
        action=f"RECOMMENDATION_{new_status}",
        resource_type="RECOMMENDATION",
        resource_id=rec.id,
        user_id=current_user.id,
        details={
            "decision": new_status,
            "reviewer": current_user.full_name,
            "comments": comments
        }
    )

    return {
        "id": record.id,
        "curriculum_id": rec.curriculum_version_id,
        "recommendation_id": rec.id,
        "user_id": current_user.id,
        "user_name": current_user.full_name,
        "user_role": current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role),
        "decision": new_status,
        "action": new_status,
        "status": new_status,
        "approval_status": new_status,
        "comments": comments,
        "created_at": record.created_at.isoformat()
    }


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
            "decision": r.action,
            "comments": r.comments,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]


@router.get("/{curriculum_id}")
def get_approvals_by_curriculum(
    curriculum_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all approval records for a given curriculum version."""
    stmt = (
        select(ApprovalRecord)
        .where(ApprovalRecord.curriculum_version_id == curriculum_id)
        .order_by(desc(ApprovalRecord.created_at))
    )
    records = db.execute(stmt).scalars().all()

    return [
        {
            "id": r.id,
            "curriculum_id": r.curriculum_version_id,
            "recommendation_id": r.recommendation_id,
            "recommendation_title": r.recommendation.title if r.recommendation else None,
            "user_id": r.reviewer_id,
            "user_name": r.reviewer.full_name if r.reviewer else "Faculty Reviewer",
            "user_role": r.reviewer.role.value if (r.reviewer and hasattr(r.reviewer.role, "value")) else "FACULTY",
            "decision": r.action,
            "action": r.action,
            "comments": r.comments,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]


@router.post("/{curriculum_id}/signoff")
@router.post("/finalize-report")
def signoff_and_finalize_report(
    curriculum_id: Optional[str] = None,
    payload: dict = {},
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY, RoleEnum.MANAGEMENT]))
):
    """Faculty Senate and Board of Studies formal curriculum sign-off sealing the version for accreditation."""
    target_curr_id = curriculum_id or payload.get("curriculum_version_id")
    comments = payload.get("comments") or "Officially approved and endorsed by Board of Studies."

    curr = None
    if target_curr_id:
        curr = db.execute(select(CurriculumVersion).where(CurriculumVersion.id == target_curr_id)).scalar_one_or_none()

    if not curr:
        curr = db.execute(select(CurriculumVersion).order_by(desc(CurriculumVersion.created_at))).scalars().first()

    if not curr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculum version not found")

    recs = db.execute(
        select(Recommendation).where(Recommendation.curriculum_version_id == curr.id)
    ).scalars().all()

    approved_count = sum(1 for r in recs if r.status == "APPROVED")
    rejected_count = sum(1 for r in recs if r.status == "REJECTED")

    curr.status = "APPROVED"

    report = db.execute(
        select(Report).where(Report.curriculum_version_id == curr.id).order_by(desc(Report.created_at))
    ).scalars().first()

    if not report:
        report = Report(
            curriculum_version_id=curr.id,
            title=f"Curriculum Intelligence & Industry Alignment Report - {curr.version_tag}",
            report_type="FACULTY_APPROVED",
            status="FINALIZED",
            generated_by_user_id=current_user.id
        )
        db.add(report)

    report.status = "FINALIZED"
    report.summary_data = {
        "approved_by": current_user.full_name,
        "approved_date": datetime.now(timezone.utc).isoformat(),
        "approved_recommendations_count": approved_count,
        "rejected_recommendations_count": rejected_count,
        "faculty_comments": comments
    }

    db.commit()
    db.refresh(curr)
    db.refresh(report)

    log_audit_event(
        db=db,
        action="FINAL_CURRICULUM_SIGNOFF",
        resource_type="REPORT",
        resource_id=report.id,
        user_id=current_user.id,
        details={
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "curriculum_version": curr.version_tag,
            "comments": comments
        }
    )

    return {
        "status": "APPROVED",
        "report_id": report.id,
        "curriculum_id": curr.id,
        "message": f"Curriculum version {curr.version_tag} has been formally sealed and signed off by Board of Studies.",
        "approved_count": approved_count,
        "rejected_count": rejected_count
    }
