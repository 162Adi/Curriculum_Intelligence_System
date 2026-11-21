"""
Agent 4: Gap Analysis Agent.
Deterministic scoring service merging Curriculum Mapping, Industry Skills, and Academic Benchmarks.
Calculates: Gap Score = Importance * (1 - Coverage) with transparent score breakdowns.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.intelligence import GapResult
from app.models.curriculum import Course, CourseTopic


class GapAnalysisAgent:
    NAME = "Gap Analysis Agent"
    ROLE = "Curriculum Deficit & Alignment Evaluator"

    @classmethod
    def calculate_gap_metric(cls, importance: float, coverage: float) -> Dict[str, Any]:
        """Deterministic mathematical formula: Gap Score = Importance * (1.0 - Coverage)."""
        score = round(importance * (1.0 - coverage), 1)
        if score >= 70.0:
            severity = "CRITICAL"
        elif score >= 45.0:
            severity = "HIGH"
        elif score >= 25.0:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        return {"score": score, "severity": severity}

    SYSTEM_INSTRUCTIONS = """
    You are the Gap Analysis Agent.
    Your mission is to rigorously identify weaknesses and misalignments in the curriculum:
    1. Merge outputs from Curriculum Mapping, Industry Skills, and Academic Benchmarking.
    2. Compute mathematical gap scores using: Gap Score = Importance * (1 - Coverage).
    3. Categorize gaps into the 10 formal classifications.
    4. Attach supporting evidence, affected courses, semesters, and priority rankings.
    """

    @classmethod
    def execute(
        cls,
        db: Session,
        curriculum_version_id: str,
        mapping_data: Dict[str, Any],
        industry_data: Dict[str, Any],
        benchmark_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compute deterministic gap analysis with explicit score breakdowns."""
        # Clean existing gaps for this version
        existing_gaps = db.execute(
            select(GapResult).where(GapResult.curriculum_version_id == curriculum_version_id)
        ).scalars().all()
        for g in existing_gaps:
            db.delete(g)
        db.flush()

        gaps: List[Dict[str, Any]] = []
        courses = db.execute(
            select(Course).where(Course.curriculum_version_id == curriculum_version_id)
        ).scalars().all()

        curriculum_text_corpus = ""
        for c in courses:
            topics = db.execute(select(CourseTopic).where(CourseTopic.course_id == c.id)).scalars().all()
            t_names = " ".join(t.topic_name for t in topics)
            curriculum_text_corpus += f" {c.course_title} {t_names}".lower()

        # 1. Evaluate Industry Skills Gaps
        ranked_skills = industry_data.get("ranked_skills", [])
        gap_counter = 1

        for skill in ranked_skills:
            s_name = skill["skill_name"].lower()
            s_importance = skill.get("importance_score", 0.8)

            # Deterministic coverage calculation
            if s_name in curriculum_text_corpus:
                # Topic present: check if practical lab or theory
                coverage = 0.50 if "lab" in curriculum_text_corpus else 0.40
            else:
                # Partial token check
                tokens = s_name.split()
                overlap = sum(1 for t in tokens if len(t) > 2 and t in curriculum_text_corpus)
                coverage = (overlap / max(1, len(tokens))) * 0.30

            gap_score = round(s_importance * (1.0 - coverage), 3)

            # If gap score is notable (> 0.35)
            if gap_score > 0.35:
                # Determine category
                if coverage < 0.15:
                    cat = "MISSING_SKILL"
                    severity = "HIGH" if s_importance >= 0.85 else "MEDIUM"
                elif "lab" not in s_name and ("docker" in s_name or "cloud" in s_name or "react" in s_name):
                    cat = "PRACTICAL_GAP"
                    severity = "HIGH"
                else:
                    cat = "WEAK_COVERAGE"
                    severity = "MEDIUM"

                # Find closest semester or course
                affected_sem = 6 if "ai" in s_name or "cloud" in s_name or "generative" in s_name else 4
                affected_course = next((c for c in courses if any(w in c.course_title.lower() for w in s_name.split())), None)

                gap_id = f"GAP-{gap_counter:03d}"
                gap_counter += 1

                title = f"Curriculum Deficit in {skill['canonical_name']}"
                desc = (
                    f"Employer demand in Indian technology hubs shows high priority for {skill['canonical_name']} "
                    f"({skill.get('target_occupation', 'Software Engineer')}), but existing coverage is only {int(coverage*100)}%."
                )

                db_gap = GapResult(
                    curriculum_version_id=curriculum_version_id,
                    gap_id=gap_id,
                    title=title,
                    description=desc,
                    category=cat,
                    affected_semester=affected_sem,
                    affected_course_id=affected_course.id if affected_course else None,
                    related_skills=[skill["skill_name"]],
                    related_benchmark_ref="ACM CS2023 Sec 4.4 / IEEE-CS" if "ai" in s_name else "ACM CS2023 Sec 7.5",
                    importance_score=s_importance,
                    coverage_score=coverage,
                    gap_score=gap_score,
                    severity=severity,
                    priority_rank=gap_counter,
                    supporting_evidence=f"Industry snapshot ({industry_data.get('sample_size', 1000)} jobs): frequency={skill.get('frequency', 0)}, demand score={s_importance}.",
                    recommended_action=f"Introduce hands-on modules or practical laboratory exercises covering {skill['canonical_name']}."
                )
                db.add(db_gap)
                gaps.append({
                    "gap_id": gap_id,
                    "title": title,
                    "category": cat,
                    "severity": severity,
                    "importance_score": s_importance,
                    "coverage_score": coverage,
                    "gap_score": gap_score,
                    "affected_semester": affected_sem,
                    "affected_course": affected_course.course_title if affected_course else "New Elective / Lab Recommended",
                    "supporting_evidence": db_gap.supporting_evidence
                })

        # 2. Evaluate Academic Benchmark Missing Topics
        missing_bench = benchmark_data.get("missing_topics", [])
        for mb in missing_bench[:4]:
            gap_id = f"GAP-{gap_counter:03d}"
            gap_counter += 1
            gap_score = 0.72

            db_gap = GapResult(
                curriculum_version_id=curriculum_version_id,
                gap_id=gap_id,
                title=f"Academic Benchmark Gap: {mb['knowledge_unit']}",
                description=f"ACM CS2023 ({mb['tier']}) requires instruction in {mb['topic_name']} ({mb['section']}, Page {mb['page']}). Not present in current courses.",
                category="ACADEMIC_BENCHMARK",
                affected_semester=5,
                related_benchmark_ref=f"ACM CS2023 {mb['section']} p.{mb['page']}",
                importance_score=0.80,
                coverage_score=0.10,
                gap_score=gap_score,
                severity="HIGH" if "Core" in mb["tier"] else "MEDIUM",
                priority_rank=gap_counter,
                supporting_evidence=f"ACM CS2023 Reference Guideline: {mb['knowledge_area']} - {mb['knowledge_unit']} (Sec {mb['section']}, Page {mb['page']})",
                recommended_action=f"Incorporate knowledge unit '{mb['knowledge_unit']}' into the computer science core syllabus."
            )
            db.add(db_gap)
            gaps.append({
                "gap_id": gap_id,
                "title": db_gap.title,
                "category": "ACADEMIC_BENCHMARK",
                "severity": db_gap.severity,
                "importance_score": 0.80,
                "coverage_score": 0.10,
                "gap_score": gap_score,
                "affected_semester": 5,
                "affected_course": "Core Curriculum Syllabus",
                "supporting_evidence": db_gap.supporting_evidence
            })

        # Sort gaps by gap_score descending
        gaps.sort(key=lambda x: x["gap_score"], reverse=True)
        for idx, g in enumerate(gaps):
            g["priority_rank"] = idx + 1

        db.commit()

        high_count = sum(1 for g in gaps if g["severity"] == "HIGH")
        med_count = sum(1 for g in gaps if g["severity"] == "MEDIUM")

        return {
            "agent_name": cls.NAME,
            "status": "COMPLETED",
            "total_gaps_identified": len(gaps),
            "high_severity_gaps": high_count,
            "medium_severity_gaps": med_count,
            "gaps": gaps,
            "scoring_formula": "Gap Score = Importance * (1 - Coverage)",
            "summary": f"Identified {len(gaps)} curriculum gaps ({high_count} High, {med_count} Medium). Top gap: {gaps[0]['title'] if gaps else 'None'}."
        }
