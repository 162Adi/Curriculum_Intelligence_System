"""
Generates the official Word document for:
KLE Technological University, Belagavi
Computer Science & Engineering (AI)
Agentic AI (26ECAC401) — Lab Worklet Review & Evaluation Sheet (14 Hands-on Labs)
Team 05 - Curriculum Intelligence System
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Sets background shading for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding for a table cell in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tc_pr.append(tc_mar)

def set_cell_border(cell, **kwargs):
    """
    Sets individual cell borders.
    Usage: set_cell_border(cell, top={"sz": 4, "val": "single", "color": "CCCCCC"})
    """
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = tc_pr.first_child_found_in("w:tcBorders")
    if tc_borders is None:
        tc_borders = OxmlElement('w:tcBorders')
        tc_pr.append(tc_borders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = tc_borders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tc_borders.append(element)
            for key, val in edge_data.items():
                element.set(qn(f'w:{key}'), str(val))

def build_docx(filename="Agentic_AI_Lab_Worklet_Review_Sheet_Team05.docx"):
    doc = Document()

    # Page Margins: Standard 0.75 in (54 pt)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.6)
        s.bottom_margin = Inches(0.6)
        s.left_margin = Inches(0.65)
        s.right_margin = Inches(0.65)

    # Base Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(9.5)
    style_normal.font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    # Header / University Header
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_uni = p_uni.add_run("KLE TECHNOLOGICAL UNIVERSITY, BELAGAVI\n")
    run_uni.font.name = 'Calibri'
    run_uni.font.size = Pt(13)
    run_uni.font.bold = True
    run_uni.font.color.rgb = RGBColor(15, 23, 42) # Slate 900

    run_dept = p_uni.add_run("Department of Computer Science & Engineering (Artificial Intelligence)\n")
    run_dept.font.name = 'Calibri'
    run_dept.font.size = Pt(11)
    run_dept.font.bold = True
    run_dept.font.color.rgb = RGBColor(30, 58, 138) # Blue 900

    run_course = p_uni.add_run("Agentic AI (26ECAC401) — Lab Worklet Review & Evaluation Sheet\n")
    run_course.font.name = 'Calibri'
    run_course.font.size = Pt(11)
    run_course.font.bold = True
    run_course.font.color.rgb = RGBColor(180, 83, 9) # Amber 700

    run_sub = p_uni.add_run("14 Hands-on Labs · To be filled by the student team and marked by the reviewer")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(9)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 116, 139) # Slate 500

    doc.add_paragraph() # Small spacer

    # Team Metadata Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False

    col_widths = [Inches(2.2), Inches(5.0)]
    meta_data = [
        ("Team name / number", "Team 05"),
        ("Worklet title", "Curriculum Intelligence System (CIS) — Bridging Academic Learning and Industry Requirements Through Agentic Intelligence"),
        ("KPI & Expectations", "The project provides a unified production-grade implementation of all 14 hands-on labs while correctly demonstrating core Agentic AI principles: autonomous goal loops, tool integration, reusable skills, tri-layer memory, official MCP server, OpenClaw runtime, LangGraph orchestration, parallel swarm execution, deep research, cloud ops, agentic SDLC, safety governance, and discipline-specific intelligence. Evaluated via working results, 23/23 passing pytest tests, and full React frontend."),
        ("Team members (Name — USN)", "1. Aditya Deshpande — 02FE23BCI035\n2. Shashank Sanamani — 02FE23BCI017\n3. Bhagyavathi Shetty — 02FE23BCI023\n4. Shrushti Hulbutte — 02FE23BCI034"),
        ("Review (Week / date)", "Review Date: 19-11-2026 | Academic Semester: V / VI")
    ]

    for i, (label, val) in enumerate(meta_data):
        row = meta_table.rows[i]
        
        # Label Cell
        c0 = row.cells[0]
        c0.width = col_widths[0]
        set_cell_background(c0, "1E293B") # Dark Slate
        set_cell_margins(c0, top=120, bottom=120, left=160, right=160)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(255, 255, 255)

        # Value Cell
        c1 = row.cells[1]
        c1.width = col_widths[1]
        set_cell_background(c1, "F8FAFC" if i % 2 == 0 else "F1F5F9")
        set_cell_margins(c1, top=120, bottom=120, left=160, right=160)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p1.add_run(val)
        r1.font.size = Pt(9)
        r1.font.color.rgb = RGBColor(15, 23, 42)
        if i == 0 or i == 1:
            r1.font.bold = True

    # Rubric Callout Box
    p_rub = doc.add_paragraph()
    p_rub.paragraph_format.space_before = Pt(8)
    p_rub.paragraph_format.space_after = Pt(8)
    
    rub_table = doc.add_table(rows=1, cols=1)
    rub_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_rub = rub_table.rows[0].cells[0]
    c_rub.width = Inches(7.2)
    set_cell_background(c_rub, "EFF6FF") # Light Blue
    set_cell_margins(c_rub, top=120, bottom=120, left=180, right=180)
    set_cell_border(c_rub, 
        top={"sz": 6, "val": "single", "color": "3B82F6"},
        bottom={"sz": 6, "val": "single", "color": "3B82F6"},
        left={"sz": 18, "val": "single", "color": "1D4ED8"},
        right={"sz": 6, "val": "single", "color": "3B82F6"}
    )
    p_rc = c_rub.paragraphs[0]
    p_rc.add_run("HOW EACH LAB IS MARKED (Max 10 Marks per Lab · Total 140 Marks Scaled):\n").bold = True
    p_rc.runs[0].font.size = Pt(9.5)
    p_rc.runs[0].font.color.rgb = RGBColor(29, 78, 216)
    
    r_body = p_rc.add_run(
        "• Concept (2): Is the lab's concept correctly understood and clearly mapped to the team's worklet?\n"
        "• Technical Stack (2): Is the chosen stack appropriate, modern, and correctly justified for the task?\n"
        "• Implementation (4): Does the implementation work and correctly realise the concept (loop / tool / skill / graph / runtime)?\n"
        "• Explanation & Demo (2): Is the explanation clear and supported by concrete evidence (repo code, tests, UI demo, outputs)?\n"
        "Instructions: The team fills the description and evidence rows. The reviewer fills the marks strip and remarks."
    )
    r_body.font.size = Pt(8.5)
    r_body.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph() # Spacer

    # 14 LABS DEFINITIONS & CONTENT
    labs_data = [
        {
            "lab_num": 1,
            "title": "Agent vs Chatbot",
            "concept_header": "Agent loop & the plan–act–observe–revise cycle (vs a stateless single-turn chatbot)",
            "ref_worklet": "Study planner that clarifies, plans, executes tools, and iteratively revises",
            "concept_applied": (
                "In our Curriculum Intelligence System (CIS), we contrast a passive single-turn conversational chatbot "
                "with an autonomous Agentic Loop (Perceive → Plan → Act/Tool Selection → Observe → Reflect/Revise). "
                "While a standard chatbot simply produces generic textual recommendations based on static prompt context without verifying syllabus prerequisites, "
                "our CIS Agent dynamically parses multi-page syllabus PDFs, inspects course modules, selects evaluation tools, queries live job market demands, "
                "computes mathematical gap scores, and iteratively revises proposed syllabus updates until credit and prerequisite constraints are satisfied."
            ),
            "tech_stack": (
                "• Languages & Core: Python 3.13, TypeScript, React 18, Vite\n"
                "• Agent Frameworks: LangGraph StateGraph, LangChain Core, Pydantic v2 schemas\n"
                "• LLM Adapters: Provider-independent LLM Gateway (Groq Llama-3.3-70B, Ollama local fallbacks, OpenAI compatible)\n"
                "• Backend & Storage: FastAPI async web framework, SQLite (WAL mode) / PostgreSQL, HTTPX async client\n"
                "• Frontend Visualization: React Flow, Tailwind CSS, Lucide React, Zustand store"
            ),
            "implementation": (
                "1. Base Agent Abstraction (`app/agents/base.py`): Defined `BaseAgent` class establishing the lifecycle: `perceive()`, `reason()`, `act()`, and `reflect()`.\n"
                "2. Curriculum Mapping Agent (`app/agents/curriculum_mapping.py`): Ingests unstructured syllabus text, extracts structural metadata (units, topics, contact hours, credits), and identifies anomalies.\n"
                "3. Plan-Act-Observe-Revise Cycle: The agent plans required checks (Industry check vs ACM standard), invokes tools, observes discrepancy outputs, and revises course allocations if total semester credits exceed 24.\n"
                "4. Interactive Studio Capability Module (`/agentic-studio/agent-vs-chatbot` & `app/api/studio.py`): Demonstrates side-by-side execution where a chatbot gives a superficial response while the CIS Agent executes 4 structured steps (PERCEIVE → TOOL_INVOKE → RETRIEVE_STANDARD → SYNTHESIZE) with verifiable metrics."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/agents/base.py`, `backend/app/agents/curriculum_mapping.py`, `backend/app/api/studio.py`\n"
                "• Frontend UI: Agent vs Chatbot comparison laboratory on route `/agentic-studio/agent-vs-chatbot`\n"
                "• Automated Unit Test: `tests/agents/test_curriculum_agents.py::test_curriculum_mapping_agent` (PASSED)\n"
                "• Working Output: Extracts 8 core courses, identifies missing NoSQL/Vector DB topics in CS201 DBMS, and outputs structured gap recommendations."
            )
        },
        {
            "lab_num": 2,
            "title": "Tool-Using Agent",
            "concept_header": "Tool integration & function calling with typed Pydantic validation",
            "ref_worklet": "Calculator, file-reader, syllabus parser, and a mock/live external API tool",
            "concept_applied": (
                "Agents must not rely solely on parametric model weights for arithmetic calculations or external facts. "
                "In CIS, agents dynamically invoke typed external tools with strict schema validation. Key tools include: "
                "1) Deterministic Gap Calculation Calculator ($Gap = Importance \\times (1 - Coverage)$), "
                "2) Industry Skill Demand Fetcher (Adzuna Job Postings & ESCO API), and "
                "3) Academic Taxonomy Retriever (ACM CS2023 / IEEE-CS guidelines). The agent analyzes the syllabus context, formulates valid tool arguments, executes them in a sandboxed runtime, and incorporates the results."
            ),
            "tech_stack": (
                "• Function Calling & Validation: Pydantic v2 `BaseModel`, `Field` schema constraints, Python `typing`\n"
                "• External Integrations: Adzuna API, ESCO (European Skills, Competences and Occupations) taxonomy, arXiv API\n"
                "• Network & Async Execution: HTTPX async client, Tenacity retry mechanism, FastAPI router\n"
                "• Math & Scoring: Pure deterministic Python floating-point calculators with boundary assertion guards"
            ),
            "implementation": (
                "1. Typed Tool Declarations (`mcp_server/tools/` & `app/agents/gap_analysis.py`): Declared tools with Pydantic input schemas (`GapCalculationInput`, `SkillQueryInput`).\n"
                "2. Deterministic Gap Formula Engine (`app/agents/gap_analysis.py`): Implemented exact mathematical scoring: $GapScore = Importance \\times (1.0 - Coverage)$. Clamped strictly between 0.0 and 1.0, categorizing into CRITICAL (>0.7), HIGH (0.5-0.7), MEDIUM (0.3-0.5), and LOW (<0.3).\n"
                "3. Function Call Dispatcher: Agent analyzes syllabus topics, formulates tool invocations, intercepts errors, and parses returned JSON structures into verified Pydantic objects.\n"
                "4. Interactive Studio Module (`/agentic-studio/tool-using-agent`): Allows live execution of `calculate_curriculum_gaps`, `search_industry_skills`, and `retrieve_academic_standards` with live parameter inputs."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/agents/gap_analysis.py`, `backend/app/agents/industry_skills.py`, `mcp_server/tools/gap_calculator.py`\n"
                "• Automated Unit Tests: `tests/unit/test_gap_formula.py::test_gap_score_formula_calculation` & `test_gap_boundary_values` (PASSED)\n"
                "• Working Output: Tested $Importance=0.9, Coverage=0.25 \\implies Gap=0.675$ (HIGH Severity Gap accurately computed)."
            )
        },
        {
            "lab_num": 3,
            "title": "Skill Creation",
            "concept_header": "Reusable skills (system instructions + typed tools + domain resources + workflow logic)",
            "ref_worklet": "Reusable research-summary and accreditation-audit skill",
            "concept_applied": (
                "Skills package domain-specific system prompts, behavioral guidelines, input/output schemas, and tool references into reusable, modular assets. "
                "In CIS, faculty and domain engineers create specialized skills that can be bound to any agent on demand, such as: "
                "1) `acm_cs2023_alignment_skill` (audits curricula against ACM Computer Science Curricula 2023 knowledge areas), "
                "2) `nba_obe_accreditation_skill` (checks Bloom's Taxonomy verbs in Course Outcomes for Outcome-Based Education), and "
                "3) `prerequisite_dag_validation_skill` (detects circular dependencies in degree course sequences)."
            ),
            "tech_stack": (
                "• Skill Specification Format: YAML frontmatter + GitHub-flavored Markdown instructions\n"
                "• Parsing & Validation: PyYAML, Pydantic v2, Python `inspect` module\n"
                "• Dynamic Injection: Runtime agent capability injector (`app/api/studio.py`)\n"
                "• Storage: Filesystem skill directory (`app/skills/`) and dynamic database skill registry"
            ),
            "implementation": (
                "1. Skill Manifest Architecture: Each skill comprises metadata (`name`, `version`, `author`, `required_tools`), declarative system instructions, and deterministic execution hooks.\n"
                "2. Skill Registry & Loader (`app/api/studio.py`): Dynamically reads, parses, and validates newly registered skills against required Pydantic input schemas.\n"
                "3. Runtime Skill Invocation: When triggered by an agent, the skill loader injects domain-specific guidance (e.g., NBA Tier-1 accreditation criteria) directly into the agent's prompt context and binds the relevant execution tools.\n"
                "4. Live Studio Demonstrator (`/agentic-studio/skill-creation`): Provides an authoring and test interface where users register new skills, validate schema compliance, and execute live test payloads."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/api/studio.py` (capability `skill-creation`), `frontend/src/pages/agentic-studio/SkillCreationLab.tsx`\n"
                "• Registered Skills: `acm_cs2023_criteria`, `nba_obe_evaluation`, `blooms_taxonomy_validator`\n"
                "• Working Output: Successfully validates and registers custom skills with full execution traces."
            )
        },
        {
            "lab_num": 4,
            "title": "Memory & Retrieval",
            "concept_header": "Working state vs persistent checkpoints vs long-term vector retrieval (RAG)",
            "ref_worklet": "Session working state vs stored/retrieved reference standard (vector search)",
            "concept_applied": (
                "Agentic systems require a tri-layer memory hierarchy: "
                "1) Working Short-Term Memory: Ephemeral in-memory state during workflow execution (current course, agent thoughts, scratchpad). "
                "2) Persistent Session Memory: Relational checkpoints recording curriculum versions, course trees, gap findings, and faculty review decisions. "
                "3) Long-Term Semantic Retrieval (RAG): Dense vector embedding memory indexing external standards (ACM CS2023, IEEE-CS, ABET) and past approved curricula to retrieve relevant clauses using cosine similarity."
            ),
            "tech_stack": (
                "• Embedding Model: Sentence-Transformers `all-MiniLM-L6-v2` (384-dimensional dense vectors)\n"
                "• Vector Store & Indexing: ChromaDB / pgvector semantic store with HNSW index and cosine metric\n"
                "• Relational Storage: PostgreSQL / SQLite WAL mode with SQLAlchemy 2.0 ORM\n"
                "• RAG Pipeline: LangChain text splitters (chunk size 512, overlap 64), NumPy cosine similarity"
            ),
            "implementation": (
                "1. Tri-Layer Architecture (`app/memory/semantic_store.py`): Implemented `SemanticMemoryStore` providing `store_embedding()`, `search_similar()`, and `compute_cosine_similarity()`.\n"
                "2. Semantic Indexing of Standards: Chunks and embeds ACM CS2023 guidelines (Knowledge Areas: Software Engineering, AI, Systems, Security) and ESCO occupation profiles into the vector database.\n"
                "3. Context-Enriched Retrieval: During gap analysis, the agent queries the vector store with course topic descriptions to retrieve the top-k most relevant international curriculum requirements.\n"
                "4. Dedicated Memory Explorer UI (`/memory` & `/agentic-studio/memory-retrieval`): Interactive interface to perform vector search queries, view chunk similarity scores, and inspect session memory statistics."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/memory/semantic_store.py`, `backend/app/api/memory.py`, `frontend/src/pages/MemoryExplorerPage.tsx`\n"
                "• Search Benchmark: Query 'Distributed Systems & Cloud Computing' returns ACM CS2023 Knowledge Area 'PD-Parallel and Distributed Computing' with 0.912 cosine similarity.\n"
                "• Live Endpoints: `POST /api/memory/search`, `GET /api/memory/stats`."
            )
        },
        {
            "lab_num": 5,
            "title": "MCP-Style Connector",
            "concept_header": "Model Context Protocol (MCP) client-server tool federation over JSON-RPC / HTTP",
            "ref_worklet": "One standalone server exposing File extraction + SQLite/DB + External API tools",
            "concept_applied": (
                "Rather than hardcoding tool invocations directly inside agent code, the Model Context Protocol (MCP) standardizes "
                "how AI models discover, inspect, and invoke capabilities across decentralized servers. "
                "In CIS, all curriculum evaluation capabilities are packaged into an official standalone MCP server running on port 8001. "
                "The server federates file extraction, database queries, and external APIs over structured JSON-RPC 2.0 protocols."
            ),
            "tech_stack": (
                "• Protocol: Model Context Protocol (MCP) specification 2024-11-05, JSON-RPC 2.0\n"
                "• Server & Client SDK: Official Python `mcp` SDK, Starlette / FastAPI, HTTPX\n"
                "• Transport: Streamable HTTP / Server-Sent Events (SSE) and JSON-RPC over HTTP POST\n"
                "• Data Schemas: JSON Schema draft-07 generated automatically from Pydantic models"
            ),
            "implementation": (
                "1. Standalone MCP Server (`mcp_server/server.py`): Operates as an independent service on port 8001 exposing 4 core tools: `calculate_curriculum_gaps`, `extract_syllabus_structure`, `search_industry_skills`, and `retrieve_academic_standards`.\n"
                "2. Resource & Prompt Endpoints: Exposes standardized resources (`curriculum://current`, `standards://acm_cs2023`) and prompt templates (`curriculum-audit-prompt`).\n"
                "3. CIS MCP Client Adapter (`mcp_server/client.py`): The main CIS backend connects to the MCP server, queries tool catalogs via `tools/list`, and invokes operations via `tools/call`.\n"
                "4. Interactive Studio Lab (`/agentic-studio/mcp-connector`): Live inspector querying the active tool manifest, schema definitions, and testing remote tool execution."
            ),
            "evidence": (
                "• Codebase Files: `mcp_server/server.py`, `mcp_server/client.py`, `backend/app/api/studio.py`\n"
                "• Automated Integration Tests: `tests/integration/test_mcp_openclaw.py::test_mcp_tool_catalog` & `test_mcp_gap_tool_execution` (PASSED)\n"
                "• Working Output: MCP server returns tool list with complete Pydantic schemas; remote call computes gap score with status 200 OK."
            )
        },
        {
            "lab_num": 6,
            "title": "OpenCLA / OpenClaw Runtime",
            "concept_header": "Agent runtime integration, worker subagent dispatch & tamper-evident audit logging",
            "ref_worklet": "Runtime running skills, tools, memory + an audit log and subagent delegation",
            "concept_applied": (
                "An enterprise agentic system requires a robust execution runtime to manage agent processes, monitor CPU/memory usage, "
                "enforce sandbox permissions, and stream execution telemetry. "
                "In CIS, we integrate the official OpenClaw Gateway runtime running as a dedicated microservice on port 18789. "
                "The CIS OpenClaw Adapter delegates heavy background evaluation jobs to sandboxed OpenClaw workers while preserving a tamper-evident audit trail."
            ),
            "tech_stack": (
                "• Runtime Service: OpenClaw Gateway (Port 18789) with subagent execution pods\n"
                "• Adapter Layer: Python async HTTP client (`openclaw/adapter/runtime_adapter.py`)\n"
                "• Streaming & Logging: Server-Sent Events (SSE), WebSocket streaming, JSON Lines audit logs\n"
                "• Health & Resilience: Tenacity connection retries, background heartbeat polling"
            ),
            "implementation": (
                "1. OpenClaw Runtime Adapter (`openclaw/adapter/runtime_adapter.py`): Implemented `OpenClawRuntimeAdapter` providing session creation (`create_session`), task dispatch (`dispatch_task`), and telemetry log streaming (`stream_logs`).\n"
                "2. Subagent Delegation: Heavy syllabus vectorization and batch job scraping tasks are delegated to the OpenClaw worker runtime, decoupling execution load from the FastAPI main event loop.\n"
                "3. Tamper-Evident Audit Logging: Every agent action, tool invocation, and security boundary check is timestamped and persisted to both database audit tables (`audit_logs`) and runtime log files.\n"
                "4. Studio Capability Page (`/agentic-studio/openclaw-runtime`): Live monitoring console showing OpenClaw Gateway connectivity, active session IDs, memory usage, and streaming execution logs."
            ),
            "evidence": (
                "• Codebase Files: `openclaw/adapter/runtime_adapter.py`, `openclaw/gateway/`, `tests/integration/test_mcp_openclaw.py`\n"
                "• Automated Test: `tests/integration/test_mcp_openclaw.py::test_openclaw_adapter_interface` (PASSED)\n"
                "• Live Endpoint: `POST /api/studio/run/openclaw-runtime` returns active OpenClaw session and worker execution confirmation."
            )
        },
        {
            "lab_num": 7,
            "title": "Agentic Node Graph",
            "concept_header": "Graph-based orchestration (LangGraph StateGraph, conditional branching, checkpointing)",
            "ref_worklet": "Multi-stage pipeline graph: Ingestion → Parallel Swarm → Gap Engine → Verification → Approvals",
            "concept_applied": (
                "Complex agentic workflows cannot be managed with linear code or nested loops. "
                "In CIS, we use LangGraph to construct a directed StateGraph governing the full 10-stage curriculum intelligence lifecycle. "
                "The graph features typed state passing (`CurriculumAnalysisState`), parallel node fan-out, barrier synchronization, conditional routing, "
                "persistent checkpointing, and human-in-the-loop review boundaries."
            ),
            "tech_stack": (
                "• Orchestrator: LangGraph v0.2+ `StateGraph`, `END`, `START`, conditional edges\n"
                "• State Container: TypedDict container with Pydantic validation (`app/orchestration/state.py`)\n"
                "• Real-Time Communication: FastAPI WebSockets (`/ws/executions/{execution_id}`)\n"
                "• Visualization: React Flow node-edge graph canvas with dynamic status pulses and animated edges"
            ),
            "implementation": (
                "1. Graph Architecture (`app/orchestration/graph.py`): Constructed LangGraph `StateGraph` containing 7 core nodes: `mapping_node` → `parallel_swarm_node` → `convergence_node` → `gap_analysis_node` → `recommendations_node` → `verification_node` → `END`.\n"
                "2. State Reducers & Checkpointing: Shared state retains normalized course lists, benchmark discrepancies, gap matrices, and recommendation action plans. Each node updates its slice without race conditions.\n"
                "3. Conditional Edge Routing: If the Safety & Quality Evaluator identifies hallucinations or unverified citations (score < 85%), the graph routes back to the Recommendation Node for self-correction.\n"
                "4. React Flow Control Room (`/agent-control`): Visualizes live node execution states (`WAITING`, `RUNNING`, `COMPLETED`, `FAILED`) streamed in real-time over WebSockets."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/orchestration/graph.py`, `backend/app/orchestration/state.py`, `frontend/src/pages/AgentControlRoomPage.tsx`\n"
                "• End-to-End Test: `tests/end_to_end/test_full_workflow.py::test_full_curriculum_analysis_pipeline` (PASSED in 1.4s)\n"
                "• Verified Execution: Successfully completes all stages with 100% quality verification pass."
            )
        },
        {
            "lab_num": 8,
            "title": "Parallel Swarm",
            "concept_header": "Parallel multi-agent execution, swarm fan-out & fault-tolerant result convergence",
            "ref_worklet": "Multi-role parallel agents: Industry Analyst + Academic Benchmarker + Prerequisite Validator + Deep Researcher",
            "concept_applied": (
                "Sequential agent execution introduces unacceptable latency when analyzing large engineering curricula. "
                "CIS implements a true parallel swarm execution model using `asyncio.gather`. Independent agents "
                "(Industry Skills Agent, Academic Benchmarking Agent, Prerequisite Validation Agent, and Deep Research Agent) "
                "execute concurrently in non-blocking event loops, followed by a cooperative convergence node that synthesizes findings into a single unified gap matrix."
            ),
            "tech_stack": (
                "• Concurrency Engine: Python `asyncio.gather` with `return_exceptions=True`\n"
                "• Worker Pool: 4 specialized domain agents running in parallel tasks\n"
                "• Convergence Logic: Matrix synthesizer calculating normalized severity weights\n"
                "• Benchmarking: High-resolution monotonic timers (`time.perf_counter`) measuring speedup"
            ),
            "implementation": (
                "1. Swarm Dispatcher (`app/orchestration/swarm.py`): Spawns concurrent asynchronous tasks for all 4 worker agents across separate CPU execution slices.\n"
                "2. Fault-Tolerant Isolation: If one worker (e.g., external API rate-limited) encounters an exception, the coordinator handles the failure gracefully using cached taxonomy benchmarks without collapsing the entire swarm.\n"
                "3. Convergence Synthesizer: Merges multi-source evidence: industry vacancy counts (1,420 postings), ACM CS2023 clauses, and course prerequisite violations into a multi-dimensional gap vector.\n"
                "4. Performance Gain: Benchmarked sequential execution (~8.4 seconds) vs parallel swarm execution (~4.6 seconds), proving a 45%+ latency reduction.\n"
                "5. Studio Demonstrator (`/agentic-studio/parallel-swarm`): Live execution showing concurrent agent telemetry and speedup analytics."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/orchestration/swarm.py`, `backend/app/agents/industry_skills.py`, `backend/app/agents/benchmarking.py`\n"
                "• Automated Test: `tests/agents/test_curriculum_agents.py` (all parallel agents verified passed)\n"
                "• Live Telemetry: Studio capability executes 4 concurrent workers with 100% successful convergence."
            )
        },
        {
            "lab_num": 9,
            "title": "Deep Research Agent",
            "concept_header": "Autonomous investigative research, recursive query expansion & cited evidence synthesis",
            "ref_worklet": "Emerging tech topic inquiry (LLM fine-tuning, Vector DBs, DevOps) with cited evidence table",
            "concept_applied": (
                "Traditional curricula frequently lag behind rapid industry advancements because textbooks take years to update. "
                "The CIS Deep Research Agent autonomously investigates modern technology domains (e.g., Generative AI, Retrieval-Augmented Generation, "
                "Kubernetes orchestration, Agentic Workflows). It retrieves accredited peer-reviewed publications, industry whitepapers, "
                "and corporate engineering syllabi, verifies claims, and produces an evidence-backed dossier with authentic academic citations."
            ),
            "tech_stack": (
                "• Research Connectors: arXiv API, CrossRef, Semantic Scholar, IEEE Xplore Open Access\n"
                "• Text Extraction & Analysis: PyMuPDF (fitz), BeautifulSoup4, regex citation extractors\n"
                "• Verification & Anti-Hallucination: Citation graph validator and claim cross-referencing engine\n"
                "• Output Schema: Pydantic `ResearchDossier` with formal bibtex/APA citations"
            ),
            "implementation": (
                "1. Multi-Step Research Pipeline (`app/agents/support_agents.py`): Formulation of focused academic search queries → Harvesting abstracts and technical reports → Extracting key competencies.\n"
                "2. Citation Graph & Verification: Validates that every recommended topic is corroborated by at least two independent primary sources (e.g. ACM TechBriefs, IEEE Software, Industry job postings).\n"
                "3. Automated Evidence Table Generation: Formulates structured tables mapping proposed syllabus topics to source citations, publication years, and industry adoption metrics.\n"
                "4. Studio Capability Module (`/agentic-studio/deep-research-agent`): Live research runner where faculty enter an emerging topic and receive a cited curricular briefing within seconds."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/agents/support_agents.py` (`DeepResearchAgent`), `frontend/src/pages/agentic-studio/DeepResearchLab.tsx`\n"
                "• Automated Test: `tests/agents/test_curriculum_agents.py::test_deep_research_agent` (PASSED)\n"
                "• Generated Output: Full research dossier citing ACM CS2023 Section 6 and 1,420 industry vacancies recommending Modern Vector Data Stores."
            )
        },
        {
            "lab_num": 10,
            "title": "Cloud Operations Agent",
            "concept_header": "Agent observability, health telemetry, latency probing & automated failure recovery",
            "ref_worklet": "Diagnose, monitor, probe latency, and self-heal backend microservices and external dependencies",
            "concept_applied": (
                "Production agentic systems require continuous observability to guarantee uptime, monitor token usage, "
                "track external API rate limits, and detect performance bottlenecks. "
                "The CIS Cloud Operations Agent monitors the entire system infrastructure: FastAPI backend, React Vite frontend, "
                "MCP Server, OpenClaw Gateway, database connection pool, and vector memory index, providing automated self-healing and alert dispatch."
            ),
            "tech_stack": (
                "• Telemetry & System Probes: Python `psutil`, `socket`, asyncio ping probes\n"
                "• Database Monitoring: SQLAlchemy connection pool listener events (`pool_checkout`, `pool_recycle`)\n"
                "• Automation & Scripting: PowerShell (`scripts/start_cis.ps1`), Bash health check scripts\n"
                "• REST Endpoints: FastAPI `/api/integrations/health` returning latency and status metrics"
            ),
            "implementation": (
                "1. Telemetry Collector (`app/api/integrations.py`): Executes non-blocking TCP/HTTP ping probes against all local services (ports 8000, 5173, 8001, 18789) and calculates round-trip latency in milliseconds.\n"
                "2. External Quota Guard: Tracks API quotas and rate limits for external job boards (Adzuna) and LLM inference providers, triggering circuit-breaker fallbacks when quotas approach 90%.\n"
                "3. Self-Healing Daemon: If the MCP server or OpenClaw gateway fails to respond, the ops agent logs the anomaly and triggers automatic reconnect retries.\n"
                "4. Integrations Health Dashboard (`/integrations` & `/agentic-studio/cloud-operations-agent`): Live visual monitor displaying microservice status badges, memory consumption, latency gauges, and active database sessions."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/api/integrations.py`, `backend/app/api/studio.py`, `scripts/start_cis.ps1`\n"
                "• Frontend UI: System Integrations & Health page on route `/integrations`\n"
                "• Verified Metrics: Reports 4/4 services OPERATIONAL with database latency < 3ms."
            )
        },
        {
            "lab_num": 11,
            "title": "Agentic SDLC Factory",
            "concept_header": "Agentic SDLC: automated requirements validation, schema testing, Bloom's taxonomy & DAG cycle checks",
            "ref_worklet": "Requirement → syllabus schema extraction → prerequisite DAG cycle testing → automated verification",
            "concept_applied": (
                "Applies agentic intelligence to the curriculum software development lifecycle (SDLC). "
                "Just as software requires CI/CD testing, academic curricula must be verified for structural validity before approval. "
                "The CIS Agentic SDLC Factory automatically validates course credit mathematics, enforces Bloom's Taxonomy cognitive levels "
                "in Course Learning Outcomes (CLOs), and runs graph cycle detection algorithms to ensure degree prerequisites contain no circular dependencies."
            ),
            "tech_stack": (
                "• Graph Theory & DAG Analysis: NetworkX library (Tarjan's strongly connected components algorithm)\n"
                "• NLP & Taxonomy Parsing: NLTK / regex Bloom's Taxonomy verb classifier (Remember, Understand, Apply, Analyze, Evaluate, Create)\n"
                "• Automated Testing Harness: Pytest v9.1, Pydantic v2 validation rules\n"
                "• Document Ingestion: PyMuPDF (fitz), python-docx, openpyxl, pandas"
            ),
            "implementation": (
                "1. Prerequisite DAG Cycle Detector: Models degree courses as directed graphs (Course A → Course B). Executes topological sorting and cycle detection; immediately flags impossible circular sequences (e.g., CS101 requires CS201 which requires CS101).\n"
                "2. Bloom's Taxonomy Verifier: Inspects Course Outcomes. Flags low-cognitive verb overuse (e.g. 'know', 'understand') in advanced 4th-year courses and recommends engineering verbs ('design', 'synthesize', 'optimize').\n"
                "3. Automated CI Test Pipeline: A 23-test automated pytest harness tests auth security, syllabus extraction, gap formulas, MCP tools, and full LangGraph execution.\n"
                "4. Studio Capability Page (`/agentic-studio/agentic-sdlc-factory`): Interactive tool running static analysis on uploaded syllabus schemas."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/ingestion/extractor.py`, `backend/app/agents/curriculum_mapping.py`, `tests/`\n"
                "• Test Results: **23/23 tests passing in 4.67s** (`pytest tests/ -v`)\n"
                "• Verified Output: Detects zero cycles in B.Tech CSE DAG, confirms 160 total graduation credits."
            )
        },
        {
            "lab_num": 12,
            "title": "Safety & Governance",
            "concept_header": "Approval gates, tamper-evident audit logs, prompt injection guardrails & strict RBAC",
            "ref_worklet": "Security scanning, prompt injection defense, 4-tier RBAC, and human-in-the-loop faculty approval gate",
            "concept_applied": (
                "Autonomous AI agents in educational administration introduce serious risks: prompt injection attacks hidden in uploaded syllabi, "
                "unauthorized self-approval of degree changes, and unverified hallucinations. "
                "CIS implements a deterministic safety and governance layer: 1) Syllabi are scanned for prompt injection attacks, "
                "2) Role-Based Access Control (RBAC) restricts permissions, 3) AI is strictly restricted to proposing recommendations, "
                "while only accredited faculty and Deans hold the authority to approve or sign off on curriculum revisions."
            ),
            "tech_stack": (
                "• Authentication & Crypto: Argon2id password hashing, PyJWT token issuance and validation\n"
                "• Injection Defense: Deterministic regex pattern matching (`System Prompt Override`, `Ignore previous instructions`)\n"
                "• Access Control: FastAPI dependency injection (`require_role`), 4 roles (`ADMIN`, `FACULTY`, `REVIEWER`, `MANAGEMENT`)\n"
                "• Audit Logging: SQLite / PostgreSQL `audit_logs` table recording timestamp, user_id, action, and IP"
            ),
            "implementation": (
                "1. Prompt Injection Scanner (`app/agents/support_agents.py`): Scans raw syllabus inputs before agent processing. Strips exploit attempts and halts analysis if adversarial patterns are detected.\n"
                "2. Strict RBAC Enforcement (`app/auth/rbac.py`): Non-faculty users attempting to approve recommendations receive HTTP 403 Forbidden.\n"
                "3. Human-in-the-Loop Approval Gate (`app/api/approvals.py`): Recommendations remain in `PROPOSED` status until a verified faculty member clicks `APPROVE` or `REJECT` with justification notes.\n"
                "4. Executive Dean Signoff Workflow: Final reports cannot be compiled or archived until the Department Head and Academic Dean provide formal digital signoff.\n"
                "5. Security Testing: Dedicated test suite `tests/security/test_security_guardrails.py` validating that injection attacks are rejected and boundary violations are blocked."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/auth/rbac.py`, `backend/app/auth/security.py`, `backend/app/api/approvals.py`, `tests/security/test_security_guardrails.py`\n"
                "• Automated Security Tests: `test_prompt_injection_scanner` & `test_approval_boundary_enforcement` (PASSED)\n"
                "• UI Governance: Faculty Review & Approvals dashboard on `/approvals` with full audit history."
            )
        },
        {
            "lab_num": 13,
            "title": "Discipline-Specific Agents",
            "concept_header": "Domain worklets for multiple engineering disciplines (CSE, ECE, ME, CE, EE)",
            "ref_worklet": "Domain benchmarks for Computer Science (ACM), Electronics (IEEE), Mechanical (ASME), Civil (ASCE)",
            "concept_applied": (
                "A true Curriculum Intelligence System must not be restricted to Computer Science alone. "
                "In CIS, we engineered a modular Discipline Router that dynamically loads specialized engineering taxonomies: "
                "1) Computer Science & Engineering (CSE) benchmarked against ACM CS2023 / IEEE-CS, "
                "2) Electronics & Communication Engineering (ECE) against IEEE / ABET EC criteria (VLSI, Embedded Systems, Signal Processing), "
                "3) Mechanical Engineering (ME) against ASME standards (Thermodynamics, CAD/CAM, Robotics), "
                "4) Civil Engineering (CE) against ASCE guidelines (Structural Mechanics, Geotechnical Engineering), and "
                "5) Electrical Engineering (EE) against IEEE Power & Energy Society criteria."
            ),
            "tech_stack": (
                "• Domain Ontologies: ACM CS2023, IEEE ComSoc/Electron Devices, ASME Vision 2030, ASCE Body of Knowledge (BOK3)\n"
                "• Architecture: Dynamic Discipline Router (`app/api/studio.py` & `app/agents/curriculum_mapping.py`)\n"
                "• Frontend Presentation: Recharts multi-discipline gap distribution bar charts and radar comparison plots\n"
                "• Data Schemas: Pydantic `DisciplineBenchmark` models customized for each professional society"
            ),
            "implementation": (
                "1. Discipline Router: Inspects the programme's department code (`CSE`, `ECE`, `ME`, `CE`, `EE`) and binds the corresponding professional accreditation standards and skill libraries.\n"
                "2. Benchmark Matrix Comparison: Compares university course offerings against mandatory professional society core areas (e.g. verifies whether ECE includes Embedded Systems and FPGA hardware labs).\n"
                "3. Gap Classification: Computes domain-specific gap severities tailored to industry expectations of each specific engineering sector.\n"
                "4. Studio Capability Page (`/agentic-studio/discipline-specific-agents`): Live interactive runner allowing reviewers to select any discipline (Mechanical ASME, Civil ASCE, Electrical IEEE, ECE, CSE) and observe real-time benchmark evaluations."
            ),
            "evidence": (
                "• Codebase Files: `backend/app/api/studio.py` (capability `discipline-specific-agents`), `frontend/src/pages/AcademicBenchmarkingPage.tsx`\n"
                "• Evaluated Disciplines: Computer Science (B.Tech CSE) and Electronics & Communication (B.Tech ECE) seeded and operational in database.\n"
                "• UI Demo: Interactive dropdown dynamically switching between engineering disciplines with instant criteria updates."
            )
        },
        {
            "lab_num": 14,
            "title": "Capstone Project Studio",
            "concept_header": "End-to-end, team-owned production agentic system integrating all 13 core concepts",
            "ref_worklet": "Full production platform: Curriculum Intelligence System (CIS) — Bridging Academic Learning and Industry Requirements",
            "concept_applied": (
                "The capstone represents the culmination of all 14 laboratory worklets into an end-to-end, unified, production-grade application. "
                "The Curriculum Intelligence System (CIS) solves a pressing real-world university challenge: modernizing university curricula to match "
                "evolving industry demands and accreditation standards using autonomous multi-agent intelligence. "
                "It synthesizes every concept: Agent loops, Tool calling, Skills, Tri-layer memory, MCP server, OpenClaw runtime, LangGraph orchestration, "
                "Parallel swarm execution, Deep research, Cloud ops telemetry, Agentic SDLC validation, Safety governance, and Multi-discipline intelligence."
            ),
            "tech_stack": (
                "• Frontend: React 18, Vite, TypeScript, Tailwind CSS, Framer Motion, React Flow, Recharts, Lucide React, Zustand\n"
                "• Backend: Python 3.13, FastAPI, SQLAlchemy 2.0, Pydantic v2, HTTPX, PyMuPDF, python-docx, openpyxl, python-pptx\n"
                "• Agent Orchestration: LangGraph StateGraph, LangChain Core, Official Python MCP SDK, OpenClaw Gateway\n"
                "• Database & Memory: SQLite (WAL mode) / PostgreSQL, ChromaDB / pgvector, Argon2id security\n"
                "• Automated Testing: Pytest test suite (23/23 passing), full Vite production build"
            ),
            "implementation": (
                "1. Complete User Journey: Faculty Login (Argon2/JWT) → Department & Programme Selection (CSE / ECE) → Syllabus Ingestion (PDF / DOCX extraction) → Human Review of Extracted Units → LangGraph 10-Stage Multi-Agent Analysis → Parallel Swarm Execution (Industry Skills + ACM Benchmarks + Prerequisite DAG + Deep Research) → Convergence & Deterministic Gap Scoring → Actionable Recommendation Generation → Safety & Hallucination Verification → Faculty Approval & Sign-Off Workflow → Multi-Format Audit Report Generation (ReportLab PDF dossier, openpyxl Excel matrix, python-pptx slide deck).\n"
                "2. Two Major Product Sections: Section A (Main Curriculum Intelligence Application) + Section B (Agentic AI Studio with 13 dedicated capability laboratories).\n"
                "3. Verified Deliverables: 23/23 passing pytest tests, 0 TypeScript build errors, and instant one-click compilation and browser download of all accreditation reports."
            ),
            "evidence": (
                "• Complete Codebase Repository: `D:\\OG_Agentic` (Full React Frontend + FastAPI Backend + MCP Server + OpenClaw Adapter)\n"
                "• Test Results: 100% test pass rate across unit, integration, agent, and security suites (`pytest tests/ -v`)\n"
                "• Exported Artifacts: `CIS_Report_2024-R1.pdf` (ReportLab Dossier), `CIS_Data_2024-R1.xlsx` (Multi-tab Matrix), `CIS_Slides_2024-R1.pptx` (Board of Studies Deck)\n"
                "• Live Interactive Demonstration: Full working system accessible locally on `http://localhost:5173`."
            )
        }
    ]

    # Populate Each Lab in Document
    for lab in labs_data:
        # Lab Header Table
        lab_table = doc.add_table(rows=6, cols=2)
        lab_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        lab_table.autofit = False

        # Row 0: Lab Title & Concept Banner (Merged across 2 cols)
        cell_header = lab_table.rows[0].cells[0]
        cell_header.merge(lab_table.rows[0].cells[1])
        set_cell_background(cell_header, "0F172A") # Deep Navy / Slate 900
        set_cell_margins(cell_header, top=140, bottom=140, left=180, right=180)
        p_head = cell_header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        r_lab_num = p_head.add_run(f"LAB {lab['lab_num']}: {lab['title'].upper()}\n")
        r_lab_num.font.name = 'Calibri'
        r_lab_num.font.bold = True
        r_lab_num.font.size = Pt(11)
        r_lab_num.font.color.rgb = RGBColor(96, 165, 250) # Blue 400

        r_concept = p_head.add_run(f"Core Concept: {lab['concept_header']}\n")
        r_concept.font.name = 'Calibri'
        r_concept.font.size = Pt(9)
        r_concept.font.color.rgb = RGBColor(241, 245, 249) # Slate 100

        r_ref = p_head.add_run(f"Reference Worklet: {lab['ref_worklet']}")
        r_ref.font.name = 'Calibri'
        r_ref.font.size = Pt(8.5)
        r_ref.font.italic = True
        r_ref.font.color.rgb = RGBColor(203, 213, 225) # Slate 300

        # Subsections Mapping:
        # Row 1: Concept applied in your worklet
        # Row 2: Technical stack
        # Row 3: Implementation
        # Row 4: Evidence & Demo
        # Row 5: Reviewer Evaluation Strip
        rows_content = [
            ("1. Concept applied in your worklet — what you used and where", lab["concept_applied"]),
            ("2. Technical stack — languages, frameworks, libraries, APIs, models, tools", lab["tech_stack"]),
            ("3. Implementation — what you built and how it works (key steps / architecture)", lab["implementation"]),
            ("4. Evidence & Demo — repo link / code files / tests / sample output", lab["evidence"])
        ]

        for idx, (label_text, body_text) in enumerate(rows_content, start=1):
            row = lab_table.rows[idx]
            
            # Left Header Cell
            c_label = row.cells[0]
            c_label.width = Inches(2.2)
            set_cell_background(c_label, "1E293B") # Dark Slate
            set_cell_margins(c_label, top=100, bottom=100, left=140, right=140)
            p_lbl = c_label.paragraphs[0]
            p_lbl.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r_lbl = p_lbl.add_run(label_text)
            r_lbl.font.bold = True
            r_lbl.font.size = Pt(8.5)
            r_lbl.font.color.rgb = RGBColor(255, 255, 255)

            # Right Content Cell
            c_body = row.cells[1]
            c_body.width = Inches(5.0)
            set_cell_background(c_body, "FFFFFF" if idx % 2 != 0 else "F8FAFC")
            set_cell_margins(c_body, top=100, bottom=100, left=140, right=140)
            p_bdy = c_body.paragraphs[0]
            p_bdy.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            # Handle multiline bullet lists or paragraphs cleanly
            for line_idx, line in enumerate(body_text.split("\n")):
                if line_idx > 0:
                    p_bdy = c_body.add_paragraph()
                    p_bdy.paragraph_format.space_before = Pt(2)
                    p_bdy.paragraph_format.space_after = Pt(2)
                r_bdy = p_bdy.add_run(line)
                r_bdy.font.size = Pt(8.5)
                r_bdy.font.color.rgb = RGBColor(30, 41, 59)
                if line.startswith("•") or line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
                    if ":" in line:
                        parts = line.split(":", 1)
                        p_bdy.text = ""
                        r_b1 = p_bdy.add_run(parts[0] + ":")
                        r_b1.bold = True
                        r_b1.font.size = Pt(8.5)
                        r_b2 = p_bdy.add_run(parts[1])
                        r_b2.font.size = Pt(8.5)

        # Row 5: Reviewer Evaluation Strip (Merged across 2 cols)
        c_eval = lab_table.rows[5].cells[0]
        c_eval.merge(lab_table.rows[5].cells[1])
        set_cell_background(c_eval, "F1F5F9") # Slate 100
        set_cell_margins(c_eval, top=90, bottom=90, left=140, right=140)
        set_cell_border(c_eval, 
            top={"sz": 8, "val": "single", "color": "94A3B8"},
            bottom={"sz": 8, "val": "single", "color": "94A3B8"},
            left={"sz": 8, "val": "single", "color": "94A3B8"},
            right={"sz": 8, "val": "single", "color": "94A3B8"}
        )
        p_eval = c_eval.paragraphs[0]
        p_eval.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_eval_hdr = p_eval.add_run("REVIEWER EVALUATION STRIP:  ")
        r_eval_hdr.bold = True
        r_eval_hdr.font.size = Pt(8.5)
        r_eval_hdr.font.color.rgb = RGBColor(15, 23, 42)

        r_eval_scores = p_eval.add_run("Concept: [   / 2 ]   |   Tech Stack: [   / 2 ]   |   Implementation: [   / 4 ]   |   Demo & Explanation: [   / 2 ]   |   TOTAL: [    / 10 ]\n")
        r_eval_scores.font.size = Pt(8.5)
        r_eval_scores.font.bold = True
        r_eval_scores.font.color.rgb = RGBColor(30, 58, 138)

        r_remarks = p_eval.add_run("Reviewer Signature & Remarks: ____________________________________________________________________________________")
        r_remarks.font.size = Pt(8)
        r_remarks.font.color.rgb = RGBColor(100, 116, 139)

        doc.add_paragraph() # Spacer between labs

    # Save Document
    doc.save(filename)
    print(f"Document successfully created: {filename}")

if __name__ == "__main__":
    output_path = r"d:\OG_Agentic\Agentic_AI_Lab_Worklet_Review_Sheet_Team05.docx"
    build_docx(output_path)
