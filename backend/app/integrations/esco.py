"""
ESCO (European Skills, Competences, Qualifications and Occupations) taxonomy adapter.
Provides semantic skill classification, category normalization, and occupation mappings.
"""

from typing import Dict, Any, List, Optional
import re


class ESCOTaxonomyAdapter:
    """Normalizes raw curriculum and industry skills into standardized taxonomy buckets."""

    SKILL_TAXONOMY_MAP = {
        # Programming & Languages
        "python": {"canonical": "Python", "category": "Programming Languages", "esco_code": "S1.1.1", "occupation": "Software Developer"},
        "c": {"canonical": "C / C++", "category": "Programming Languages", "esco_code": "S1.1.2", "occupation": "Systems Software Developer"},
        "c++": {"canonical": "C / C++", "category": "Programming Languages", "esco_code": "S1.1.2", "occupation": "Embedded Systems Engineer"},
        "java": {"canonical": "Java", "category": "Programming Languages", "esco_code": "S1.1.3", "occupation": "Backend Enterprise Developer"},
        "javascript": {"canonical": "JavaScript / TypeScript", "category": "Web Technologies", "esco_code": "S1.2.1", "occupation": "Full Stack Developer"},
        "typescript": {"canonical": "TypeScript", "category": "Web Technologies", "esco_code": "S1.2.2", "occupation": "Frontend Engineer"},

        # AI & Machine Learning
        "machine learning": {"canonical": "Machine Learning", "category": "Artificial Intelligence", "esco_code": "S2.1.1", "occupation": "AI/ML Engineer"},
        "deep learning": {"canonical": "Deep Learning & Neural Networks", "category": "Artificial Intelligence", "esco_code": "S2.1.2", "occupation": "Deep Learning Researcher"},
        "generative ai": {"canonical": "Generative AI & LLMs", "category": "Artificial Intelligence", "esco_code": "S2.1.3", "occupation": "AI Solutions Architect"},
        "llm": {"canonical": "Large Language Models & Prompt Engineering", "category": "Artificial Intelligence", "esco_code": "S2.1.4", "occupation": "LLM Application Developer"},
        "rag": {"canonical": "Retrieval-Augmented Generation & Vector Search", "category": "Artificial Intelligence", "esco_code": "S2.1.5", "occupation": "AI Systems Engineer"},
        "langgraph": {"canonical": "Agentic AI & Orchestration Frameworks", "category": "Artificial Intelligence", "esco_code": "S2.1.6", "occupation": "Agentic AI Engineer"},

        # Data & Databases
        "sql": {"canonical": "Relational Databases & SQL", "category": "Data Management", "esco_code": "S3.1.1", "occupation": "Database Administrator"},
        "postgresql": {"canonical": "PostgreSQL & Advanced Relational Systems", "category": "Data Management", "esco_code": "S3.1.2", "occupation": "Backend Database Engineer"},
        "nosql": {"canonical": "NoSQL & Distributed Data Stores", "category": "Data Management", "esco_code": "S3.1.3", "occupation": "Data Architect"},
        "vector database": {"canonical": "Vector Databases (pgvector, Chroma, Pinecone)", "category": "Data Management", "esco_code": "S3.1.4", "occupation": "AI Data Engineer"},

        # Cloud, DevOps & Systems
        "docker": {"canonical": "Containerization (Docker)", "category": "DevOps & Cloud", "esco_code": "S4.1.1", "occupation": "DevOps Engineer"},
        "kubernetes": {"canonical": "Container Orchestration (Kubernetes)", "category": "DevOps & Cloud", "esco_code": "S4.1.2", "occupation": "Cloud Reliability Engineer"},
        "aws": {"canonical": "Cloud Platforms (AWS / GCP / Azure)", "category": "DevOps & Cloud", "esco_code": "S4.1.3", "occupation": "Cloud Solutions Architect"},
        "ci/cd": {"canonical": "Continuous Integration & Deployment (CI/CD)", "category": "DevOps & Cloud", "esco_code": "S4.1.4", "occupation": "DevOps Specialist"},
        "git": {"canonical": "Version Control (Git)", "category": "Software Engineering Tools", "esco_code": "S4.1.5", "occupation": "Software Engineer"},

        # Security
        "cybersecurity": {"canonical": "Cybersecurity & Application Security", "category": "Security & Trust", "esco_code": "S5.1.1", "occupation": "Security Engineer"},
        "cryptography": {"canonical": "Applied Cryptography & Secure Protocols", "category": "Security & Trust", "esco_code": "S5.1.2", "occupation": "Security Architect"},
    }

    @classmethod
    def normalize_skill(cls, raw_skill_name: str) -> Dict[str, Any]:
        """Normalize a skill name into canonical name, ESCO category, and occupation."""
        clean = raw_skill_name.lower().strip()
        clean = re.sub(r"[^\w\s\+\#\/]", "", clean)

        for key, val in cls.SKILL_TAXONOMY_MAP.items():
            if key == clean or key in clean or clean in key:
                return {
                    "raw_skill": raw_skill_name,
                    "canonical_name": val["canonical"],
                    "category": val["category"],
                    "esco_code": val["esco_code"],
                    "target_occupation": val["occupation"],
                    "match_type": "EXACT" if key == clean else "SEMANTIC"
                }

        # Fallback category
        return {
            "raw_skill": raw_skill_name,
            "canonical_name": raw_skill_name.title(),
            "category": "General Engineering Competency",
            "esco_code": "S0.0.0",
            "target_occupation": "Software Engineer",
            "match_type": "HEURISTIC"
        }
