"""
Curriculum structure models: Department, Programme, CurriculumVersion, Course, Topic, Outcome.
"""

import uuid
from typing import Optional, List, Any
from sqlalchemy import String, Integer, Float, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    programmes: Mapped[List["Programme"]] = relationship("Programme", back_populates="department", cascade="all, delete-orphan")
    users: Mapped[List["User"]] = relationship("User", back_populates="department")


class Programme(Base):
    __tablename__ = "programmes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    department_id: Mapped[str] = mapped_column(String(36), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    degree_type: Mapped[str] = mapped_column(String(50), default="B.Tech")  # B.Tech, M.Tech, Ph.D.
    total_semesters: Mapped[int] = mapped_column(Integer, default=8)
    total_credits: Mapped[int] = mapped_column(Integer, default=160)

    # Relationships
    department: Mapped["Department"] = relationship("Department", back_populates="programmes", lazy="selectin")
    curriculum_versions: Mapped[List["CurriculumVersion"]] = relationship("CurriculumVersion", back_populates="programme", cascade="all, delete-orphan")


class CurriculumVersion(Base):
    __tablename__ = "curriculum_versions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    programme_id: Mapped[str] = mapped_column(String(36), ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False)
    version_tag: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g. "2024-v1.0"
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)  # e.g. "2024-2028"
    status: Mapped[str] = mapped_column(String(50), default="DRAFT")  # DRAFT, INGESTED, ANALYZED, APPROVED, ARCHIVED
    file_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    extracted_data: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    total_courses: Mapped[int] = mapped_column(Integer, default=0)
    total_credits: Mapped[float] = mapped_column(Float, default=0.0)

    # Relationships
    programme: Mapped["Programme"] = relationship("Programme", back_populates="curriculum_versions", lazy="selectin")
    courses: Mapped[List["Course"]] = relationship("Course", back_populates="curriculum_version", cascade="all, delete-orphan", lazy="selectin")
    gaps: Mapped[List["GapResult"]] = relationship("GapResult", back_populates="curriculum_version", cascade="all, delete-orphan")
    recommendations: Mapped[List["Recommendation"]] = relationship("Recommendation", back_populates="curriculum_version", cascade="all, delete-orphan")
    benchmark_results: Mapped[List["BenchmarkResult"]] = relationship("BenchmarkResult", back_populates="curriculum_version", cascade="all, delete-orphan")
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="curriculum_version", cascade="all, delete-orphan")


Curriculum = CurriculumVersion


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    curriculum_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("curriculum_versions.id", ondelete="CASCADE"), nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    course_code: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    course_title: Mapped[str] = mapped_column(String(255), nullable=False)
    course_type: Mapped[str] = mapped_column(String(50), default="THEORY")  # THEORY, LAB, INTEGRATED, ELECTIVE
    credits: Mapped[float] = mapped_column(Float, default=3.0)
    lecture_hours: Mapped[int] = mapped_column(Integer, default=3)
    tutorial_hours: Mapped[int] = mapped_column(Integer, default=0)
    practical_hours: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    curriculum_version: Mapped["CurriculumVersion"] = relationship("CurriculumVersion", back_populates="courses")
    topics: Mapped[List["CourseTopic"]] = relationship("CourseTopic", back_populates="course", cascade="all, delete-orphan", lazy="selectin")
    outcomes: Mapped[List["CourseOutcome"]] = relationship("CourseOutcome", back_populates="course", cascade="all, delete-orphan", lazy="selectin")


class CourseTopic(Base):
    __tablename__ = "course_topics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    unit_number: Mapped[int] = mapped_column(Integer, default=1)
    unit_title: Mapped[str] = mapped_column(String(255), nullable=False)
    topic_name: Mapped[str] = mapped_column(String(255), nullable=False)
    topic_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hours_allocated: Mapped[Optional[float]] = mapped_column(Float, default=2.0)

    course: Mapped["Course"] = relationship("Course", back_populates="topics")


class CourseOutcome(Base):
    __tablename__ = "course_outcomes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id: Mapped[str] = mapped_column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    outcome_code: Mapped[str] = mapped_column(String(20), nullable=False)  # e.g. CO1, CO2
    description: Mapped[str] = mapped_column(Text, nullable=False)
    bloom_taxonomy_level: Mapped[Optional[str]] = mapped_column(String(50), default="Understand")  # Remember, Understand, Apply, Analyze, Evaluate, Create

    course: Mapped["Course"] = relationship("Course", back_populates="outcomes")
