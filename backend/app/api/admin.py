"""
Admin & System Maintenance API: Storage cleanup, raw upload management, and file purge.
Enables administrators to delete uploaded syllabus documents from disk once data is stored in the database,
and purge or manage generated report files.
"""

import os
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.session import get_db
from app.models.users import User, RoleEnum
from app.models.curriculum import CurriculumVersion, Course
from app.models.approvals import Report
from app.auth.rbac import require_role, log_audit_event
from app.reporting.report_generator import REPORT_OUTPUT_DIR

router = APIRouter(prefix="/admin", tags=["Admin & Storage Maintenance"])

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = str((PROJECT_ROOT / "data" / "uploads").resolve())
REPORTS_DIR = str(Path(REPORT_OUTPUT_DIR).resolve())

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


def format_file_size(size_bytes: int) -> str:
    """Format bytes into readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def is_safe_path(target_path: str) -> bool:
    """Ensure file path is strictly within project upload or report directory (prevents path traversal)."""
    try:
        resolved = str(Path(target_path).resolve())
        is_in_uploads = resolved.startswith(UPLOAD_DIR)
        is_in_reports = resolved.startswith(REPORTS_DIR)
        return is_in_uploads or is_in_reports
    except Exception:
        return False


@router.get("/files")
def list_managed_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """List all stored upload documents and generated reports with disk and DB status."""
    files_list = []

    # 1. Inspect Uploaded Syllabus Documents
    curr_versions = db.execute(select(CurriculumVersion)).scalars().all()
    upload_path_map = {}
    for cv in curr_versions:
        if cv.file_path:
            norm = str(Path(cv.file_path).resolve()) if os.path.exists(cv.file_path) else cv.file_path
            upload_path_map[norm] = cv
            upload_path_map[os.path.basename(norm)] = cv

    if os.path.exists(UPLOAD_DIR):
        for fname in os.listdir(UPLOAD_DIR):
            fpath = os.path.join(UPLOAD_DIR, fname)
            if os.path.isfile(fpath):
                norm_fpath = str(Path(fpath).resolve())
                stat = os.stat(fpath)
                matched_cv = upload_path_map.get(norm_fpath) or upload_path_map.get(fname)
                
                # Check if curriculum data is in DB
                has_db_data = False
                associated_title = "Uploaded Syllabus Document"
                if matched_cv:
                    has_db_data = bool(matched_cv.total_courses and matched_cv.total_courses > 0)
                    prog_name = matched_cv.programme.name if matched_cv.programme else "Academic Programme"
                    associated_title = f"{prog_name} ({matched_cv.version_tag})"

                files_list.append({
                    "id": f"upload_{fname}",
                    "file_name": fname,
                    "file_path": fpath,
                    "category": "UPLOAD",
                    "category_label": "Uploaded Syllabus",
                    "size_bytes": stat.st_size,
                    "size_formatted": format_file_size(stat.st_size),
                    "created_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "stored_in_db": has_db_data or (matched_cv is not None),
                    "associated_title": associated_title,
                    "curriculum_version_id": matched_cv.id if matched_cv else None
                })

    # 2. Inspect Generated Reports
    reports = db.execute(select(Report)).scalars().all()
    report_path_map = {}
    for r in reports:
        for p in [r.pdf_path, r.excel_path, r.pptx_path]:
            if p:
                norm_p = str(Path(p).resolve()) if os.path.exists(p) else p
                report_path_map[norm_p] = r
                report_path_map[os.path.basename(norm_p)] = r

    if os.path.exists(REPORTS_DIR):
        for fname in os.listdir(REPORTS_DIR):
            fpath = os.path.join(REPORTS_DIR, fname)
            if os.path.isfile(fpath):
                norm_fpath = str(Path(fpath).resolve())
                stat = os.stat(fpath)
                matched_rep = report_path_map.get(norm_fpath) or report_path_map.get(fname)

                files_list.append({
                    "id": f"report_{fname}",
                    "file_name": fname,
                    "file_path": fpath,
                    "category": "GENERATED_REPORT",
                    "category_label": "Generated Report",
                    "size_bytes": stat.st_size,
                    "size_formatted": format_file_size(stat.st_size),
                    "created_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "stored_in_db": (matched_rep is not None),
                    "associated_title": matched_rep.title if matched_rep else "Compiled Audit Report",
                    "report_id": matched_rep.id if matched_rep else None
                })

    # Sort newest first
    files_list.sort(key=lambda x: x["created_at"], reverse=True)
    return files_list


@router.delete("/files")
def delete_managed_file(
    file_path: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """Erase a single uploaded file or generated report from disk while preserving DB records."""
    if not is_safe_path(file_path):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Forbidden: Path must reside inside data/uploads or data/reports."
        )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found on disk: {os.path.basename(file_path)}"
        )

    basename = os.path.basename(file_path)
    norm_path = str(Path(file_path).resolve())

    # 1. If it was linked to CurriculumVersion, set file_path = None (keeping courses in DB)
    currs = db.execute(select(CurriculumVersion)).scalars().all()
    for cv in currs:
        if cv.file_path and (str(Path(cv.file_path).resolve()) == norm_path or cv.file_path == file_path or os.path.basename(cv.file_path) == basename):
            cv.file_path = None

    # 2. If it was linked to a Report, clear that path
    reports = db.execute(select(Report)).scalars().all()
    for r in reports:
        if r.pdf_path and (str(Path(r.pdf_path).resolve()) == norm_path or os.path.basename(r.pdf_path) == basename):
            r.pdf_path = None
        if r.excel_path and (str(Path(r.excel_path).resolve()) == norm_path or os.path.basename(r.excel_path) == basename):
            r.excel_path = None
        if r.pptx_path and (str(Path(r.pptx_path).resolve()) == norm_path or os.path.basename(r.pptx_path) == basename):
            r.pptx_path = None

    db.commit()

    # Remove file from disk
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file from disk: {str(e)}"
        )

    log_audit_event(
        db=db,
        action="ADMIN_FILE_ERASED",
        resource_type="STORAGE",
        resource_id=basename,
        user_id=current_user.id,
        details={"file_path": file_path, "file_name": basename}
    )

    return {
        "message": f"File '{basename}' successfully erased from disk. Database courses/records preserved.",
        "file_name": basename,
        "file_path": file_path
    }


@router.post("/files/purge")
def purge_managed_files(
    target: str = Query("uploads", regex="^(uploads|reports|all)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """Bulk purge uploaded files or generated reports from disk once data is stored in DB."""
    removed_count = 0
    total_bytes_freed = 0

    dirs_to_clean = []
    if target in ["uploads", "all"]:
        dirs_to_clean.append((UPLOAD_DIR, "UPLOAD"))
    if target in ["reports", "all"]:
        dirs_to_clean.append((REPORTS_DIR, "REPORT"))

    for dpath, cat in dirs_to_clean:
        if os.path.exists(dpath):
            for fname in os.listdir(dpath):
                fpath = os.path.join(dpath, fname)
                if os.path.isfile(fpath):
                    try:
                        sz = os.path.getsize(fpath)
                        os.remove(fpath)
                        removed_count += 1
                        total_bytes_freed += sz
                    except Exception as err:
                        print(f"Error removing {fpath}: {err}")

    # Clear references in DB
    if target in ["uploads", "all"]:
        currs = db.execute(select(CurriculumVersion)).scalars().all()
        for cv in currs:
            cv.file_path = None

    if target in ["reports", "all"]:
        reports = db.execute(select(Report)).scalars().all()
        for r in reports:
            r.pdf_path = None
            r.excel_path = None
            r.pptx_path = None

    db.commit()

    log_audit_event(
        db=db,
        action="ADMIN_BULK_PURGE",
        resource_type="STORAGE",
        resource_id=target,
        user_id=current_user.id,
        details={"target": target, "files_removed": removed_count, "bytes_freed": total_bytes_freed}
    )

    freed_mb = total_bytes_freed / (1024 * 1024)
    return {
        "message": f"Successfully purged {removed_count} files from disk ({freed_mb:.2f} MB freed). Database records preserved.",
        "target": target,
        "files_removed": removed_count,
        "bytes_freed": total_bytes_freed,
        "freed_formatted": format_file_size(total_bytes_freed)
    }


@router.delete("/curriculum/{curriculum_id}")
def delete_curriculum_version(
    curriculum_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """Admin completely erases a curriculum version, its disk file, and child records from DB."""
    cv = db.execute(select(CurriculumVersion).where(CurriculumVersion.id == curriculum_id)).scalar_one_or_none()
    if not cv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curriculum version not found")

    version_tag = cv.version_tag
    file_path = cv.file_path

    # Delete disk file if it exists
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass

    db.delete(cv)
    db.commit()

    log_audit_event(
        db=db,
        action="ADMIN_CURRICULUM_DELETED",
        resource_type="CURRICULUM_VERSION",
        resource_id=curriculum_id,
        user_id=current_user.id,
        details={"version_tag": version_tag}
    )

    return {
        "message": f"Curriculum version {version_tag} and all associated extracted data successfully erased.",
        "curriculum_id": curriculum_id
    }
