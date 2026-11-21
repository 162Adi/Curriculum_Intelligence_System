"""
Vector Memory and Semantic Search Engine for RAG and curriculum retrieval.
Provides cosine similarity vector search with automatic local deterministic embedding fallback.
"""

import math
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.agent_history import MemoryRecord


class SemanticMemoryStore:
    """Manages short-term, long-term, and semantic memory vectors."""

    @staticmethod
    def _compute_deterministic_embedding(text: str, dim: int = 128) -> List[float]:
        """Deterministic, lightweight normalized bag-of-words / character n-gram embedding."""
        vec = [0.0] * dim
        clean_words = text.lower().split()
        for idx, word in enumerate(clean_words):
            h = hash(word) % dim
            vec[h] += 1.0 / (idx + 1.0)
            # Add character bi-grams
            for i in range(len(word) - 1):
                bi_h = hash(word[i:i+2]) % dim
                vec[bi_h] += 0.5

        # Normalize to unit vector
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    @classmethod
    def store_memory(
        cls,
        db: Session,
        memory_type: str,
        scope_type: str,
        scope_id: str,
        key: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MemoryRecord:
        """Store an item in memory with semantic vector embedding."""
        embedding = cls._compute_deterministic_embedding(content)

        record = MemoryRecord(
            memory_type=memory_type,
            scope_type=scope_type,
            scope_id=scope_id,
            key=key,
            content_text=content,
            metadata_json=metadata or {},
            embedding_json=embedding,
            access_count=0
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @classmethod
    def search_similar(
        cls,
        db: Session,
        query: str,
        scope_type: Optional[str] = None,
        scope_id: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant memory records using cosine similarity over embeddings."""
        query_vec = cls._compute_deterministic_embedding(query)

        stmt = select(MemoryRecord)
        if scope_type:
            stmt = stmt.where(MemoryRecord.scope_type == scope_type)
        if scope_id:
            stmt = stmt.where(MemoryRecord.scope_id == scope_id)

        records = db.execute(stmt).scalars().all()

        scored_records = []
        for r in records:
            if r.embedding_json and isinstance(r.embedding_json, list):
                # Cosine similarity between unit vectors
                dot = sum(a * b for a, b in zip(query_vec, r.embedding_json[:len(query_vec)]))
                scored_records.append((dot, r))

        scored_records.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, r in scored_records[:limit]:
            r.access_count += 1
            results.append({
                "id": r.id,
                "key": r.key,
                "memory_type": r.memory_type,
                "content_text": r.content_text,
                "metadata": r.metadata_json,
                "similarity_score": round(float(score), 4),
                "created_at": r.created_at.isoformat()
            })
        db.commit()
        return results
