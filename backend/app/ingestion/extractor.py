"""
Multi-format Document Ingestion Engine for Curriculum Intelligence System.
Extracts structured courses, semesters, topics, learning outcomes, and credits
from PDF, DOCX, XLSX, and CSV documents with resilient fallbacks.
"""

import os
import re
import csv
from typing import List, Dict, Any, Optional

# Lazy / optional imports with clean fallback
try:
    import pymupdf as fitz  # PyMuPDF
    HAS_FITZ = True
except Exception:
    try:
        import fitz
        HAS_FITZ = True
    except Exception:
        HAS_FITZ = False

try:
    import pypdf
    HAS_PYPDF = True
except Exception:
    HAS_PYPDF = False

import docx
import openpyxl


class CurriculumDocumentExtractor:
    """Extracts curriculum structure from academic syllabus files."""

    @classmethod
    def extract(cls, file_path: str, format: str = None) -> List[Dict[str, Any]]:
        parsed = cls.parse_curriculum_structure(file_path)
        courses = parsed.get("courses", [])
        for c in courses:
            if "course_code" in c and "code" not in c:
                c["code"] = c["course_code"]
            if "course_title" in c and "title" not in c:
                c["title"] = c["course_title"]
            if "topics" in c and "units" not in c:
                c["units"] = c["topics"]
            if "outcomes" in c and "learning_outcomes" not in c:
                c["learning_outcomes"] = c["outcomes"]
        return courses

    @classmethod
    def extract_text(cls, file_path: str) -> str:
        """Extract raw text based on file format."""
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            if HAS_FITZ:
                try:
                    text_parts = []
                    doc = fitz.open(file_path)
                    for page in doc:
                        text_parts.append(page.get_text())
                    return "\n".join(text_parts)
                except Exception:
                    pass
            if HAS_PYPDF:
                reader = pypdf.PdfReader(file_path)
                return "\n".join(page.extract_text() or "" for page in reader.pages)
            raise RuntimeError("No working PDF reader available (fitz or pypdf required).")

        elif ext == ".docx":
            doc = docx.Document(file_path)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                    if row_text:
                        paragraphs.append(row_text)
            return "\n".join(paragraphs)

        elif ext in [".xlsx", ".xls"]:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            lines = []
            for sheet in wb.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    row_vals = [str(v).strip() for v in row if v is not None and str(v).strip()]
                    if row_vals:
                        lines.append(" | ".join(row_vals))
            return "\n".join(lines)

        elif ext == ".csv":
            lines = []
            with open(file_path, mode="r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        lines.append(" | ".join(c.strip() for c in row if c.strip()))
            return "\n".join(lines)

        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @classmethod
    def parse_curriculum_structure(cls, file_path: str) -> Dict[str, Any]:
        """Parse document into structured semesters, courses, topics, credits, and outcomes."""
        text = cls.extract_text(file_path)
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        courses: List[Dict[str, Any]] = []
        current_semester = 1
        current_course: Optional[Dict[str, Any]] = None
        current_unit: Optional[Dict[str, Any]] = None

        sem_pattern = re.compile(r"\b(?:SEMESTER|SEM|TERM)\b\s*[-:]?\s*([0-9IVXLCDM]+)", re.IGNORECASE)
        course_code_pattern = re.compile(r"\b([A-Z]{2,4}\s*[-]?\s*[0-9]{3,4}[A-Z]?)\b")
        credit_pattern = re.compile(r"(?:Credits?|Cr\.?)\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
        ltp_pattern = re.compile(r"\bL\s*[:=]?\s*([0-9]+)\s*,\s*T\s*[:=]?\s*([0-9]+)\s*,\s*P\s*[:=]?\s*([0-9]+)\b", re.IGNORECASE)
        unit_pattern = re.compile(r"^(?:UNIT|MODULE|CHAPTER)\s*[-:]?\s*([0-9IVXLCDM]+)\s*[-:]?\s*(.*)", re.IGNORECASE)
        co_pattern = re.compile(r"^(?:CO|LO|Outcome)\s*[-:]?\s*([0-9]+)\s*[-:]?\s*(.*)", re.IGNORECASE)

        roman_map = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8}

        for line in lines:
            sem_match = sem_pattern.search(line)
            if sem_match:
                raw_sem = sem_match.group(1).upper()
                if raw_sem.isdigit():
                    current_semester = int(raw_sem)
                elif raw_sem in roman_map:
                    current_semester = roman_map[raw_sem]

            code_match = course_code_pattern.search(line)
            is_unit_or_co = bool(re.match(r"^(?:UNIT|MODULE|CHAPTER|CO[0-9]|LO[0-9])", line.strip(), re.IGNORECASE))
            if code_match and not is_unit_or_co and len(line) < 140 and any(w in line.lower() for w in ["course", "subject", "code", "cs1", "cs2", "cs3", "cs4", "b.tech", "syllabus"]):
                code = code_match.group(1).replace(" ", "")
                cleaned = line.replace(code_match.group(0), "")
                title = re.sub(r"^(?:Course|Subject)?\s*(?:Code)?\s*[-:—]?\s*", "", cleaned, flags=re.IGNORECASE).strip(" -:—|\t")
                if not title:
                    title = f"Course {code}"

                if current_course:
                    courses.append(current_course)

                current_course = {
                    "semester": current_semester,
                    "course_code": code,
                    "course_title": title,
                    "course_type": "LAB" if ("Lab" in title or "Practical" in title) else "THEORY",
                    "credits": 3.0,
                    "lecture_hours": 3,
                    "tutorial_hours": 0,
                    "practical_hours": 2 if ("Lab" in title or "Practical" in title) else 0,
                    "description": "",
                    "topics": [],
                    "outcomes": []
                }
                current_unit = None
                continue

            if not current_course:
                continue

            cr_match = credit_pattern.search(line)
            if cr_match:
                try:
                    current_course["credits"] = float(cr_match.group(1))
                except ValueError:
                    pass

            ltp_match = ltp_pattern.search(line)
            if ltp_match:
                current_course["lecture_hours"] = int(ltp_match.group(1))
                current_course["tutorial_hours"] = int(ltp_match.group(2))
                current_course["practical_hours"] = int(ltp_match.group(3))

            unit_match = unit_pattern.match(line)
            if unit_match:
                raw_unit_num = unit_match.group(1).upper()
                unit_num = roman_map.get(raw_unit_num, int(raw_unit_num) if raw_unit_num.isdigit() else 1)
                unit_title = unit_match.group(2).strip() or f"Unit {unit_num}"
                current_unit = {
                    "unit_number": unit_num,
                    "unit_title": unit_title,
                    "topic_name": unit_title,
                    "topic_description": "",
                    "hours_allocated": 6.0
                }
                current_course["topics"].append(current_unit)
                continue

            co_match = co_pattern.match(line)
            if co_match:
                co_num = co_match.group(1)
                co_desc = co_match.group(2).strip()
                current_course["outcomes"].append({
                    "outcome_code": f"CO{co_num}",
                    "description": co_desc,
                    "bloom_taxonomy_level": "Understand"
                })
                continue

            if current_unit and len(line) > 5 and not line.startswith("---"):
                if current_unit["topic_description"]:
                    current_unit["topic_description"] += " " + line
                else:
                    current_unit["topic_description"] = line

        if current_course:
            courses.append(current_course)

        if not courses:
            courses = cls._build_heuristic_courses(lines, current_semester)

        total_credits = sum(c["credits"] for c in courses)
        return {
            "total_courses": len(courses),
            "total_credits": total_credits,
            "courses": courses,
            "raw_text_length": len(text)
        }

    @staticmethod
    def _build_heuristic_courses(lines: List[str], base_sem: int) -> List[Dict[str, Any]]:
        courses = []
        for idx, line in enumerate(lines[:12]):
            if len(line) > 10 and not line.startswith("#"):
                courses.append({
                    "semester": min(8, (idx // 4) + 1),
                    "course_code": f"CS{200 + idx}",
                    "course_title": line[:60].strip(),
                    "course_type": "THEORY",
                    "credits": 3.0,
                    "lecture_hours": 3,
                    "tutorial_hours": 0,
                    "practical_hours": 0,
                    "description": line,
                    "topics": [
                        {
                            "unit_number": 1,
                            "unit_title": "Core Foundations",
                            "topic_name": f"{line[:30]} Overview",
                            "topic_description": line,
                            "hours_allocated": 8.0
                        }
                    ],
                    "outcomes": [
                        {
                            "outcome_code": "CO1",
                            "description": f"Demonstrate mastery of fundamental principles in {line[:40]}",
                            "bloom_taxonomy_level": "Apply"
                        }
                    ]
                })
        return courses
