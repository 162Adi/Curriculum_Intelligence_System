"""
Generate an authentic academic syllabus PDF with SEVERE, STRIKING GAPS for CIS demonstration.
Represents an obsolete / legacy curriculum (Regulation 2015 - unrevised) containing outdated 1990s-2000s
technologies (Turbo C, 8085 assembly, VB6, FoxPro, Perl CGI, Token Ring, Floppy Disks) with
TOTAL ABSENCE of AI/ML, Cloud Computing, DevOps/Docker, Vector DBs, Modern Web, and Cybersecurity.
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
PDF_PATH = os.path.join(OUTPUT_DIR, "Outdated_Legacy_BTech_CSE_Curriculum_Severe_Gaps.pdf")

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=letter,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

# Typography Styles
header_style = ParagraphStyle(
    "UnivHeader",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=15,
    leading=19,
    textColor=colors.HexColor("#7f1d1d"), # Deep crimson/maroon to denote unrevised legacy
    alignment=1
)

sub_header_style = ParagraphStyle(
    "UnivSub",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#991b1b"),
    alignment=1
)

meta_style = ParagraphStyle(
    "UnivMeta",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#475569"),
    alignment=1
)

sem_header_style = ParagraphStyle(
    "SemHeader",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#1e3a8a"),
    spaceBefore=12,
    spaceAfter=5
)

course_title_style = ParagraphStyle(
    "CourseTitle",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor("#0f172a"),
    spaceBefore=8,
    spaceAfter=2
)

course_meta_style = ParagraphStyle(
    "CourseMeta",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#b91c1c") # Alerting red tone
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=11.5,
    textColor=colors.HexColor("#334155")
)

unit_title_style = ParagraphStyle(
    "UnitTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=11.5,
    textColor=colors.HexColor("#0f172a")
)

co_style = ParagraphStyle(
    "COStyle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=7.5,
    leading=10.5,
    textColor=colors.HexColor("#b45309") # Amber tone for low Bloom verbs
)

story = []

# Title Section
story.append(Paragraph("REGIONAL INSTITUTE OF SCIENCE & TECHNOLOGY (RIST)", header_style))
story.append(Spacer(1, 3))
story.append(Paragraph("FACULTY OF ENGINEERING & COMPUTING SCIENCES", sub_header_style))
story.append(Spacer(1, 3))
story.append(Paragraph("Bachelor of Technology (B.Tech) in Computer Science & Engineering", meta_style))
story.append(Paragraph("Undergraduate Curriculum & Detailed Course Syllabi — Regulation 2015 (R-15 Legacy Framework)", meta_style))
story.append(Paragraph("Status: UNREVISED (Over 10 Years Static) | Total Graduation Credits: 160", meta_style))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#991b1b"), spaceAfter=12))

# 8 Courses Designed with HUGE, SEVERE Gaps
curriculum_structure = [
    {
        "semester": "SEMESTER I",
        "courses": [
            {
                "code": "CS101",
                "title": "Turbo C Programming & Flowcharting",
                "credits": "4.0",
                "ltp": "L: 4, T: 0, P: 0",
                "desc": "Procedural programming principles strictly using Borland Turbo C compiler in 16-bit DOSBox emulation mode, flowchart drawing on paper, and conio.h screen manipulation.",
                "units": [
                    ("UNIT 1: DOS Environment & Flowcharts", "Introduction to MS-DOS command prompt, autoexec.bat, flowchart templates, terminal compilation with TCC.EXE, conio.h, clrscr() and getch() routines."),
                    ("UNIT 2: Primitive Data Types & Control Structures", "16-bit integers, float representations, goto statements, nested if-else branching, switch-case constructs, infinite while loops."),
                    ("UNIT 3: Static One-Dimensional Arrays", "Fixed-size static array declarations, linear scanning, matrix operations, string termination with null bytes in 16-bit memory models."),
                    ("UNIT 4: Segmented Architecture & Pointer Math", "Near and far pointers in 16-bit segmented architecture, addressing offset calculation, static memory buffers, passing values by reference."),
                    ("UNIT 5: File Operations with Disk Drives", "Sequential text files, binary records on 3.5-inch floppy diskette drives (A: drive), basic fopen/fclose syntax, EOF marker handling.")
                ],
                "outcomes": [
                    ("CO1", "Memorize procedural C keywords and draw static flowcharts using standard drafting symbols."),
                    ("CO2", "Operate the Borland Turbo C integrated development environment inside a 16-bit DOS emulator.")
                ]
            },
            {
                "code": "CS102",
                "title": "8085 Microprocessor Architecture & Assembly",
                "credits": "4.0",
                "ltp": "L: 4, T: 0, P: 0",
                "desc": "Low-level hardware study of the 8-bit Intel 8085 microprocessor, assembly mnemonic coding on physical hex trainer kits, and discrete peripheral chip interfacing.",
                "units": [
                    ("UNIT 1: 8085 Internal Hardware Architecture", "8-bit accumulator, flag register layout, general purpose register pairs (BC, DE, HL), stack pointer, program counter, multiplexed address/data bus."),
                    ("UNIT 2: Instruction Set & Machine Cycles", "Instruction formats, opcode fetch cycles, memory read/write cycles, addressing modes, arithmetic and logical instruction mnemonics."),
                    ("UNIT 3: Hexadecimal Keypad Programming", "Entering hexadecimal opcodes manually into 7-segment LED trainer kits, single-step hardware debugging, register inspection."),
                    ("UNIT 4: Interrupts & Serial Data Transfer", "TRAP, RST 7.5, RST 6.5, RST 5.5, INTR hardware interrupt pins, SIM and RIM instructions for serial I/O communication."),
                    ("UNIT 5: Peripheral Interfacing ICs", "Intel 8255 Programmable Peripheral Interface, Intel 8259 Interrupt Controller, Intel 8253 Programmable Interval Timer interfacing via breadboards.")
                ],
                "outcomes": [
                    ("CO1", "Recall the pin diagram and internal bus multiplexing of the 8-bit Intel 8085 microprocessor."),
                    ("CO2", "Key in hexadecimal machine codes on physical training kit boards to execute simple 8-bit addition.")
                ]
            }
        ]
    },
    {
        "semester": "SEMESTER II",
        "courses": [
            {
                "code": "CS201",
                "title": "Procedural Data Structures in Turbo C",
                "credits": "4.0",
                "ltp": "L: 4, T: 0, P: 0",
                "desc": "Elementary data structures implemented without modern object-oriented paradigms, standard template libraries (STL), or dynamic memory frameworks.",
                "units": [
                    ("UNIT 1: Static Stacks and Queues", "Array-based stack implementation with fixed limits, push and pop routines, static circular queue implementation, overflow and underflow checks."),
                    ("UNIT 2: Singly Linked Chains", "Pointer-linked linear chains in procedural C, traversal routines, insertion at head and tail, deletion of nodes."),
                    ("UNIT 3: Elementary Sorting Algorithms", "Bubble sort step-by-step trace, selection sort, insertion sort on small static integer arrays."),
                    ("UNIT 4: Static Binary Search Trees", "Binary tree definitions, left child and right child pointers, recursive in-order, pre-order, and post-order node traversals."),
                    ("UNIT 5: Sequential File Storage", "Linear searching through flat sequential text records, basic hashing with modulo arithmetic on hard disk partitions.")
                ],
                "outcomes": [
                    ("CO1", "Define elementary linear data structures using static arrays in procedural C."),
                    ("CO2", "Trace the algorithmic steps of bubble sort and selection sort on chalkboard exercises.")
                ]
            },
            {
                "code": "CS202",
                "title": "Visual Basic 6.0 & Desktop Application Programming",
                "credits": "4.0",
                "ltp": "L: 3, T: 1, P: 0",
                "desc": "Rapid application development using Microsoft Visual Basic 6.0, drag-and-drop form construction, ActiveX controls, and localized Microsoft Access desktop databases.",
                "units": [
                    ("UNIT 1: Visual Basic 6.0 IDE Fundamentals", "Toolbox controls, CommandButton, TextBox, Label, OptionButton, ComboBox, Form properties, project structure (.vbp)."),
                    ("UNIT 2: Event-Driven Programming Model", "Click, DoubleClick, Change, MouseMove event procedures, msgbox and inputbox dialog functions, variable scopes in VB6."),
                    ("UNIT 3: ActiveX Controls & Menus", "Menu editor, CommonDialog controls, PictureBox, Image control, timer tick events, compiling executables for Windows 98/XP."),
                    ("UNIT 4: DAO & ADO Data Controls", "Data Access Objects (DAO), ActiveX Data Objects (ADO), binding text boxes to local Microsoft Access .mdb files."),
                    ("UNIT 5: Reporting with Crystal Reports 8.5", "Generating standalone invoice printouts using legacy Crystal Reports, packaging VB6 installers with Setup.exe wizards.")
                ],
                "outcomes": [
                    ("CO1", "Construct graphical forms with drag-and-drop buttons and text boxes in Visual Basic 6.0."),
                    ("CO2", "Connect Visual Basic forms to local desktop Microsoft Access (.mdb) files using ADO controls.")
                ]
            }
        ]
    },
    {
        "semester": "SEMESTER III",
        "courses": [
            {
                "code": "CS301",
                "title": "Traditional Database Systems with FoxPro & Oracle 8i",
                "credits": "4.0",
                "ltp": "L: 4, T: 0, P: 0",
                "desc": "Legacy database systems: flat file table structures, xBase commands in Microsoft Visual FoxPro, and classical SQL-92 commands on Oracle 8i installations.",
                "units": [
                    ("UNIT 1: File Processing Systems vs DBMS", "Limitations of manual flat filing systems, early hierarchical and network data models, records and fields terminology."),
                    ("UNIT 2: Visual FoxPro Table Manipulation", "Creating .dbf files, append, browse, edit commands, indexing on single fields, FoxPro command-line expressions."),
                    ("UNIT 3: Relational Concepts & SQL-92", "Relational tables, basic SELECT, INSERT, UPDATE, DELETE queries on Oracle 8i, simple primary keys and foreign keys."),
                    ("UNIT 4: Elementary Schema Normalization", "First normal form (atomic attributes), second normal form (partial dependencies), third normal form exercises."),
                    ("UNIT 5: Backup on Tape & Disk Partitions", "Exporting database dump files, magnetic tape storage considerations, single-user database lock commands.")
                ],
                "outcomes": [
                    ("CO1", "List basic SQL queries for single relational tables using legacy Oracle 8i command line."),
                    ("CO2", "Create and index flat .dbf tables using Microsoft Visual FoxPro command-line utilities.")
                ]
            },
            {
                "code": "CS302",
                "title": "Legacy Operating Systems & MS-DOS Internals",
                "credits": "4.0",
                "ltp": "L: 4, T: 0, P: 0",
                "desc": "Single-user operating systems, early personal computer BIOS boot sequencing, command.com batch files, and FAT16 disk allocation tables.",
                "units": [
                    ("UNIT 1: Operating System Evolution & Single-Tasking", "History of mainframe batch processors, CP/M, disk operating system (MS-DOS), single-program execution flow."),
                    ("UNIT 2: BIOS Services & Interrupt Vector Table", "Master boot record (MBR), BIOS interrupt 21h functions, keyboard and display BIOS routines, IO.SYS and MSDOS.SYS roles."),
                    ("UNIT 3: Memory Organization in 16-Bit DOS", "Conventional memory 640KB barrier, upper memory blocks, expanded memory (EMS), extended memory (XMS), HIMEM.SYS driver."),
                    ("UNIT 4: FAT16 File System Architecture", "Boot sector, file allocation tables, root directory entries, 8.3 filename limitations, cluster allocation and lost chains."),
                    ("UNIT 5: Batch Scripting & Command Utilities", "Authoring .bat scripts, config.sys device drivers, chkdsk, fdisk partition utility, debug.exe memory inspection.")
                ],
                "outcomes": [
                    ("CO1", "Describe the role of BIOS interrupt 21h and 640KB conventional memory barrier in MS-DOS."),
                    ("CO2", "Write basic batch files to automate file copying and directory listing on single-user workstations.")
                ]
            }
        ]
    },
    {
        "semester": "SEMESTER IV",
        "courses": [
            {
                "code": "CS401",
                "title": "Telecommunications & Local Area Networks",
                "credits": "4.0",
                "ltp": "L: 4, T: 0, P: 0",
                "desc": "Early telecommunications: telephone modems, coaxial cabling, Ethernet 10BASE2 coaxial bus topology, and theoretical OSI 7-layer models.",
                "units": [
                    ("UNIT 1: Physical Media & Analog Modems", "Twisted pair cabling, thick and thin coaxial cables (RG-58), BNC connectors, RS-232 serial ports, dial-up telephone modems."),
                    ("UNIT 2: Early LAN Architectures & Topologies", "Bus topology, ring topology, star topology, token passing in IBM Token Ring networks, CSMA/CD principles."),
                    ("UNIT 3: OSI 7-Layer Theoretical Model", "Physical, data link, network, transport, session, presentation, application layer theoretical definitions and responsibilities."),
                    ("UNIT 4: Classful IPv4 Addressing", "Class A, B, C, D, E network addresses, default subnet masks, ARP and RARP translation, static IP configuration in Windows 98."),
                    ("UNIT 5: Early Internet Application Protocols", "FTP file transfer command line, Telnet terminal access, early POP3/SMTP email headers, dial-up networking scripts.")
                ],
                "outcomes": [
                    ("CO1", "Recall the seven theoretical layers of the ISO-OSI network model."),
                    ("CO2", "Identify physical BNC connectors, coaxial cables, and calculate default Classful IPv4 subnets.")
                ]
            },
            {
                "code": "CS402",
                "title": "Software Engineering & Waterfall Methodology",
                "credits": "4.0",
                "ltp": "L: 4, T: 0, P: 0",
                "desc": "Classical linear sequential Waterfall lifecycle, paper Software Requirement Specification (SRS) documents, and static software testing.",
                "units": [
                    ("UNIT 1: Classical Waterfall Software Lifecycle", "Feasibility study, requirements analysis, architectural design, coding, testing, deployment on CD-ROM/floppy disk."),
                    ("UNIT 2: Software Requirement Documentation", "IEEE 830 paper SRS templates, user requirements vs system requirements, manual reviews and inspection sign-offs."),
                    ("UNIT 3: Function Point Estimation & COCOMO-I", "Line of Code (LOC) counting, Basic COCOMO cost estimation, project scheduling using manual Gantt charts on paper."),
                    ("UNIT 4: Structural Black-Box Testing", "Boundary value analysis on paper worksheets, equivalence partitioning, manual test case logging, bug tracking ledgers."),
                    ("UNIT 5: Software Maintenance & Physical Packaging", "Corrective maintenance, shrink-wrap retail box packaging, floppy disk duplicating, user manual printing.")
                ],
                "outcomes": [
                    ("CO1", "Describe the rigid phased progression of the classical linear sequential Waterfall development model."),
                    ("CO2", "Calculate estimated project effort using basic COCOMO-I formulas from static lines of code (LOC).")
                ]
            }
        ]
    }
]

for sem in curriculum_structure:
    story.append(Paragraph(sem["semester"], sem_header_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#991b1b"), spaceAfter=6))

    for c in sem["courses"]:
        c_elements = []
        c_elements.append(Paragraph(f"Course Code: {c['code']} — {c['title']}", course_title_style))
        c_elements.append(Paragraph(f"Credits: {c['credits']} | Teaching Scheme: {c['ltp']} | Category: Legacy Theory Core", course_meta_style))
        c_elements.append(Spacer(1, 2))
        c_elements.append(Paragraph(f"<b>Course Description:</b> {c['desc']}", body_style))
        c_elements.append(Spacer(1, 4))

        # Units table
        unit_rows = []
        for u_title, u_desc in c["units"]:
            unit_rows.append([
                Paragraph(u_title, unit_title_style),
                Paragraph(u_desc, body_style)
            ])

        unit_table = Table(unit_rows, colWidths=[190, 342])
        unit_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fff1f2")), # Very light reddish background
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#fca5a5")),
            ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor("#fee2e2")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ]))
        c_elements.append(unit_table)
        c_elements.append(Spacer(1, 3))

        # Course Outcomes
        for co_code, co_desc in c["outcomes"]:
            c_elements.append(Paragraph(f"<b>{co_code}:</b> {co_desc}", co_style))

        c_elements.append(Spacer(1, 8))
        story.append(KeepTogether(c_elements))

doc.build(story)
print(f"Generated Legacy Syllabus PDF: {PDF_PATH} ({os.path.getsize(PDF_PATH)} bytes)")
