"""
Memory API: Short-Term, Long-Term, and Semantic pgvector Memory Explorer.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.database.session import get_db
from app.models.users import User
from app.models.agent_history import MemoryRecord
from app.memory.semantic_store import SemanticMemoryStore
from app.auth.rbac import get_current_user

router = APIRouter(prefix="/memory", tags=["Memory Explorer"])


@router.get("")
def list_memory_records(
    memory_type: Optional[str] = None,
    scope_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List memory records (short-term, long-term, semantic) with access counts."""
    stmt = select(MemoryRecord)
    if memory_type:
        stmt = stmt.where(MemoryRecord.memory_type == memory_type)
    if scope_type:
        stmt = stmt.where(MemoryRecord.scope_type == scope_type)

    stmt = stmt.order_by(desc(MemoryRecord.created_at)).limit(limit)
    records = db.execute(stmt).scalars().all()

    return [
        {
            "id": r.id,
            "memory_type": r.memory_type,
            "scope_type": r.scope_type,
            "scope_id": r.scope_id,
            "key": r.key,
            "content_preview": r.content_text[:120] + "..." if len(r.content_text) > 120 else r.content_text,
            "metadata": r.metadata_json,
            "has_embedding": bool(r.embedding_json),
            "access_count": r.access_count,
            "last_accessed_at": r.last_accessed_at.isoformat() if r.last_accessed_at else None,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]


@router.get("/{memory_id}")
def get_memory_record(
    memory_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve full content and embedding vector metadata of a memory record."""
    r = db.execute(select(MemoryRecord).where(MemoryRecord.id == memory_id)).scalar_one_or_none()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory record not found")

    r.access_count += 1
    db.commit()

    return {
        "id": r.id,
        "memory_type": r.memory_type,
        "scope_type": r.scope_type,
        "scope_id": r.scope_id,
        "key": r.key,
        "content_text": r.content_text,
        "metadata": r.metadata_json,
        "embedding_dimensions": len(r.embedding_json) if r.embedding_json else 0,
        "access_count": r.access_count,
        "created_at": r.created_at.isoformat()
    }


@router.post("/search")
def search_semantic_memory(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Semantic vector search across memory records using cosine similarity."""
    query = payload.get("query", "")
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="query string required")

    scope_type = payload.get("scope_type")
    scope_id = payload.get("scope_id")
    limit = int(payload.get("limit", 5))

    results = SemanticMemoryStore.search_similar(
        db=db,
        query=query,
        scope_type=scope_type,
        scope_id=scope_id,
        limit=limit
    )

    return {"query": query, "total_matches": len(results), "results": results}


@router.post("")
def create_memory_record(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Store a custom knowledge or memory record with computed vector embedding."""
    key = payload.get("key", "custom_knowledge")
    content = payload.get("content_text", "")
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="content_text required")

    mem_type = payload.get("memory_type", "SEMANTIC")
    scope_type = payload.get("scope_type", "PROGRAMME")
    scope_id = payload.get("scope_id", "BT-CSE")
    metadata = payload.get("metadata", {})

    record = SemanticMemoryStore.store_memory(
        db=db,
        memory_type=mem_type,
        scope_type=scope_type,
        scope_id=scope_id,
        key=key,
        content=content,
        metadata=metadata
    )

    return {"id": record.id, "message": "Memory record created and embedded successfully.", "key": record.key}
