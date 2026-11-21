# CURRICULUM INTELLIGENCE SYSTEM (CIS)

> *"Bridging Academic Learning and Industry Requirements Through Agentic Intelligence."*

---

## 1. Executive Summary & Purpose

The **Curriculum Intelligence System (CIS)** is a university-grade multi-agent AI platform engineered to solve a critical academic problem: **the divergence between university curricula and rapidly evolving industry competencies**.

Traditional curriculum revision cycles take 3 to 5 years, relying on manual faculty committees and subjective surveys. CIS replaces this with continuous, evidence-based agentic intelligence. Powered by **LangGraph orchestration**, a **Model Context Protocol (MCP)** server, an **OpenClaw runtime gateway**, and deterministic mathematical gap scoring, CIS autonomously maps curricula, queries live job vacancy data (Adzuna & ESCO), benchmarks international academic standards (ACM CS2023, IEEE-CS, AAAI), computes gaps, and synthesizes faculty-in-the-loop proposals with one-click export to accreditation-ready PDF, Excel, and PowerPoint dossiers.

---

## 2. System Architecture & Product Sections

CIS is built as two distinct yet seamlessly interconnected product sections:

```
Curriculum Intelligence System (CIS)
├── SECTION A: MAIN CURRICULUM INTELLIGENCE APPLICATION (Core University Product)
│   ├── 1. University Authentication & Role-Based Access Control (RBAC)
│   ├── 2. Department & Academic Programme Selection
│   ├── 3. Multi-Format Curriculum Ingestion (PDF, DOCX, XLSX, CSV)
│   ├── 4. Course, Unit & Learning Outcome Structure Workspace
│   ├── 5. Interactive LangGraph Agent Control Room (React Flow)
│   ├── 6. Industry Intelligence & Skill Demand Analytics (Adzuna + ESCO)
│   ├── 7. Academic Benchmarking (ACM CS2023 / IEEE-CS / AAAI)
│   ├── 8. Deterministic Mathematical Gap Analysis (Gap = Importance * (1 - Coverage))
│   ├── 9. Actionable Curriculum Revision Recommendations (DRAFT Status)
│   ├── 10. Granular Faculty Review, Revision Requests & BoS Sign-off
│   └── 11. Multi-Format Report Generation (ReportLab PDF, openpyxl XLSX, python-pptx PPTX)
│
└── SECTION B: AGENTIC AI STUDIO (13 University Curriculum Capabilities)
    ├── 1. Agent vs Chatbot (Perception -> Tool -> Reflection Loop)
    ├── 2. Tool-Using Agent (Dynamic Schema & Function Execution)
    ├── 3. Skill Creation (Authoring & Registering Modular Skills)
    ├── 4. Memory & Retrieval (Working Memory, Checkpoints, Vector Search)
    ├── 5. MCP-Style Connector (Model Context Protocol Port 8001)
    ├── 6. OpenClaw Runtime (Gateway Adapter Port 18789)
    ├── 7. Agentic Node Graph (LangGraph StateGraph Visualizer)
    ├── 8. Parallel Swarm (Concurrent Execution & State Convergence)
    ├── 9. Deep Research Agent (Multi-Source Cited Inquiry)
    ├── 10. Cloud Operations Agent (Health Telemetry & Latency Probes)
    ├── 11. Agentic SDLC Factory (Automated Schema Tests & Bloom's Validation)
    ├── 12. Safety & Governance (Deterministic Injection Defense & RBAC Gates)
    └── 13. Discipline-Specific Agents (Mechanical ASME, Civil ASCE, Electrical IEEE)
```

---

## 3. Technology Stack

| Domain | Technology / Library | Architectural Role |
| :--- | :--- | :--- |
| **Frontend UI** | React 18, Vite 5, TypeScript | Reactive modern single-page application |
| **Styling** | Tailwind CSS 3, Lucide Icons | Dark slate academic design system |
| **Interactive Graph** | `@xyflow/react` (React Flow v12) | Dynamic agent node graph with real-time status pulses |
| **Visualizations** | Recharts | Market demand vs coverage radar charts and bar distributions |
| **State Management** | Zustand 5, TanStack Query 5 | Client-side auth, curriculum cache, and server sync |
| **Notifications** | Sonner | Real-time toast feedback |
| **Backend API** | Python 3.11+, FastAPI, Uvicorn | Async REST endpoints and WebSocket event streams |
| **Agent Orchestration** | LangGraph StateGraph | Directed acyclic graph with checkpointing and human-in-the-loop gates |
| **Data Persistence** | PostgreSQL / SQLite WAL, SQLAlchemy 2 | ACID storage with zero-dependency SQLite WAL fallback |
| **Vector Memory** | Unit-Vector Cosine Engine / pgvector | Semantic standard retrieval and revision similarity |
| **Tool Protocol** | Python MCP SDK (`mcp`) | Official Model Context Protocol Server (Port 8001) |
| **Worker Runtime** | OpenClaw Gateway Service | Dedicated runtime service adapter (Port 18789) |
| **Security & Auth** | Argon2id (`argon2-cffi`), PyJWT | Memory-hard password hashing and JWT access/refresh tokens |
| **Document Parsing** | PyMuPDF, `pypdf`, `python-docx`, `openpyxl` | Resilient multi-format syllabus extractor |
| **Accreditation Reports** | ReportLab, `openpyxl`, `python-pptx` | Numbered-canvas PDFs, multi-tab Excel, and presentation decks |
| **Test Suite** | pytest, pytest-asyncio | 22 comprehensive unit, agent, integration, security, and E2E tests |

