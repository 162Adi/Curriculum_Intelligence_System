"""
Generate sample curriculum files (DOCX and CSV) for faculty upload testing.
"""

import os
import csv
import docx

os.makedirs("data/sample_curriculum", exist_ok=True)

# 1. Generate DOCX sample curriculum
doc = docx.Document()
doc.add_heading("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", level=0)
doc.add_heading("B.Tech Computer Science & Engineering — Curriculum & Syllabus", level=1)
doc.add_paragraph("Academic Regulation: 2024-2028 | Total Credits: 160")

curriculum_data = [
    ("SEMESTER I", [
        ("CS101", "Programming for Problem Solving using C", "3.0", "L: 3, T: 0, P: 0", [
            ("Unit 1: Introduction to Algorithms & Flowcharts", "Variables, data types, standard input/output, conditional statements"),
            ("Unit 2: Control Structures & Loops", "For loops, while loops, nested constructs, switch cases"),
            ("Unit 3: Arrays and Strings", "Single and multidimensional arrays, string manipulation functions"),
            ("Unit 4: Pointers and Memory", "Pointer arithmetic, dynamic memory allocation with malloc and free"),
            ("Unit 5: Structures and File Handling", "User defined structures, file operations, error handling in files")
        ], [
            ("CO1", "Formulate algorithmic solutions for mathematical and logical problems"),
            ("CO2", "Implement modular programs using functions, pointers, and memory control")
        ]),
        ("CS102", "Digital Logic and Computer Organization", "3.0", "L: 3, T: 0, P: 0", [
            ("Unit 1: Boolean Algebra and Gates", "K-maps, combinational logic design, adders and multiplexers"),
            ("Unit 2: Sequential Circuits", "Flip-flops, registers, counters, finite state machines"),
            ("Unit 3: Basic Computer Architecture", "Instruction cycle, ALU design, register transfer language"),
            ("Unit 4: Memory Hierarchy", "Cache memory, virtual memory, paging, address translation"),
            ("Unit 5: Input/Output Organization", "Interrupts, DMA, bus arbitration, programmed I/O")
        ], [
            ("CO1", "Design combinational and sequential digital logic circuits"),
            ("CO2", "Analyze CPU datapath, memory caching, and bus communication protocols")
        ]),
    ]),
    ("SEMESTER II", [
        ("CS201", "Data Structures and Algorithms", "4.0", "L: 3, T: 1, P: 2", [
            ("Unit 1: Linear Data Structures", "Arrays, stacks, queue implementations, circular queues"),
            ("Unit 2: Linked Lists", "Singly, doubly, and circular linked lists with operations"),
            ("Unit 3: Trees and BST", "Binary trees, traversals, Binary Search Trees, AVL balance"),
            ("Unit 4: Graphs and Traversals", "Breadth-First Search, Depth-First Search, shortest path Dijkstra"),
            ("Unit 5: Sorting and Hashing", "Merge sort, Quick sort, Hash tables, collision resolution")
        ], [
            ("CO1", "Evaluate asymptotic complexity of algorithms using Big-O notation"),
            ("CO2", "Design efficient data structures for graph traversal and searching")
        ]),
        ("CS202", "Object-Oriented Programming with Java", "3.0", "L: 3, T: 0, P: 0", [
            ("Unit 1: OOP Principles", "Classes, objects, encapsulation, abstraction, inheritance"),
            ("Unit 2: Polymorphism & Interfaces", "Method overloading, overriding, abstract classes, interfaces"),
            ("Unit 3: Exception Handling & Collections", "Try-catch blocks, custom exceptions, ArrayList, HashMap"),
            ("Unit 4: Multithreading & Concurrency", "Thread lifecycle, synchronization, inter-thread communication"),
            ("Unit 5: Streams and Modern Java", "Lambda expressions, Stream API, file I/O operations")
        ], [
            ("CO1", "Develop robust object-oriented applications adhering to SOLID principles"),
            ("CO2", "Apply multithreading and collection frameworks for concurrent data processing")
        ]),
    ]),
]

for sem_title, courses in curriculum_data:
    doc.add_heading(sem_title, level=2)
    for code, title, credits, ltp, units, outcomes in courses:
        doc.add_heading(f"Course: {code} - {title}", level=3)
        doc.add_paragraph(f"Credits: {credits} | {ltp}")
        for utitle, udesc in units:
            doc.add_paragraph(f"{utitle}: {udesc}")
        doc.add_paragraph("Course Outcomes:")
        for co_code, co_desc in outcomes:
            doc.add_paragraph(f"{co_code}: {co_desc}")

docx_path = "data/sample_curriculum/Sample_BTech_CSE_Curriculum.docx"
doc.save(docx_path)
print(f"Created sample DOCX at {docx_path}")

# 2. Generate CSV sample curriculum
csv_path = "data/sample_curriculum/Sample_Curriculum_Courses.csv"
with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Semester", "Course Code", "Course Title", "Type", "Credits", "L", "T", "P", "Description"])
    writer.writerow([1, "CS101", "Programming for Problem Solving using C", "THEORY", 3.0, 3, 0, 0, "Core programming principles in C"])
    writer.writerow([1, "CS102", "Digital Logic and Computer Organization", "THEORY", 3.0, 3, 0, 0, "Digital circuits, architecture and memory"])
    writer.writerow([2, "CS201", "Data Structures and Algorithms", "INTEGRATED", 4.0, 3, 1, 2, "Trees, graphs, dynamic programming, sorting"])
    writer.writerow([2, "CS202", "Object-Oriented Programming with Java", "THEORY", 3.0, 3, 0, 0, "OOP, multithreading, collections, streams"])
    writer.writerow([3, "CS301", "Database Management Systems", "THEORY", 3.0, 3, 0, 0, "Relational schemas, SQL, transactions, normalization"])
    writer.writerow([3, "CS302", "Operating Systems", "THEORY", 3.0, 3, 0, 0, "Process scheduling, virtual memory, file systems"])
    writer.writerow([4, "CS401", "Computer Networks", "THEORY", 3.0, 3, 0, 0, "TCP/IP stack, routing, sockets, HTTP"])
    writer.writerow([4, "CS402", "Artificial Intelligence & Foundations", "THEORY", 3.0, 3, 0, 0, "Search, logic, basic machine learning"])

print(f"Created sample CSV at {csv_path}")
