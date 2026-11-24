"""
Generate the Word (.docx) version of the Outdated Legacy Syllabus.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls

OUTPUT_PATH = "data/sample_curriculum/Outdated_Legacy_BTech_CSE_Curriculum_Severe_Gaps.docx"

doc = Document()

# Set margins
for section in doc.sections:
    section.top_margin = Inches(0.6)
    section.bottom_margin = Inches(0.6)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

# Title Header
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_h1 = p_title.add_run("REGIONAL INSTITUTE OF SCIENCE & TECHNOLOGY (RIST)\n")
r_h1.font.bold = True
r_h1.font.size = Pt(14)
r_h1.font.color.rgb = RGBColor(127, 29, 29) # Crimson

r_h2 = p_title.add_run("FACULTY OF ENGINEERING & COMPUTING SCIENCES\n")
r_h2.font.bold = True
r_h2.font.size = Pt(11)
r_h2.font.color.rgb = RGBColor(153, 27, 27)

r_h3 = p_title.add_run("Bachelor of Technology (B.Tech) in Computer Science & Engineering\n")
r_h3.font.size = Pt(9.5)
r_h3.font.color.rgb = RGBColor(71, 85, 105)

r_h4 = p_title.add_run("Curriculum & Course Syllabi — Regulation 2015 (Unrevised Legacy Framework) | Total Credits: 160\n")
r_h4.font.size = Pt(8.5)
r_h4.font.italic = True
r_h4.font.color.rgb = RGBColor(185, 28, 28)

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.generate_legacy_outdated_syllabus import curriculum_structure

for sem in curriculum_structure:
    p_sem = doc.add_paragraph()
    p_sem.paragraph_format.space_before = Pt(12)
    p_sem.paragraph_format.space_after = Pt(4)
    r_sem = p_sem.add_run(sem["semester"])
    r_sem.font.bold = True
    r_sem.font.size = Pt(12)
    r_sem.font.color.rgb = RGBColor(30, 58, 138)

    for c in sem["courses"]:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(8)
        p_c.paragraph_format.space_after = Pt(2)
        r_c = p_c.add_run(f"Course Code: {c['code']} — {c['title']}\n")
        r_c.font.bold = True
        r_c.font.size = Pt(10.5)
        r_c.font.color.rgb = RGBColor(15, 23, 42)

        r_cm = p_c.add_run(f"Credits: {c['credits']} | Teaching Scheme: {c['ltp']} | Category: Legacy Theory Core\n")
        r_cm.font.bold = True
        r_cm.font.size = Pt(8.5)
        r_cm.font.color.rgb = RGBColor(185, 28, 28)

        r_cd = p_c.add_run(f"Course Description: {c['desc']}")
        r_cd.font.size = Pt(8.5)
        r_cd.font.color.rgb = RGBColor(51, 65, 85)

        # Table for units
        table = doc.add_table(rows=len(c["units"]), cols=2)
        table.autofit = False
        table.columns[0].width = Inches(2.3)
        table.columns[1].width = Inches(4.7)

        for u_idx, (u_title, u_desc) in enumerate(c["units"]):
            row = table.rows[u_idx]
            c0 = row.cells[0]
            c1 = row.cells[1]
            
            p0 = c0.paragraphs[0]
            r0 = p0.add_run(u_title)
            r0.font.bold = True
            r0.font.size = Pt(8)
            r0.font.color.rgb = RGBColor(15, 23, 42)

            p1 = c1.paragraphs[0]
            r1 = p1.add_run(u_desc)
            r1.font.size = Pt(8)
            r1.font.color.rgb = RGBColor(51, 65, 85)

        p_co = doc.add_paragraph()
        p_co.paragraph_format.space_before = Pt(4)
        p_co.paragraph_format.space_after = Pt(6)
        for co_code, co_desc in c["outcomes"]:
            r_co = p_co.add_run(f"{co_code}: {co_desc}\n")
            r_co.font.size = Pt(8)
            r_co.font.color.rgb = RGBColor(180, 83, 9)

doc.save(OUTPUT_PATH)
print(f"Generated Legacy Syllabus DOCX: {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH)} bytes)")