---

## 4. The 5 Specialized Curriculum Agents

1. **Curriculum Mapping Agent**: Ingests raw syllabi, normalizes departmental terminology, extracts course codes, contact hours, credits, units, and Course Learning Outcomes (CLOs).
2. **Industry Skills Agent**: Connects to the **Adzuna API** and **ESCO Taxonomy** to analyze 1,420 Indian tech job vacancies across Bengaluru, Hyderabad, and Pune, quantifying market demand for technical competencies.
3. **Academic Benchmarking Agent**: Cross-references curriculum content against international curricular guidelines: **ACM CS2023 Guidelines**, **IEEE Computer Society standards**, and the **AAAI Model AI Curriculum**.
4. **Gap Analysis Agent**: Evaluates curriculum deficits using the deterministic mathematical formula:
   $$\text{Gap Score} = \text{Importance} \times (1.0 - \text{Coverage})$$
   Categorizes weaknesses into Critical ($\ge 70$), High ($\ge 45$), Medium ($\ge 25$), and Low ($< 25$).
5. **Recommendation Agent**: Formulates proposed curriculum actions (`ADD_TOPIC`, `NEW_COURSE`, `UPDATE_OUTCOME`, `PEDAGOGY`) stored in `DRAFT` status awaiting faculty review.

---

## 5. Pre-Seeded Test Credentials

The system includes pre-seeded accounts configured with Argon2id password hashes:

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Faculty** | `faculty@university.edu` | `Faculty@CIS2026!` | Upload syllabi, confirm structure, inspect swarm, approve recommendations |
| **Reviewer** | `reviewer@university.edu` | `Reviewer@CIS2026!` | Inspect benchmark evidence, add review comments, evaluate gaps |
| **Management** | `management@university.edu` | `Dean@CIS2026!` | Executive dashboard, BoS final sign-off, download accreditation reports |
| **Admin** | `admin@university.edu` | `Admin@CIS2026!` | Full RBAC user management, system diagnostics, configuration |

> **Note**: The login screen features **Instant Role Access buttons** allowing one-click login for any of the 4 roles without typing credentials.

---

## 6. Quick Start Guide (Windows PowerShell)

### Prerequisites
- Python 3.11+ installed and on `PATH`
- Node.js 18+ and `npm` installed and on `PATH`

### Step 1: Install Dependencies
```powershell
# In project root (D:\OG_Agentic)
pip install -r backend/requirements.txt
npm --prefix frontend install
```

### Step 2: Seed Database
Populates the CSE Department, B.Tech CSE programme, 8 core syllabus courses (`2024-R1`), ACM CS2023 standards, 1,420 tech job market skills, and all 4 test users:
```powershell
$env:PYTHONPATH = "backend;."
python scripts/seed_db.py
```

### Step 3: Launch All Services (One Command)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_cis.ps1
```
This automatically launches all 4 services in their respective ports:
- **Frontend App**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000/docs`
- **MCP Server**: `http://localhost:8001/mcp/tools`
- **OpenClaw Gateway**: `http://localhost:18789/health`

### Launching Services Individually
```powershell
# 1. Start OpenClaw Gateway (Port 18789)
python openclaw/gateway_service.py

# 2. Start MCP Server (Port 8001)
python mcp_server/server.py

# 3. Start Backend FastAPI (Port 8000)
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 4. Start Frontend (Port 5173)
cd frontend
npm run dev
```

---

## 7. Running the Automated Test Suite

CIS includes a comprehensive test suite covering unit tests, agents, security guardrails, integrations, and end-to-end multi-agent execution:

```powershell
$env:PYTHONPATH = "backend;."
pytest tests/ -v
```

