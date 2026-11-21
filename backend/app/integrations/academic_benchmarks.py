"""
Academic Standards & Reference Corpus Provider for ACM CS2023, IEEE-CS, and AAAI AI.
Delivers versioned, page-cited curriculum benchmark requirements.
"""

import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.intelligence import AcademicStandard, BenchmarkDocument


class AcademicBenchmarkService:
    """Manages official curriculum guidelines from ACM, IEEE-CS, and AAAI."""

    @staticmethod
    def get_standard_guidelines(db: Session, standard_code: str = "ACM_CS2023") -> List[Dict[str, Any]]:
        """Retrieve knowledge units and topics for an official academic standard."""
        std = db.execute(select(AcademicStandard).where(AcademicStandard.code == standard_code)).scalar_one_or_none()
        if not std:
            return []

        docs = db.execute(
            select(BenchmarkDocument)
            .where(BenchmarkDocument.standard_id == std.id)
            .order_by(BenchmarkDocument.knowledge_area, BenchmarkDocument.tier)
        ).scalars().all()

        return [
            {
                "id": d.id,
                "standard_code": std.code,
                "standard_title": std.title,
                "version": std.version,
                "publication_year": std.publication_year,
                "knowledge_area": d.knowledge_area,
                "knowledge_unit": d.knowledge_unit,
                "topic_name": d.topic_name,
                "tier": d.tier,
                "section_reference": d.section_reference,
                "page_number": d.page_number,
                "content_text": d.content_text
            }
            for d in docs
        ]

    @staticmethod
    def calculate_topic_alignment(curriculum_topics: List[str], benchmark_topic: str) -> Dict[str, Any]:
        """Transparent, deterministic string and semantic matching between curriculum and guideline."""
        clean_bench = benchmark_topic.lower()
        bench_tokens = set(re.findall(r"\w+", clean_bench))

        best_score = 0.0
        best_match = ""

        for ct in curriculum_topics:
            clean_ct = ct.lower()
            ct_tokens = set(re.findall(r"\w+", clean_ct))

            # Jaccard Token Overlap
            if bench_tokens and ct_tokens:
                intersection = bench_tokens.intersection(ct_tokens)
                jaccard = len(intersection) / len(bench_tokens.union(ct_tokens))
                containment = len(intersection) / len(bench_tokens)
                score = 0.4 * jaccard + 0.6 * containment
                if score > best_score:
                    best_score = score
                    best_match = ct

        if best_score >= 0.70:
            status = "COVERED"
        elif best_score >= 0.35:
            status = "PARTIAL"
        else:
            status = "MISSING"

        return {
            "status": status,
            "alignment_score": round(best_score, 3),
            "matched_curriculum_topic": best_match if best_score >= 0.35 else None
        }
