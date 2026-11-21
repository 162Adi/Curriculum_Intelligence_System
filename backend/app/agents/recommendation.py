"""
Agent 5: Recommendation Agent.
Synthesizes identified gaps into actionable, editable curriculum improvement proposals
(new subjects, updated topics, practical labs, electives, credit balance).
All recommendations start as DRAFT and require faculty approval.
"""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.intelligence import GapResult, Recommendation
from app.models.curriculum import Course


class RecommendationAgent:
    NAME = "Recommendation Agent"
    ROLE = "Curriculum Enhancement Strategist"

    SYSTEM_INSTRUCTIONS = """
    You are the Recommendation Agent.
    Your mission is to produce actionable, evidence-backed curriculum improvements:
    1. Propose concrete changes linked directly to identified gaps.
    2. Categorize proposals (New Subject, Practical Lab, Topic Update, Elective, Sequencing).
    3. State clearly: what should change, why it should change, supporting evidence, implementation effort, and expected student benefit.
    4. Treat all outputs as editable proposals. Never alter official curriculum without faculty sign-off.
    """

    RECOMMENDATION_TEMPLATES = [
        {
            "category": "PRACTICAL_LAB",
            "title": "Establish Cloud-Native & Containerization Laboratory",
            "description": "Introduce a 2-credit hands-on practical laboratory covering Docker containerization, Kubernetes orchestration, and cloud deployment pipelines on AWS/GCP.",
            "rationale": "High industry demand for cloud-native engineering across Bengaluru and Hyderabad tech markets with zero current lab coverage.",
            "effort": "MEDIUM",
            "benefit": "Enables students to deploy microservices and manage production-grade cloud environments.",
            "semester": 6
        },
        {
            "category": "NEW_SUBJECT",
            "title": "Introduce Modern Generative AI & Agentic Systems Elective",
            "description": "Create a 3-credit professional elective on LLMs, Retrieval-Augmented Generation (RAG), vector databases (pgvector), and LangGraph agent architectures.",
            "rationale": "Direct alignment with ACM CS2023 Sec 4.4 (Applied AI & LLMs) and high market demand for AI engineering.",
            "effort": "MEDIUM",
            "benefit": "Prepares graduates for modern AI Engineering and enterprise intelligent automation roles.",
            "semester": 7
        },
        {
            "category": "UPDATE_SUBJECT",
            "title": "Modernize Database Management Systems with Vector & Distributed Storage",
            "description": "Revise Unit 5 of DBMS (CS201) to include NoSQL document stores, vector embeddings with cosine similarity, and distributed database sharding.",
            "rationale": "Existing syllabus focuses solely on relational algebra and 1NF-BCNF normalization, omitting modern data architectures required by industry.",
            "effort": "LOW",
            "benefit": "Bridges gap between traditional SQL theory and modern distributed AI data stores.",
            "semester": 3
        },
        {
            "category": "PRACTICAL_LAB",
            "title": "Integrate DevOps, CI/CD, and Automated Testing Workflows",
            "description": "Incorporate automated GitHub Actions / GitLab CI pipelines, unit testing frameworks (pytest/Jest), and SonarQube quality gates into Software Engineering (CS302).",
            "rationale": "Fulfills ACM CS2023 Sec 7.5 (DevOps & CI/CD) and employer requirements for automated testing competence.",
            "effort": "LOW",
            "benefit": "Instills industrial software development lifecycle practices and automated deployment discipline.",
            "semester": 5
        },
        {
            "category": "COURSE_OUTCOME",
            "title": "Update Course Outcomes for AI & Machine Learning to Bloom Level 5 (Evaluate)",
            "description": "Revise CO2 from 'Train supervised models' to 'Design, evaluate, and fine-tune machine learning architectures and retrieval pipelines for domain problems'.",
            "rationale": "Elevates learning taxonomy from basic comprehension to critical evaluation and architectural design.",
            "effort": "LOW",
            "benefit": "Direct alignment with Outcome-Based Education (OBE) and NBA/ABET accreditation standards.",
            "semester": 7
        }
    ]

    @classmethod
    def execute(cls, db: Session, curriculum_version_id: str, gaps_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate editable recommendation drafts linked to identified gaps."""
        # Clean existing recommendations for this version
        existing_recs = db.execute(
            select(Recommendation).where(Recommendation.curriculum_version_id == curriculum_version_id)
        ).scalars().all()
        for r in existing_recs:
            db.delete(r)
        db.flush()

        gaps = db.execute(
            select(GapResult).where(GapResult.curriculum_version_id == curriculum_version_id).order_by(GapResult.gap_score.desc())
        ).scalars().all()

        recommendations_list = []
        rec_counter = 1

        for idx, tmpl in enumerate(cls.RECOMMENDATION_TEMPLATES):
            matching_gap = gaps[idx] if idx < len(gaps) else (gaps[0] if gaps else None)
            rec_id = f"REC-{rec_counter:03d}"
            rec_counter += 1

            db_rec = Recommendation(
                curriculum_version_id=curriculum_version_id,
                gap_id=matching_gap.id if matching_gap else None,
                recommendation_id=rec_id,
                category=tmpl["category"],
                title=tmpl["title"],
                description=tmpl["description"],
                affected_course_id=matching_gap.affected_course_id if matching_gap else None,
                affected_semester=tmpl["semester"],
                proposed_content={"outline": tmpl["description"], "suggested_hours": 30},
                rationale=tmpl["rationale"],
                industry_evidence=matching_gap.supporting_evidence if matching_gap else "Indian technology employer hiring trends (Bengaluru/Hyderabad).",
                academic_reference=matching_gap.related_benchmark_ref if matching_gap else "ACM CS2023 Guidelines",
                estimated_effort=tmpl["effort"],
                expected_benefit=tmpl["benefit"],
                priority="HIGH" if idx < 3 else "MEDIUM",
                status="DRAFT"  # All recommendations start as DRAFT
            )
            db.add(db_rec)
            recommendations_list.append({
                "id": db_rec.id,
                "recommendation_id": rec_id,
                "category": tmpl["category"],
                "title": tmpl["title"],
                "description": tmpl["description"],
                "affected_semester": tmpl["semester"],
                "estimated_effort": tmpl["effort"],
                "expected_benefit": tmpl["benefit"],
                "priority": db_rec.priority,
                "status": "DRAFT",
                "linked_gap_id": matching_gap.gap_id if matching_gap else None,
                "linked_gap_title": matching_gap.title if matching_gap else None
            })

        db.commit()

        return {
            "agent_name": cls.NAME,
            "status": "COMPLETED",
            "total_recommendations": len(recommendations_list),
            "recommendations": recommendations_list,
            "summary": f"Generated {len(recommendations_list)} actionable curriculum recommendations. All proposals submitted as DRAFT for faculty review."
        }
