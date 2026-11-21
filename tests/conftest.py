"""
Global Pytest Configuration and Fixtures for Curriculum Intelligence System.
"""
import os
import sys
import pytest

# Ensure backend and project root are on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [backend_dir, project_root]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Initialize Cython compatibility shim for Windows environments
import app.core.cython_compat

from app.database.session import SessionLocal, init_db, engine
from app.models.users import User, Role
from app.models.curriculum import Department, Programme, Curriculum, Course
from app.auth.security import get_password_hash


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database schema is created and initialized."""
    init_db()
    yield


@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional database session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def sample_curriculum(db_session):
    """Retrieve or create a test curriculum."""
    curr = db_session.query(Curriculum).first()
    if not curr:
        dept = Department(name="Computer Science & Engineering", code="CSE")
        db_session.add(dept)
        db_session.flush()

        prog = Programme(
            department_id=dept.id,
            name="B.Tech Computer Science & Engineering",
            code="BTECH-CSE",
            degree_type="B.Tech",
            total_semesters=8,
            total_credits=160
        )
        db_session.add(prog)
        db_session.flush()

        curr = Curriculum(
            programme_id=prog.id,
            academic_year="2024-2025",
            version_tag="2024-R1",
            status="ANALYZED"
        )
        db_session.add(curr)
        db_session.commit()
    return curr