### Test Suite Summary
```
tests/agents/test_curriculum_agents.py::test_curriculum_mapping_agent PASSED
tests/agents/test_curriculum_agents.py::test_industry_skills_agent PASSED
tests/agents/test_curriculum_agents.py::test_academic_benchmarking_agent PASSED
tests/agents/test_curriculum_agents.py::test_gap_analysis_and_recommendations PASSED
tests/agents/test_curriculum_agents.py::test_deep_research_agent PASSED
tests/agents/test_curriculum_agents.py::test_quality_evaluator PASSED
tests/end_to_end/test_full_workflow.py::test_full_curriculum_analysis_pipeline PASSED
tests/integration/test_mcp_openclaw.py::test_mcp_tool_catalog PASSED
tests/integration/test_mcp_openclaw.py::test_mcp_gap_tool_execution PASSED
tests/integration/test_mcp_openclaw.py::test_openclaw_adapter_interface PASSED
tests/integration/test_reports.py::test_pdf_report_generation PASSED
tests/integration/test_reports.py::test_excel_report_generation PASSED
tests/integration/test_reports.py::test_pptx_report_generation PASSED
tests/security/test_security_guardrails.py::test_prompt_injection_scanner PASSED
tests/security/test_security_guardrails.py::test_approval_boundary_enforcement PASSED
tests/unit/test_auth_security.py::test_argon2_password_hashing PASSED
tests/unit/test_auth_security.py::test_jwt_access_and_refresh_tokens PASSED
tests/unit/test_auth_security.py::test_invalid_token_decoding PASSED
tests/unit/test_extractor.py::test_csv_extraction PASSED
tests/unit/test_extractor.py::test_docx_extraction PASSED
tests/unit/test_gap_formula.py::test_gap_score_formula_calculation PASSED
tests/unit/test_gap_formula.py::test_gap_boundary_values PASSED

====================== 22 passed in 2.02s =======================
```

---

## 8. Section B — Agentic AI Studio (13 Capabilities)

The **Agentic AI Studio** (`/studio`) demonstrates the 13 foundational agentic capabilities:

1. **Agent vs Chatbot** (`/studio/agent-vs-chatbot`): Contrasts passive single-turn responses with autonomous goal execution loops.
2. **Tool-Using Agent** (`/studio/tool-using-agent`): Dynamic tool selection and Pydantic schema validation.
3. **Skill Creation** (`/studio/skill-creation`): Dynamic authoring and registration of reusable modular skills.
4. **Memory & Retrieval** (`/studio/memory-retrieval`): Short-term working RAM, persistent PostgreSQL checkpoints, and vector cosine retrieval.
5. **MCP-Style Connector** (`/studio/mcp-connector`): Model Context Protocol v1.0 tool federation on port 8001.
6. **OpenClaw Runtime** (`/studio/openclaw-runtime`): Dedicated gateway connection and subagent dispatch on port 18789.
7. **Agentic Node Graph** (`/studio/node-graph`): LangGraph StateGraph traversal and checkpointing visualization.
8. **Parallel Swarm** (`/studio/parallel-swarm`): True concurrent multi-agent execution (`asyncio.gather`) and speedup measurement.
9. **Deep Research Agent** (`/studio/deep-research`): Autonomous multi-source cited inquiry and evidence synthesis.
10. **Cloud Operations Agent** (`/studio/cloud-ops`): Automated health telemetry, latency probes, and API quota monitoring.
11. **Agentic SDLC Factory** (`/studio/sdlc-factory`): Automated test generation, schema verification, and Bloom's taxonomy tests.
12. **Safety & Governance** (`/studio/safety-governance`): Deterministic prompt injection scanning and RBAC approval barriers.
13. **Discipline-Specific Agents** (`/studio/discipline-agents`): Specialized domain models for Mechanical (ASME), Civil (ASCE), and Electrical (IEEE) Engineering.

---

## 9. Security & Governance Compliance

- **No Self-Approval**: Autonomous AI agents strictly create recommendations in `DRAFT` status; only verified faculty or administrators can approve modifications.
- **Prompt Injection Defense**: Every uploaded syllabus and input prompt is scanned by the deterministic regex & semantic pattern filter before analysis.
- **Accreditation Audit Trail**: All actions, approvals, and report generations are permanently logged in the `audit_logs` table with timestamps, IP addresses, and user IDs.

---

## 10. Verification & Artifact Inspection

- Implementation Plan: [cis_implementation_plan.md](file:///C:/Users/adity/.gemini/antigravity/brain/e4a7c46a-978f-4277-9b60-0f7b94c9740f/cis_implementation_plan.md)
- Seed Script: [scripts/seed_db.py](file:///d:/OG_Agentic/scripts/seed_db.py)
- Sample Syllabi: [data/sample_curriculum/](file:///d:/OG_Agentic/data/sample_curriculum/)
- Test Suite: [tests/](file:///d:/OG_Agentic/tests/)
- Launcher: [scripts/start_cis.ps1](file:///d:/OG_Agentic/scripts/start_cis.ps1)
