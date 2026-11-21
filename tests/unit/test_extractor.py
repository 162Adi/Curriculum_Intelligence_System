"""
Unit tests for curriculum document extraction (CSV, DOCX, fallback parsing).
"""
import os
import pytest
from app.ingestion.extractor import CurriculumDocumentExtractor


def test_csv_extraction():
    csv_path = os.path.join("data", "sample_curriculum", "Sample_Curriculum_Courses.csv")
    if not os.path.exists(csv_path):
        pytest.skip("Sample CSV not present")

    courses = CurriculumDocumentExtractor.extract(csv_path, "csv")
    assert len(courses) >= 4
    course_codes = [c["code"] for c in courses]
    assert "CS101" in course_codes
    assert "CS102" in course_codes
    assert "CS201" in course_codes


def test_docx_extraction():
    docx_path = os.path.join("data", "sample_curriculum", "Sample_BTech_CSE_Curriculum.docx")
    if not os.path.exists(docx_path):
        pytest.skip("Sample DOCX not present")

    courses = CurriculumDocumentExtractor.extract(docx_path, "docx")
    assert len(courses) >= 4
    for c in courses:
        assert "code" in c
        assert "title" in c
        assert len(c["units"]) >= 1
        assert len(c["learning_outcomes"]) >= 1


def test_pdf_pymupdf_extraction():
    pdf_path = os.path.join("data", "sample_curriculum", "Sample_BTech_CSE_Curriculum.pdf")
    assert os.path.exists(pdf_path), "Sample_BTech_CSE_Curriculum.pdf must exist"

    parsed = CurriculumDocumentExtractor.parse_curriculum_structure(pdf_path)
    assert parsed["total_courses"] == 8
    assert parsed["total_credits"] == 28.0

    courses = CurriculumDocumentExtractor.extract(pdf_path, "pdf")
    assert len(courses) == 8
    codes = [c["code"] for c in courses]
    assert codes == ["CS101", "CS102", "CS201", "CS202", "CS301", "CS302", "CS303", "CS304"]
    for c in courses:
        assert len(c["units"]) == 5
        assert len(c["learning_outcomes"]) == 2
