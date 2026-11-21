"""
Curriculum Workspace API: File upload, structure extraction, faculty review, and course editing.
"""

import os
import shutil
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.session import get_db
from app.models.users import User, RoleEnum
from app.models.curriculum import (
    Department,
    Programme,
    CurriculumVersion,
    Course,
    CourseTopic,
    CourseOutcome,
)
from app.ingestion.extractor import CurriculumDocumentExtractor
from app.auth.rbac import get_current_user, require_role, log_audit_event
from app.core.config import settings

router = APIRouter(prefix="/curriculum", tags=["Curriculum Management"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/departments")
def get_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all departments for selection dropdowns."""
    depts = db.execute(select(Department)).scalars().all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "code": d.code,
            "description": d.description
        }
        for d in depts
    ]


@router.get("/programmes")
def get_programmes(
    department_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve academic programmes, optionally filtered by department_id."""
    stmt = select(Programme)
    if department_id:
        stmt = stmt.where(Programme.department_id == department_id)
    progs = db.execute(stmt).scalars().all()
    return [
        {
            "id": p.id,
            "department_id": p.department_id,
            "name": p.name,
            "code": p.code,
            "degree_type": p.degree_type,
            "duration_years": p.duration_years,
            "total_credits": p.total_credits
        }
        for p in progs
    ]


@router.get("/by-programme/{programme_id}")
@router.get("")
def list_curricula(
    programme_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all ingested or active curriculum versions."""
    stmt = select(CurriculumVersion)
    if programme_id:
        stmt = stmt.where(CurriculumVersion.programme_id == programme_id)
    
    versions = db.execute(stmt).scalars().all()
    return [
        {
            "id": v.id,
            "programme_id": v.programme_id,
            "programme_name": v.programme.name if v.programme else None,
            "department_name": v.programme.department.name if v.programme and v.programme.department else None,
            "version": v.version_tag,
            "version_tag": v.version_tag,
            "academic_year": v.academic_year,
            "status": v.status,
            "file_name": v.file_name,
            "total_courses": v.total_courses,
            "total_credits": v.total_credits,
            "is_active": (v.status != "ARCHIVED"),
            "created_at": v.created_at.isoformat()
        }
        for v in versions
    ]


@router.post("/upload")
def upload_curriculum(
    file: UploadFile = File(...),
    programme_id: Optional[str] = Form(None),
    version_tag: Optional[str] = Form(None),
    version: Optional[str] = Form(None),
    academic_year: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY]))
):
    """Upload curriculum file (PDF/DOCX/XLSX/CSV), extract structured courses and outcomes."""
    eff_version = version_tag or version or "1.0"
    eff_year = academic_year or "2024-2025"

    programme = None
    if programme_id:
        programme = db.execute(select(Programme).where(Programme.id == programme_id)).scalar_one_or_none()

    if not programme:
        programme = db.execute(select(Programme)).scalars().first()

    if not programme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target academic programme not found")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx", ".xlsx", ".xls", ".csv"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format {ext}. Allowed: PDF, DOCX, XLSX, CSV."
        )

    # Save file to disk
    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract curriculum structure
    try:
        parsed_data = CurriculumDocumentExtractor.parse_curriculum_structure(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to extract document contents: {str(e)}"
        )

    # Create CurriculumVersion
    curriculum_ver = CurriculumVersion(
        programme_id=programme.id,
        version_tag=eff_version,
        academic_year=eff_year,
        status="INGESTED",
        file_name=file.filename,
        file_path=file_path,
        extracted_data=parsed_data,
        total_courses=parsed_data["total_courses"],
        total_credits=parsed_data["total_credits"]
    )
    db.add(curriculum_ver)
    db.flush()

    # Populate Course, Topic, and Outcome models
    for c_data in parsed_data["courses"]:
        course = Course(
            curriculum_version_id=curriculum_ver.id,
            semester=c_data["semester"],
            course_code=c_data["course_code"],
            course_title=c_data["course_title"],
            course_type=c_data["course_type"],
            credits=c_data["credits"],
            lecture_hours=c_data["lecture_hours"],
            tutorial_hours=c_data["tutorial_hours"],
            practical_hours=c_data["practical_hours"],
            description=c_data["description"]
        )
        db.add(course)
        db.flush()

        for t_data in c_data.get("topics", []):
            topic = CourseTopic(
                course_id=course.id,
                unit_number=t_data["unit_number"],
                unit_title=t_data["unit_title"],
                topic_name=t_data["topic_name"],
                topic_description=t_data["topic_description"],
                hours_allocated=t_data.get("hours_allocated", 6.0)
            )
            db.add(topic)

        for o_data in c_data.get("outcomes", []):
            outcome = CourseOutcome(
                course_id=course.id,
                outcome_code=o_data["outcome_code"],
                description=o_data["description"],
                bloom_taxonomy_level=o_data.get("bloom_taxonomy_level", "Understand")
            )
            db.add(outcome)

    db.commit()
    db.refresh(curriculum_ver)

    log_audit_event(
        db=db,
        action="CURRICULUM_UPLOADED",
        resource_type="CURRICULUM_VERSION",
        resource_id=curriculum_ver.id,
        user_id=current_user.id,
        details={
            "file_name": file.filename,
            "version_tag": version_tag,
            "total_courses": parsed_data["total_courses"]
        }
    )

    return {
        "id": curriculum_ver.id,
        "message": f"Curriculum ingested successfully with {parsed_data['total_courses']} courses extracted.",
        "version_tag": curriculum_ver.version_tag,
        "total_courses": curriculum_ver.total_courses,
        "total_credits": curriculum_ver.total_credits,
        "status": curriculum_ver.status
    }


@router.get("/{curriculum_id}")
def get_curriculum_details(
    curriculum_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve metadata and courses overview for a specific curriculum version."""
    v = db.execute(select(CurriculumVersion).where(CurriculumVersion.id == curriculum_id)).scalar_one_or_none()
    if not v:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculum version not found")

    courses = db.execute(
        select(Course).where(Course.curriculum_version_id == curriculum_id).order_by(Course.semester, Course.course_code)
    ).scalars().all()

    course_list = []
    for c in courses:
        topics = db.execute(
            select(CourseTopic).where(CourseTopic.course_id == c.id).order_by(CourseTopic.unit_number)
        ).scalars().all()
        outcomes = db.execute(
            select(CourseOutcome).where(CourseOutcome.course_id == c.id)
        ).scalars().all()

        units_map = {}
        for t in topics:
            u_num = t.unit_number
            if u_num not in units_map:
                units_map[u_num] = {
                    "id": t.id,
                    "unit_number": u_num,
                    "title": t.unit_title,
                    "topics": [],
                    "contact_hours": t.hours_allocated
                }
            units_map[u_num]["topics"].append(f"{t.topic_name}: {t.topic_description}")

        course_list.append({
            "id": c.id,
            "curriculum_id": v.id,
            "code": c.course_code,
            "course_code": c.course_code,
            "title": c.course_title,
            "course_title": c.course_title,
            "credits": c.credits,
            "semester": c.semester,
            "course_type": c.course_type,
            "lecture_hours": c.lecture_hours,
            "tutorial_hours": c.tutorial_hours,
            "practical_hours": c.practical_hours,
            "description": c.description,
            "syllabus_text": c.description,
            "units": list(units_map.values()),
            "learning_outcomes": [
                {
                    "id": o.id,
                    "code": o.outcome_code,
                    "description": o.description,
                    "bloom_level": o.bloom_taxonomy_level
                }
                for o in outcomes
            ]
        })

    return {
        "id": v.id,
        "programme_id": v.programme_id,
        "programme_name": v.programme.name if v.programme else None,
        "programme_code": v.programme.code if v.programme else None,
        "department_name": v.programme.department.name if v.programme and v.programme.department else None,
        "version": v.version_tag,
        "version_tag": v.version_tag,
        "academic_year": v.academic_year,
        "status": v.status,
        "file_name": v.file_name,
        "total_courses": len(courses),
        "total_credits": v.total_credits,
        "is_active": (v.status != "ARCHIVED"),
        "created_at": v.created_at.isoformat(),
        "courses": course_list
    }


@router.get("/{curriculum_id}/structure")
def get_curriculum_structure(
    curriculum_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get complete semester-wise tree of courses, topics, and learning outcomes."""
    v = db.execute(select(CurriculumVersion).where(CurriculumVersion.id == curriculum_id)).scalar_one_or_none()
    if not v:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculum version not found")

    courses = db.execute(
        select(Course).where(Course.curriculum_version_id == curriculum_id).order_by(Course.semester, Course.course_code)
    ).scalars().all()

    semesters_map = {}
    for c in courses:
        sem = c.semester
        if sem not in semesters_map:
            semesters_map[sem] = []

        topics = db.execute(select(CourseTopic).where(CourseTopic.course_id == c.id).order_by(CourseTopic.unit_number)).scalars().all()
        outcomes = db.execute(select(CourseOutcome).where(CourseOutcome.course_id == c.id)).scalars().all()

        semesters_map[sem].append({
            "id": c.id,
            "course_code": c.course_code,
            "course_title": c.course_title,
            "course_type": c.course_type,
            "credits": c.credits,
            "lecture_hours": c.lecture_hours,
            "tutorial_hours": c.tutorial_hours,
            "practical_hours": c.practical_hours,
            "description": c.description,
            "topics": [
                {
                    "id": t.id,
                    "unit_number": t.unit_number,
                    "unit_title": t.unit_title,
                    "topic_name": t.topic_name,
                    "topic_description": t.topic_description,
                    "hours_allocated": t.hours_allocated
                }
                for t in topics
            ],
            "outcomes": [
                {
                    "id": o.id,
                    "outcome_code": o.outcome_code,
                    "description": o.description,
                    "bloom_taxonomy_level": o.bloom_taxonomy_level
                }
                for o in outcomes
            ]
        })

    return {
        "curriculum_id": v.id,
        "version_tag": v.version_tag,
        "status": v.status,
        "total_courses": len(courses),
        "semesters": [
            {"semester": sem, "courses": courses_list}
            for sem, courses_list in sorted(semesters_map.items())
        ]
    }


@router.patch("/courses/{course_id}")
@router.patch("/{curriculum_id}/courses/{course_id}")
def update_course_details(
    course_id: str,
    payload: dict,
    curriculum_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY]))
):
    """Faculty review and correction: edit course title, code, credits, type, hours, description."""
    stmt = select(Course).where(Course.id == course_id)
    if curriculum_id:
        stmt = stmt.where(Course.curriculum_version_id == curriculum_id)
    course = db.execute(stmt).scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found in this curriculum")

    for field in ["course_code", "course_title", "course_type", "description"]:
        if field in payload and payload[field] is not None:
            setattr(course, field, payload[field])
        if field == "course_code" and "code" in payload and payload["code"] is not None:
            course.course_code = payload["code"]
        if field == "course_title" and "title" in payload and payload["title"] is not None:
            course.course_title = payload["title"]

    for num_field in ["semester", "lecture_hours", "tutorial_hours", "practical_hours"]:
        if num_field in payload and payload[num_field] is not None:
            setattr(course, num_field, int(payload[num_field]))

    if "credits" in payload and payload["credits"] is not None:
        course.credits = float(payload["credits"])

    db.commit()
    db.refresh(course)

    log_audit_event(
        db=db,
        action="COURSE_EDITED_BY_FACULTY",
        resource_type="COURSE",
        resource_id=course.id,
        user_id=current_user.id,
        details={"updated_fields": list(payload.keys())}
    )

    return {
        "id": course.id,
        "code": course.course_code,
        "course_code": course.course_code,
        "title": course.course_title,
        "course_title": course.course_title,
        "credits": course.credits,
        "semester": course.semester,
        "course_type": course.course_type,
        "description": course.description,
        "message": "Course updated successfully"
    }


@router.post("/{curriculum_id}/confirm-structure")
@router.post("/{curriculum_id}/confirm")
def confirm_extracted_curriculum(
    curriculum_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN, RoleEnum.FACULTY]))
):
    """Faculty marks curriculum structure as verified and ready for agent analysis."""
    v = db.execute(select(CurriculumVersion).where(CurriculumVersion.id == curriculum_id)).scalar_one_or_none()
    if not v:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculum version not found")

    v.status = "STRUCTURE_CONFIRMED"
    db.commit()

    log_audit_event(
        db=db,
        action="CURRICULUM_STRUCTURE_CONFIRMED",
        resource_type="CURRICULUM_VERSION",
        resource_id=v.id,
        user_id=current_user.id
    )

    return {"message": "Curriculum structure confirmed by faculty. Ready to launch agent analysis.", "status": v.status}
