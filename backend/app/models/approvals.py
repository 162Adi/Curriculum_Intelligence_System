"""
Faculty approval and multi-format reporting models.
"""

import uuid
from typing import Optional, List, Any
from sqlalchemy import String, Integer, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class ApprovalRecord(Base):
    __tablename__ = "approval_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    recommendation_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("recommendations.id", ondelete="CASCADE"), nullable=True)
    curriculum_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculum_versions.id", ondelete="CASCADE"), nullable=False)
    reviewer_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # APPROVED, REJECTED, MODIFIED, REOPENED
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    previous_state: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    new_state: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)

    recommendation: Mapped[Optional["Recommendation"]] = relationship("Recommendation", back_populates="approval_records")
    reviewer: Mapped["User"] = relationship("User", lazy="selectin")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculum_versions.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="Curriculum Intelligence & Industry Alignment Report")
    report_type: Mapped[str] = mapped_column(String(50), default="FACULTY_APPROVED")  # EXECUTIVE, COMPREHENSIVE, FACULTY_APPROVED
    status: Mapped[str] = mapped_column(String(50), default="READY")  # GENERATING, READY, FINALIZED
    pdf_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    excel_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    pptx_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    summary_data: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    generated_by_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    curriculum_version: Mapped["CurriculumVersion"] = relationship("CurriculumVersion", back_populates="reports", lazy="selectin")
    generated_by: Mapped[Optional["User"]] = relationship("User", lazy="selectin")
    versions: Mapped[List["ReportVersion"]] = relationship("ReportVersion", back_populates="report", cascade="all, delete-orphan")


class ReportVersion(Base):
    __tablename__ = "report_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id: Mapped[str] = mapped_column(String(36), ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, default=1)
    changelog: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)

    report: Mapped["Report"] = relationship("Report", back_populates="versions")
