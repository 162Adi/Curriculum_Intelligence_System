"""
Agent 1: Curriculum Mapping Agent.
Analyzes the existing curriculum, maps courses to knowledge areas,
and detects repeated or overlapping topics across semesters.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.curriculum import CurriculumVersion, Course, CourseTopic, CourseOutcome


class CurriculumMappingAgent:
    NAME = "Curriculum Mapping Agent"
    ROLE = "Curriculum Structure Analyzer"

    SYSTEM_INSTRUCTIONS = """
    You are the Curriculum Mapping Agent of the Curriculum Intelligence System.
    Analyze the uploaded academic curriculum:
    1. Extract semester-wise course distribution, credits, theory vs practical balance.
    2. Map courses into computing knowledge areas (Algorithms, Systems, AI, Software Engineering, Networks, Security, Web).
    3. Detect overlapping or redundant topics taught across multiple subjects.
    4. Compile comprehensive structural mapping evidence.
    """

    KNOWLEDGE_AREA_KEYWORDS = {
        "Foundations & Algorithms": ["programming", "c", "c++", "data structures", "algorithms", "discrete mathematics"],
        "Systems & Architecture": ["operating systems", "computer organization", "architecture", "digital logic", "microprocessors"],
        "Data Management": ["database", "dbms", "sql", "data warehouse", "nosql"],
        "Networking & Distributed": ["computer networks", "tcp/ip", "distributed systems", "cloud computing"],
        "Software Engineering": ["software engineering", "agile", "uml", "design patterns", "object-oriented", "testing"],
        "Artificial Intelligence": ["artificial intelligence", "machine learning", "deep learning", "neural networks", "nlp"],
        "Web & Full Stack": ["web technologies", "javascript", "react", "html", "css", "internet programming"]
    }

    @classmethod
    def execute(cls, db: Session, curriculum_version_id: str) -> Dict[str, Any]:
        """Execute curriculum mapping analysis on specified curriculum version."""
        courses = db.execute(
            select(Course).where(Course.curriculum_version_id == curriculum_version_id).order_by(Course.semester)
        ).scalars().all()

        mapped_courses = []
        all_topics: List[Dict[str, Any]] = []
        area_distribution = {k: 0 for k in cls.KNOWLEDGE_AREA_KEYWORDS}

        total_theory_hours = 0
        total_lab_hours = 0
        total_credits = 0.0

        for c in courses:
            topics = db.execute(select(CourseTopic).where(CourseTopic.course_id == c.id)).scalars().all()
            outcomes = db.execute(select(CourseOutcome).where(CourseOutcome.course_id == c.id)).scalars().all()

            total_theory_hours += c.lecture_hours
            total_lab_hours += c.practical_hours
            total_credits += c.credits

            # Determine dominant knowledge area
            title_lower = c.course_title.lower()
            assigned_area = "General Computing"
            for area, keywords in cls.KNOWLEDGE_AREA_KEYWORDS.items():
                if any(kw in title_lower for kw in keywords):
                    assigned_area = area
                    area_distribution[area] += 1
                    break

            course_topics_list = []
            for t in topics:
                topic_record = {
                    "course_code": c.course_code,
                    "course_title": c.course_title,
                    "semester": c.semester,
                    "topic_name": t.topic_name,
                    "description": t.topic_description or ""
                }
                course_topics_list.append(t.topic_name)
                all_topics.append(topic_record)

            mapped_courses.append({
                "course_id": c.id,
                "semester": c.semester,
                "course_code": c.course_code,
                "course_title": c.course_title,
                "course_type": c.course_type,
                "credits": c.credits,
                "lecture_hours": c.lecture_hours,
                "practical_hours": c.practical_hours,
                "knowledge_area": assigned_area,
                "topic_count": len(topics),
                "topics": course_topics_list,
                "outcome_count": len(outcomes)
            })

        # Detect redundant or overlapping topics across courses
        redundancies = []
        seen_topics = {}
        for item in all_topics:
            t_clean = item["topic_name"].lower().strip()
            # Simple keyword overlap check
            for prev_key, prev_item in seen_topics.items():
                if (t_clean in prev_key or prev_key in t_clean) and len(t_clean) > 8 and item["course_code"] != prev_item["course_code"]:
                    redundancies.append({
                        "topic": item["topic_name"],
                        "course_a": f"{prev_item['course_code']} ({prev_item['course_title']}) - Sem {prev_item['semester']}",
                        "course_b": f"{item['course_code']} ({item['course_title']}) - Sem {item['semester']}",
                        "overlap_type": "Potential Redundant Teaching / Topic Duplication"
                    })
            seen_topics[t_clean] = item

        return {
            "agent_name": cls.NAME,
            "status": "COMPLETED",
            "total_courses": len(courses),
            "total_credits": total_credits,
            "theory_practical_ratio": round(total_theory_hours / max(1, total_lab_hours), 2),
            "area_distribution": area_distribution,
            "mapped_courses": mapped_courses,
            "detected_redundancies": redundancies[:5],
            "summary": f"Analyzed {len(courses)} courses across {max([c['semester'] for c in mapped_courses], default=1)} semesters. Total credits: {total_credits}."
        }
