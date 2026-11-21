"""
Integration tests for ReportLab PDF, openpyxl Excel, and python-pptx PowerPoint exports.
"""
import os
import pytest
from app.reporting.report_generator import ReportGenerator


def test_pdf_report_generation(db_session, sample_curriculum):
    pdf_bytes = ReportGenerator.generate_pdf(sample_curriculum.id, db_session)
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 1000
    # PDF starts with %PDF magic number
    assert pdf_bytes.startswith(b"%PDF")


def test_excel_report_generation(db_session, sample_curriculum):
    excel_bytes = ReportGenerator.generate_excel(sample_curriculum.id, db_session)
    assert excel_bytes is not None
    assert len(excel_bytes) > 1000
    # XLSX files are ZIP archives starting with PK
    assert excel_bytes.startswith(b"PK")


def test_pptx_report_generation(db_session, sample_curriculum):
    pptx_bytes = ReportGenerator.generate_pptx(sample_curriculum.id, db_session)
    assert pptx_bytes is not None
    assert len(pptx_bytes) > 1000
    # PPTX files are ZIP archives starting with PK
    assert pptx_bytes.startswith(b"PK")
