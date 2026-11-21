"""
Intelligence models: Industry jobs, skills, snapshots, academic standards, gaps, recommendations, and skill mappings.
"""

import uuid
from datetime import datetime
from typing import Optional, List, Any
from sqlalchemy import String, Integer, Float, ForeignKey, JSON, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class IndustrySnapshot(Base):
    __tablename__ = "industry_snapshots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider: Mapped[str] = mapped_column(String(50), nullable=False)  # Adzuna, Curated_Snapshot
    location: Mapped[str] = mapped_column(String(100), default="India Tech Hubs")
    snapshot_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    total_jobs_analyzed: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    metadata_json: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)

    # Relationships
    jobs: Mapped[List["IndustryJob"]] = relationship("IndustryJob", back_populates="snapshot", cascade="all, delete-orphan")
    skills: Mapped[List["IndustrySkill"]] = relationship("IndustrySkill", back_populates="snapshot", cascade="all, delete-orphan", lazy="selectin")


class IndustryJob(Base):
    __tablename__ = "industry_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    snapshot_id: Mapped[str] = mapped_column(String(36), ForeignKey("industry_snapshots.id", ondelete="CASCADE"), nullable=False)
    job_id: Mapped[str] = mapped_column(String(100), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[str] = mapped_column(String(100), default="Bengaluru, India")
    salary_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    salary_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    snapshot: Mapped["IndustrySnapshot"] = relationship("IndustrySnapshot", back_populates="jobs")


class IndustrySkill(Base):
    __tablename__ = "industry_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    snapshot_id: Mapped[str] = mapped_column(String(36), ForeignKey("industry_snapshots.id", ondelete="CASCADE"), nullable=False)
    skill_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="Technical")  # Technical, Tool, Soft
    frequency: Mapped[int] = mapped_column(Integer, default=1)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)  # 0.0 to 1.0
    esco_uri: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    snapshot: Mapped["IndustrySnapshot"] = relationship("IndustrySnapshot", back_populates="skills")


class AcademicStandard(Base):
    __tablename__ = "academic_standards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)  # ACM_CS2023, IEEE_CS, AAAI_AI
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), default="2023")
    publication_year: Mapped[int] = mapped_column(Integer, default=2023)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    documents: Mapped[List["BenchmarkDocument"]] = relationship("BenchmarkDocument", back_populates="standard", cascade="all, delete-orphan")


class BenchmarkDocument(Base):
    __tablename__ = "benchmark_documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    standard_id: Mapped[str] = mapped_column(String(36), ForeignKey("academic_standards.id", ondelete="CASCADE"), nullable=False)
    knowledge_area: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # e.g. "AI - Artificial Intelligence"
    knowledge_unit: Mapped[str] = mapped_column(String(100), index=True, nullable=False)  # e.g. "AI-Fundamental Concepts"
    topic_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tier: Mapped[str] = mapped_column(String(50), default="Tier 1 Core")  # Tier 1 Core, Tier 2 Core, Elective
    section_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    standard: Mapped["AcademicStandard"] = relationship("AcademicStandard", back_populates="documents", lazy="selectin")


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculum_versions.id", ondelete="CASCADE"), nullable=False)
    standard_id: Mapped[str] = mapped_column(String(36), ForeignKey("academic_standards.id", ondelete="CASCADE"), nullable=False)
    coverage_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0.0 - 1.0
    total_benchmark_topics: Mapped[int] = mapped_column(Integer, default=0)
    covered_topics_count: Mapped[int] = mapped_column(Integer, default=0)
    partial_topics_count: Mapped[int] = mapped_column(Integer, default=0)
    missing_topics_count: Mapped[int] = mapped_column(Integer, default=0)
    details: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)

    curriculum_version: Mapped["CurriculumVersion"] = relationship("CurriculumVersion", back_populates="benchmark_results")
    standard: Mapped["AcademicStandard"] = relationship("AcademicStandard", lazy="selectin")


class SkillMapping(Base):
    __tablename__ = "skill_mappings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculum_versions.id", ondelete="CASCADE"), nullable=False)
    course_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=True)
    skill_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    source: Mapped[str] = mapped_column(String(50), default="INDUSTRY")  # INDUSTRY, BENCHMARK
    match_type: Mapped[str] = mapped_column(String(50), default="DIRECT")  # DIRECT, SEMANTIC, PARTIAL, NONE
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    evidence_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class GapResult(Base):
    __tablename__ = "gap_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculum_versions.id", ondelete="CASCADE"), nullable=False)
    gap_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # GAP-001
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # MISSING_SKILL, WEAK_COVERAGE, etc.
    affected_semester: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    affected_course_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    related_skills: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    related_benchmark_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    importance_score: Mapped[float] = mapped_column(Float, default=0.8)
    coverage_score: Mapped[float] = mapped_column(Float, default=0.2)
    gap_score: Mapped[float] = mapped_column(Float, default=0.64)  # Formula: Importance * (1 - Coverage)
    severity: Mapped[str] = mapped_column(String(20), default="HIGH")  # HIGH, MEDIUM, LOW
    priority_rank: Mapped[int] = mapped_column(Integer, default=1)
    supporting_evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    curriculum_version: Mapped["CurriculumVersion"] = relationship("CurriculumVersion", back_populates="gaps")
    course: Mapped[Optional["Course"]] = relationship("Course", lazy="selectin")
    recommendations: Mapped[List["Recommendation"]] = relationship("Recommendation", back_populates="gap")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculum_versions.id", ondelete="CASCADE"), nullable=False)
    gap_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("gap_results.id", ondelete="SET NULL"), nullable=True)
    recommendation_id: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # REC-001
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # NEW_SUBJECT, NEW_TOPIC, PRACTICAL_LAB, etc.
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    affected_course_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    affected_semester: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    proposed_content: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    industry_evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    academic_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    estimated_effort: Mapped[str] = mapped_column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH
    expected_benefit: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="HIGH")  # HIGH, MEDIUM, LOW
    status: Mapped[str] = mapped_column(String(50), default="DRAFT")  # DRAFT, SUBMITTED, UNDER_REVIEW, APPROVED, REJECTED, NEEDS_REVISION
    faculty_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    curriculum_version: Mapped["CurriculumVersion"] = relationship("CurriculumVersion", back_populates="recommendations")
    gap: Mapped[Optional["GapResult"]] = relationship("GapResult", back_populates="recommendations", lazy="selectin")
    course: Mapped[Optional["Course"]] = relationship("Course", lazy="selectin")
    approval_records: Mapped[List["ApprovalRecord"]] = relationship("ApprovalRecord", back_populates="recommendation", cascade="all, delete-orphan")
