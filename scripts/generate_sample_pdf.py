"""
Generate an authentic academic syllabus PDF for CIS upload testing.
Uses ReportLab to build a structured multi-course B.Tech CSE curriculum document.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUTPUT_DIR = "data/sample_curriculum"
os.makedirs(OUTPUT_DIR, exist_ok=True)
PDF_PATH = os.path.join(OUTPUT_DIR, "Sample_BTech_CSE_Curriculum.pdf")

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=letter,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

# Custom styles
header_style = ParagraphStyle(
    "UnivHeader",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=16,
    leading=20,
    textColor=colors.HexColor("#0f172a"),
    alignment=1
)

sub_header_style = ParagraphStyle(
    "UnivSub",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#1e40af"),
    alignment=1
)

meta_style = ParagraphStyle(
    "UnivMeta",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#475569"),
    alignment=1
)

sem_header_style = ParagraphStyle(
    "SemHeader",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#1e3a8a"),
    spaceBefore=14,
    spaceAfter=6
)

course_title_style = ParagraphStyle(
    "CourseTitle",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#0f172a"),
    spaceBefore=10,
    spaceAfter=2
)

course_meta_style = ParagraphStyle(
    "CourseMeta",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#2563eb")
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#334155")
)

unit_title_style = ParagraphStyle(
    "UnitTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#0f172a")
)

co_style = ParagraphStyle(
    "COStyle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#047857")
)

story = []

# Title Section
story.append(Paragraph("APEX INSTITUTE OF TECHNOLOGY & ADVANCED STUDIES", header_style))
story.append(Spacer(1, 4))
story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", sub_header_style))
story.append(Spacer(1, 4))
story.append(Paragraph("Bachelor of Technology (B.Tech) in Computer Science & Engineering", meta_style))
story.append(Paragraph("Curriculum & Detailed Course Syllabi — Regulation 2024 (R-24) | Total Credits: 160", meta_style))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=14))

# Courses Data
curriculum_structure = [
    {
        "semester": "SEMESTER I",
        "courses": [
            {
                "code": "CS101",
                "title": "Programming for Problem Solving using C",
                "credits": "3.0",
                "ltp": "L: 3, T: 0, P: 0",
                "desc": "Fundamental principles of procedural computer programming, logic design, pointers, memory architectures, and structured file manipulation.",
                "units": [
                    ("UNIT 1: Introduction to Algorithms & Flowcharts", "Computational problem solving, flowcharts, pseudo-code, basic data types, operators, standard input/output."),
                    ("UNIT 2: Control Structures & Iteration", "Conditional statements, for loops, while loops, do-while iteration, nested control flows, switch-case branching."),
                    ("UNIT 3: Arrays, Strings and Modular Functions", "One-dimensional and multi-dimensional arrays, string manipulation functions, parameter passing, recursion."),
                    ("UNIT 4: Pointers and Dynamic Memory Allocation", "Pointers, address arithmetic, memory addressing, dynamic allocation using malloc, calloc, realloc, and free."),
                    ("UNIT 5: Structures, Unions and File Streams", "User-defined composite types, nested structures, file pointers, sequential and random file access, error handling.")
                ],
                "outcomes": [
                    ("CO1", "Formulate algorithmic solutions for mathematical and computational problems."),
                    ("CO2", "Implement modular, memory-efficient software using pointers and structured file streams.")
                ]
            },
            {
                "code": "CS102",
                "title": "Digital Logic and Computer Organization",
                "credits": "3.0",
                "ltp": "L: 3, T: 0, P: 0",
                "desc": "Foundational hardware concepts: combinational logic synthesis, sequential state machines, processor datapath, and memory hierarchy.",
                "units": [
                    ("UNIT 1: Boolean Algebra and Combinational Circuits", "Binary arithmetic, logic gates, Karnaugh maps minimization, multiplexers, decoders, ALU design."),
                    ("UNIT 2: Sequential Circuits and State Machines", "Latches, flip-flops (SR, JK, D, T), registers, shift registers, synchronous and asynchronous counters."),
                    ("UNIT 3: Central Processing Unit Architecture", "Instruction cycle, register transfer language, bus architecture, hardwired and microprogrammed control."),
                    ("UNIT 4: Memory Organization & Hierarchy", "RAM/ROM, cache mapping techniques, virtual memory concepts, paging, translation lookaside buffers (TLB)."),
                    ("UNIT 5: Input/Output and Peripheral Interfacing", "Programmed I/O, interrupt-driven I/O, Direct Memory Access (DMA) controllers, bus arbitration standards.")
                ],
                "outcomes": [
                    ("CO1", "Design combinational and sequential digital logic circuits for computational hardware."),
                    ("CO2", "Analyze CPU instruction execution cycles, cache hierarchy, and interrupt handling.")
                ]
            }
        ]
    },
    {
        "semester": "SEMESTER II",
        "courses": [
            {
                "code": "CS201",
                "title": "Data Structures and Algorithms",
                "credits": "4.0",
                "ltp": "L: 3, T: 1, P: 2",
                "desc": "Analysis of algorithms, linear and non-linear data structures, searching, sorting, and graph algorithms with asymptotic complexity.",
                "units": [
                    ("UNIT 1: Complexity Analysis and Linear Structures", "Big-O notation, amortized analysis, stacks, queue variants, circular queues, deque implementations."),
                    ("UNIT 2: Linked Lists and Dynamic Structures", "Singly linked lists, doubly linked lists, circular linked lists, skip lists, dynamic stack and queue."),
                    ("UNIT 3: Non-Linear Structures: Trees & Heaps", "Binary trees, tree traversals, Binary Search Trees (BST), AVL balanced trees, B-Trees, min/max heaps."),
                    ("UNIT 4: Graph Representations and Traversals", "Adjacency matrix, adjacency lists, Breadth-First Search (BFS), Depth-First Search (DFS), topological sort."),
                    ("UNIT 5: Sorting, Searching & Hashing", "Quicksort, mergesort, heap sort, linear and binary search, hash tables, collision resolution strategies.")
                ],
                "outcomes": [
                    ("CO1", "Evaluate asymptotic time and space complexity of computational algorithms."),
                    ("CO2", "Design efficient non-linear data structures for hierarchical data and graph traversals.")
                ]
            },
            {
                "code": "CS202",
                "title": "Object-Oriented Programming with Java",
                "credits": "3.0",
                "ltp": "L: 3, T: 0, P: 0",
                "desc": "Object-oriented design principles, encapsulation, polymorphism, inheritance, Java collection frameworks, and concurrent multithreading.",
                "units": [
                    ("UNIT 1: OOP Paradigms and Java Fundamentals", "Classes, objects, constructors, method overloading, encapsulation, access specifiers, garbage collection."),
                    ("UNIT 2: Inheritance, Interfaces and Packages", "Single and multilevel inheritance, method overriding, super keyword, abstract classes, interfaces, modular packages."),
                    ("UNIT 3: Exception Handling and Collections Framework", "Built-in and custom exceptions, try-catch-finally, ArrayList, LinkedList, HashSet, HashMap collections."),
                    ("UNIT 4: Multithreading and Synchronization", "Thread lifecycle, Runnable interface, thread synchronization, locks, inter-thread communication mechanisms."),
                    ("UNIT 5: I/O Streams and Modern Java Features", "Byte and character streams, object serialization, lambda expressions, Functional Interfaces, Stream API.")
                ],
                "outcomes": [
                    ("CO1", "Develop modular, maintainable software architectures leveraging SOLID object-oriented principles."),
                    ("CO2", "Apply Java concurrent multithreading and collections to build resilient enterprise applications.")
                ]
            }
        ]
    },
    {
        "semester": "SEMESTER III",
        "courses": [
            {
                "code": "CS301",
                "title": "Database Management Systems",
                "credits": "4.0",
                "ltp": "L: 3, T: 0, P: 2",
                "desc": "Relational data modeling, SQL query optimization, normalization, transaction management, ACID properties, and database indexing.",
                "units": [
                    ("UNIT 1: Database Architecture and Relational Model", "Three-schema architecture, data independence, ER and EER modeling, relational algebra, tuple calculus."),
                    ("UNIT 2: Structured Query Language (SQL)", "DDL, DML, DCL, complex nested queries, joins, views, triggers, stored procedures, assertions."),
                    ("UNIT 3: Relational Schema Normalization", "Functional dependencies, inference rules, 1NF, 2NF, 3NF, Boyce-Codd Normal Form (BCNF), multi-valued dependencies."),
                    ("UNIT 4: Transaction Processing & Concurrency", "ACID properties, serializability, conflict and view serializability, two-phase locking (2PL), deadlock prevention."),
                    ("UNIT 5: Storage and Indexing Structures", "File organizations, B-Tree and B+ Tree indexing, hash-based indexing, query processing and cost-based optimization.")
                ],
                "outcomes": [
                    ("CO1", "Design normalized relational schemas minimizing redundancy and eliminating update anomalies."),
                    ("CO2", "Implement high-throughput transaction management systems with strict ACID compliance.")
                ]
            },
            {
                "code": "CS302",
                "title": "Operating Systems & Systems Programming",
                "credits": "4.0",
                "ltp": "L: 3, T: 1, P: 0",
                "desc": "Core OS concepts: process management, CPU scheduling, synchronization primitives, memory paging, and virtual file systems.",
                "units": [
                    ("UNIT 1: Operating System Services & System Calls", "Kernel structures, monolithic vs microkernel architectures, system call interface, process state transitions."),
                    ("UNIT 2: Process Scheduling & Concurrency", "Preemptive scheduling, round-robin, priority scheduling, critical section problem, semaphores, mutex locks."),
                    ("UNIT 3: Deadlocks and Process Synchronization", "Deadlock conditions, resource allocation graphs, Banker's algorithm, deadlock detection and recovery."),
                    ("UNIT 4: Memory Management & Virtual Memory", "Contiguous allocation, paging, segmentation, demand paging, page replacement algorithms (FIFO, LRU, Optimal)."),
                    ("UNIT 5: File Systems & Storage Management", "File concepts, directory structures, allocation methods, disk scheduling (SSTF, SCAN, C-SCAN), security.")
                ],
                "outcomes": [
                    ("CO1", "Analyze process synchronization mechanisms, race conditions, and deadlock avoidance algorithms."),
                    ("CO2", "Evaluate virtual memory architectures, paging replacement strategies, and disk scheduling algorithms.")
                ]
            }
        ]
    },
    {
        "semester": "SEMESTER IV",
        "courses": [
            {
                "code": "CS303",
                "title": "Computer Networks & Distributed Protocols",
                "credits": "3.0",
                "ltp": "L: 3, T: 0, P: 0",
                "desc": "Layered protocol stack: OSI and TCP/IP, reliable transport mechanisms, routing algorithms, congestion control, and application protocols.",
                "units": [
                    ("UNIT 1: Physical and Data Link Layer Protocols", "Network topologies, guided/unguided media, framing, error detection (CRC), flow control (Stop-and-Wait, Go-Back-N)."),
                    ("UNIT 2: Medium Access Control and Ethernet", "CSMA/CD, CSMA/CA, IEEE 802.3 Ethernet, IEEE 802.11 Wi-Fi, switching, VLAN configurations."),
                    ("UNIT 3: Network Layer and Routing Protocols", "IPv4 addressing, subnetting, CIDR, IPv6, distance-vector routing (RIP), link-state routing (OSPF), BGP."),
                    ("UNIT 4: Transport Layer & Flow Control", "UDP datagrams, TCP segment format, 3-way handshake, flow control, TCP Tahoe/Reno congestion control."),
                    ("UNIT 5: Application Layer and Network Security", "DNS, HTTP/1.1, HTTP/2, SMTP, FTP, SSL/TLS handshake, public key infrastructure, network firewalls.")
                ],
                "outcomes": [
                    ("CO1", "Configure subnets, IP routing tables, and analyze packet flow across internet routers."),
                    ("CO2", "Assess end-to-end transport layer reliability and cryptographic security protocols.")
                ]
            },
            {
                "code": "CS304",
                "title": "Artificial Intelligence & Machine Learning",
                "credits": "4.0",
                "ltp": "L: 3, T: 0, P: 2",
                "desc": "Fundamental heuristic search, probabilistic reasoning, supervised learning, neural networks, and modern deep learning foundations.",
                "units": [
                    ("UNIT 1: Intelligent Agents & Problem Formulation", "Agent architectures, environment types, state space search, uninformed search, A* heuristic search, adversarial minimax."),
                    ("UNIT 2: Knowledge Representation & Logic", "Propositional logic, first-order predicate calculus, resolution refutation, forward and backward chaining, Bayesian networks."),
                    ("UNIT 3: Supervised Learning Foundations", "Linear regression, logistic regression, decision trees, entropy, random forests, Support Vector Machines (SVM)."),
                    ("UNIT 4: Unsupervised Learning & Clustering", "K-Means clustering, hierarchical clustering, Principal Component Analysis (PCA), dimensionality reduction."),
                    ("UNIT 5: Neural Networks & Deep Learning", "Perceptron, multi-layer feedforward networks, backpropagation, activation functions, convolutional neural networks (CNN).")
                ],
                "outcomes": [
                    ("CO1", "Formulate complex search problems using heuristic algorithms and knowledge representation."),
                    ("CO2", "Implement machine learning models for classification, regression, and clustering tasks.")
                ]
            }
        ]
    }
]

for sem in curriculum_structure:
    story.append(Paragraph(sem["semester"], sem_header_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#cbd5e1"), spaceAfter=8))

    for c in sem["courses"]:
        c_elements = []
        c_elements.append(Paragraph(f"Course Code: {c['code']} — {c['title']}", course_title_style))
        c_elements.append(Paragraph(f"Credits: {c['credits']} | Teaching Scheme: {c['ltp']} | Category: Professional Core", course_meta_style))
        c_elements.append(Spacer(1, 3))
        c_elements.append(Paragraph(f"<b>Course Description:</b> {c['desc']}", body_style))
        c_elements.append(Spacer(1, 5))

        # Units table
        unit_rows = []
        for u_title, u_desc in c["units"]:
            unit_rows.append([
                Paragraph(u_title, unit_title_style),
                Paragraph(u_desc, body_style)
            ])

        unit_table = Table(unit_rows, colWidths=[200, 332])
        unit_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#e2e8f0")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        c_elements.append(unit_table)
        c_elements.append(Spacer(1, 4))

        # Course Outcomes
        for co_code, co_desc in c["outcomes"]:
            c_elements.append(Paragraph(f"<b>{co_code}:</b> {co_desc}", co_style))

        c_elements.append(Spacer(1, 10))
        story.append(KeepTogether(c_elements))

# Build Document
doc.build(story)
print(f"Generated Syllabus PDF: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
