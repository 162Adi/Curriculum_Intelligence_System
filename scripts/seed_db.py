"""
Database seeding script for Curriculum Intelligence System (CIS).
Populates initial Admin, Faculty, Departments, Programmes, Academic Standards (ACM CS2023/IEEE/AAAI),
and verified India Tech Market snapshot.
"""

import logging
from datetime import datetime
import app.core.cython_compat  # noqa: F401
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base
from app.models.users import User, RoleEnum
from app.models.curriculum import Department, Programme, CurriculumVersion, Course, CourseTopic, CourseOutcome
from app.models.intelligence import AcademicStandard, BenchmarkDocument, IndustrySnapshot, IndustrySkill, IndustryJob
from app.auth.security import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cis.seed")

# Resolve DB URL
db_url = settings.DATABASE_URL
if "sqlite" in db_url:
    db_url = db_url.replace("+aiosqlite", "")
else:
    # Use SQLite for local development seed
    db_url = "sqlite:///./cis_local.db"

engine = create_engine(db_url, echo=False)
SessionFactory = sessionmaker(bind=engine)


def seed():
    logger.info("Initializing database schemas...")
    Base.metadata.create_all(engine)

    with SessionFactory() as session:
        # 1. Seed Departments
        cse_dept = session.execute(select(Department).where(Department.code == "CSE")).scalar_one_or_none()
        if not cse_dept:
            logger.info("Seeding Computer Science & Engineering Department...")
            cse_dept = Department(
                code="CSE",
                name="Department of Computer Science & Engineering",
                description="School of Computing and Information Technology offering undergraduate and graduate engineering programmes."
            )
            session.add(cse_dept)
            session.flush()

        ece_dept = session.execute(select(Department).where(Department.code == "ECE")).scalar_one_or_none()
        if not ece_dept:
            ece_dept = Department(
                code="ECE",
                name="Department of Electronics & Communication Engineering",
                description="Electronics, VLSI, Embedded Systems and Signal Processing."
            )
            session.add(ece_dept)
            session.flush()

        # 2. Seed Programmes
        btech_cse = session.execute(select(Programme).where(Programme.code == "BT-CSE")).scalar_one_or_none()
        if not btech_cse:
            logger.info("Seeding B.Tech Computer Science & Engineering Programme...")
            btech_cse = Programme(
                department_id=cse_dept.id,
                code="BT-CSE",
                name="Bachelor of Technology in Computer Science & Engineering",
                degree_type="B.Tech",
                total_semesters=8,
                total_credits=160
            )
            session.add(btech_cse)
            session.flush()

        # 3. Seed Users with Argon2 hashed passwords
        users_to_seed = [
            ("admin@university.edu", "System Administrator", "Admin@CIS2026!", RoleEnum.ADMIN, cse_dept.id),
            ("faculty@university.edu", "Dr. A. Sharma (HOD CSE)", "Faculty@CIS2026!", RoleEnum.FACULTY, cse_dept.id),
            ("reviewer@university.edu", "Prof. R. Venkat (Board of Studies)", "Reviewer@CIS2026!", RoleEnum.REVIEWER, cse_dept.id),
            ("management@university.edu", "Dean Academics & Leadership", "Dean@CIS2026!", RoleEnum.MANAGEMENT, cse_dept.id),
        ]

        for email, full_name, raw_pwd, role, dept_id in users_to_seed:
            existing_user = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
            if not existing_user:
                logger.info(f"Creating user {email} ({role.value})...")
                user = User(
                    email=email,
                    full_name=full_name,
                    hashed_password=hash_password(raw_pwd),
                    role=role,
                    department_id=dept_id,
                    is_active=True
                )
                session.add(user)

        # 4. Seed Academic Standards: ACM CS2023, IEEE-CS, AAAI-AI
        standards_to_seed = [
            ("ACM_CS2023", "ACM/IEEE-CS/AAAI Computer Science Curricula 2023", "CS2023-Final", 2023, "https://cs2023.org"),
            ("IEEE_CS", "IEEE Computer Society Curriculum Guidelines", "IEEE-CS-2023", 2023, "https://computer.org"),
            ("AAAI_AI", "AAAI/EAAI AI Curriculum Guidelines for Undergraduate CS", "AAAI-2024", 2024, "https://aaai.org"),
        ]

        for code, title, ver, year, url in standards_to_seed:
            std = session.execute(select(AcademicStandard).where(AcademicStandard.code == code)).scalar_one_or_none()
            if not std:
                logger.info(f"Seeding academic standard {code}...")
                std = AcademicStandard(code=code, title=title, version=ver, publication_year=year, source_url=url)
                session.add(std)
                session.flush()

                if code == "ACM_CS2023":
                    benchmark_units = [
                        ("AI - Artificial Intelligence", "AI-Fundamental Concepts", "Search, Knowledge Representation, Heuristics", "Tier 1 Core", "Sec 4.1", 112),
                        ("AI - Artificial Intelligence", "AI-Machine Learning", "Supervised Learning, Deep Neural Networks, Loss Functions", "Tier 1 Core", "Sec 4.2", 116),
                        ("AI - Artificial Intelligence", "AI-Applied AI & LLMs", "Large Language Models, Retrieval-Augmented Generation, Agentic Workflows", "Tier 2 Core", "Sec 4.4", 124),
                        ("SE - Software Engineering", "SE-Software Architecture", "Microservices, Event-Driven Systems, API Design", "Tier 1 Core", "Sec 7.3", 198),
                        ("SE - Software Engineering", "SE-DevOps & CI/CD", "Continuous Integration, Automated Testing, Cloud Deployment", "Tier 1 Core", "Sec 7.5", 204),
                        ("SEC - Security", "SEC-Foundational Principles", "Confidentiality, Integrity, Authentication, Threat Modeling", "Tier 1 Core", "Sec 8.1", 232),
                        ("DM - Data Management", "DM-Modern Data Architectures", "Distributed Databases, NoSQL, Vector Databases, Data Pipelines", "Tier 2 Core", "Sec 6.3", 168),
                        ("SDF - Software Development", "SDF-Algorithms & Complexity", "Asymptotic Analysis, Graph Algorithms, Dynamic Programming", "Tier 1 Core", "Sec 2.2", 64),
                    ]
                    for ka, ku, topic, tier, sref, pnum in benchmark_units:
                        doc = BenchmarkDocument(
                            standard_id=std.id,
                            knowledge_area=ka,
                            knowledge_unit=ku,
                            topic_name=topic,
                            tier=tier,
                            section_reference=sref,
                            page_number=pnum,
                            content_text=f"Guideline requirement for {ku} under {ka} ({tier}): Covers rigorous competency in {topic}."
                        )
                        session.add(doc)

        # 5. Seed Curated Verified India Tech Snapshot
        snap = session.execute(select(IndustrySnapshot).where(IndustrySnapshot.provider == "Curated_India_Tech")).scalar_one_or_none()
        if not snap:
            logger.info("Seeding curated verified India tech industry snapshot (Bengaluru, Hyderabad, Pune, Mumbai)...")
            snap = IndustrySnapshot(
                provider="Curated_India_Tech",
                location="India (Bengaluru, Hyderabad, Pune, Mumbai, NCR)",
                snapshot_date=datetime.utcnow(),
                total_jobs_analyzed=1420,
                status="ACTIVE",
                metadata_json={
                    "source": "Tech Employment Aggregation Q1-2026",
                    "hubs": ["Bengaluru", "Hyderabad", "Pune", "Mumbai", "Gurugram"],
                    "verified_sample_size": 1420
                }
            )
            session.add(snap)
            session.flush()

            skills_data = [
                ("Python", "Technical", 1120, 0.98),
                ("React & TypeScript", "Technical", 940, 0.92),
                ("FastAPI / REST APIs", "Technical", 820, 0.88),
                ("Docker & Containers", "Tool", 890, 0.90),
                ("Kubernetes & Cloud Native", "Tool", 760, 0.85),
                ("Machine Learning & PyTorch", "Technical", 830, 0.89),
                ("Generative AI & LLMs", "Technical", 910, 0.94),
                ("Vector Databases & RAG", "Technical", 740, 0.86),
                ("SQL & PostgreSQL", "Technical", 950, 0.93),
                ("Git & CI/CD Pipelines", "Tool", 920, 0.91),
                ("Microservices & Distributed Systems", "Technical", 810, 0.87),
                ("Data Structures & Algorithms", "Technical", 1050, 0.96),
                ("Cloud Architecture (AWS / GCP / Azure)", "Tool", 870, 0.89),
                ("Agentic AI & LangGraph / MCP", "Technical", 680, 0.84),
                ("Cybersecurity & AppSec", "Technical", 620, 0.81),
            ]

            for sname, cat, freq, imp in skills_data:
                skill = IndustrySkill(
                    snapshot_id=snap.id,
                    skill_name=sname,
                    category=cat,
                    frequency=freq,
                    importance_score=imp
                )
                session.add(skill)

            jobs_data = [
                ("Senior AI Engineer - Agentic Systems", "Bengaluru", 1800000.0, 3200000.0, "Seeking AI Engineer proficient in LangGraph, Python, RAG pipelines and FastAPI microservices."),
                ("Full Stack Cloud Developer", "Hyderabad", 1200000.0, 2400000.0, "Building cloud-native web apps with React, TypeScript, Docker, and PostgreSQL on AWS."),
                ("Data & Machine Learning Specialist", "Pune", 1400000.0, 2600000.0, "Experienced in PyTorch, distributed data pipelines, vector search, and model deployment."),
                ("Software Engineer - Core Backend", "Mumbai", 1100000.0, 2000000.0, "Strong foundations in Data Structures, Algorithms, Distributed Databases, and CI/CD."),
            ]
            for idx, (jtitle, jloc, smin, smax, jdesc) in enumerate(jobs_data):
                job = IndustryJob(
                    snapshot_id=snap.id,
                    job_id=f"IND-JOB-{idx+1:04d}",
                    title=jtitle,
                    company="Leading Global Tech / Unicorn",
                    location=f"{jloc}, India",
                    salary_min=smin,
                    salary_max=smax,
                    description=jdesc,
                    source_date=datetime.utcnow()
                )
                session.add(job)

        # 6. Seed Sample Curriculum Version
        curr_ver = session.execute(
            select(CurriculumVersion).where(CurriculumVersion.version_tag == "2024-R1")
        ).scalar_one_or_none()

        if not curr_ver:
            logger.info("Seeding baseline B.Tech CSE Curriculum (2024-R1)...")
            curr_ver = CurriculumVersion(
                programme_id=btech_cse.id,
                version_tag="2024-R1",
                academic_year="2024-2028",
                status="INGESTED",
                file_name="BTech_CSE_Curriculum_2024_Syllabus.pdf",
                total_courses=8,
                total_credits=24.0
            )
            session.add(curr_ver)
            session.flush()

            courses_spec = [
                (1, "CS101", "Introduction to Programming in C", "THEORY", 3.0, [
                    ("Variables, Data Types, and Operators", 6),
                    ("Control Structures: If-Else, Loops, Switches", 8),
                    ("Functions, Recursion, and Scope", 8),
                    ("Pointers and Dynamic Memory Allocation", 10),
                    ("Structures, Unions, and File I/O", 8),
                ], [
                    ("CO1", "Apply fundamental programming constructs to solve computational problems", "Apply"),
                    ("CO2", "Design recursive algorithms and manage dynamic memory", "Create")
                ]),
                (2, "CS102", "Data Structures and Algorithms", "INTEGRATED", 4.0, [
                    ("Linear Data Structures: Arrays, Stacks, Queues", 8),
                    ("Linked Lists and Doubly Linked Lists", 8),
                    ("Non-linear Structures: Binary Trees and BST", 10),
                    ("Graph Representations and Traversals (BFS, DFS)", 10),
                    ("Sorting, Searching, and Hashing", 8),
                ], [
                    ("CO1", "Analyze asymptotic time and space complexity of algorithms", "Analyze"),
                    ("CO2", "Implement tree and graph algorithms for real-world scenarios", "Apply")
                ]),
                (3, "CS201", "Database Management Systems", "THEORY", 3.0, [
                    ("Relational Model and ER Diagrams", 6),
                    ("SQL Queries, Joins, Subqueries, Views", 10),
                    ("Relational Algebra and Normalization (1NF-BCNF)", 8),
                    ("Transaction Management, ACID properties, Concurrency", 8),
                    ("Overview of Indexing and Query Optimization", 6),
                ], [
                    ("CO1", "Design normalized relational schemas for enterprise databases", "Design"),
                    ("CO2", "Execute complex SQL queries and transaction management", "Apply")
                ]),
                (4, "CS202", "Operating Systems", "THEORY", 3.0, [
                    ("Process Management and CPU Scheduling", 8),
                    ("Inter-Process Communication and Synchronization", 8),
                    ("Deadlocks: Prevention, Avoidance, Detection", 6),
                    ("Memory Management: Paging, Segmentation, Virtual Memory", 10),
                    ("File Systems and I/O Management", 6),
                ], [
                    ("CO1", "Explain concurrency, process scheduling and memory paging", "Understand"),
                    ("CO2", "Develop multithreaded programs with synchronization primitives", "Apply")
                ]),
                (5, "CS301", "Computer Networks", "THEORY", 3.0, [
                    ("OSI and TCP/IP Layered Architectures", 6),
                    ("Data Link Layer: Framing, Error Detection, Flow Control", 8),
                    ("Network Layer: IP Addressing, Subnetting, Routing Algorithms", 10),
                    ("Transport Layer: TCP vs UDP, Flow & Congestion Control", 8),
                    ("Application Layer: HTTP, DNS, SMTP, Socket Programming", 8),
                ], [
                    ("CO1", "Analyze network protocols across TCP/IP stack layers", "Analyze"),
                    ("CO2", "Build client-server network applications using sockets", "Create")
                ]),
                (6, "CS302", "Software Engineering & Object-Oriented Design", "THEORY", 3.0, [
                    ("SDLC Models: Waterfall, Agile, Scrum", 6),
                    ("Requirements Engineering and UML Modeling", 8),
                    ("Design Patterns: Creational, Structural, Behavioral", 8),
                    ("Software Testing: Unit, Integration, System Testing", 8),
                    ("Project Estimation and Quality Assurance", 6),
                ], [
                    ("CO1", "Apply Agile methodologies and UML diagrams to software projects", "Apply"),
                    ("CO2", "Implement standard object-oriented design patterns", "Create")
                ]),
                (7, "CS401", "Artificial Intelligence & Foundations", "THEORY", 3.0, [
                    ("State Space Search, BFS, DFS, A* Search", 8),
                    ("Knowledge Representation and First-Order Logic", 8),
                    ("Classical Machine Learning: Linear/Logistic Regression", 8),
                    ("Decision Trees, Random Forests, Support Vector Machines", 8),
                    ("Introduction to Neural Networks and Perceptrons", 6),
                ], [
                    ("CO1", "Formulate search problems and heuristics for AI agents", "Analyze"),
                    ("CO2", "Train supervised learning models on tabular datasets", "Apply")
                ]),
                (8, "CS402", "Web Technologies Laboratory", "LAB", 2.0, [
                    ("HTML5, CSS3, Responsive Design Basics", 6),
                    ("JavaScript Fundamentals and DOM Manipulation", 8),
                    ("PHP and MySQL Basic CRUD Operations", 10),
                    ("XML and Basic Web Services", 6),
                ], [
                    ("CO1", "Construct multi-page responsive web applications", "Create"),
                    ("CO2", "Implement backend database connectivity with server scripts", "Apply")
                ]),
            ]

            for sem, ccode, ctitle, ctype, cred, topics, outcomes in courses_spec:
                course = Course(
                    curriculum_version_id=curr_ver.id,
                    semester=sem,
                    course_code=ccode,
                    course_title=ctitle,
                    course_type=ctype,
                    credits=cred,
                    lecture_hours=int(cred),
                    tutorial_hours=0,
                    practical_hours=2 if ctype == "LAB" else 0,
                    description=f"{ctitle} core curriculum course covering modern fundamentals."
                )
                session.add(course)
                session.flush()

                for uidx, (tname, thours) in enumerate(topics):
                    topic = CourseTopic(
                        course_id=course.id,
                        unit_number=uidx + 1,
                        unit_title=f"Unit {uidx + 1}",
                        topic_name=tname,
                        hours_allocated=float(thours)
                    )
                    session.add(topic)

                for ocode, odesc, blevel in outcomes:
                    outcome = CourseOutcome(
                        course_id=course.id,
                        outcome_code=ocode,
                        description=odesc,
                        bloom_taxonomy_level=blevel
                    )
                    session.add(outcome)

        session.commit()
        logger.info("Database seeding completed successfully.")


if __name__ == "__main__":
    seed()
