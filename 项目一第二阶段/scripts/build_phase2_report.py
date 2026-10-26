#!/usr/bin/env python3
"""Build the compact second-stage report from Markdown.

This wraps scripts/md_to_docx.py and then applies report-specific layout:
- keep only the cover -> abstract page break;
- use 10pt body text and 1.3 line spacing so the report stays within 15 pages;
- tighten table cell margins and heading spacing.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from md_to_docx import convert, set_run_font


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "项目完成报告_第二阶段.md"
OUTPUT = ROOT / "大作业一第二阶段实验报告.docx"


def set_cell_margins(cell, top=20, bottom=20, left=55, right=55):
    tcpr = cell._tc.get_or_add_tcPr()
    tcmar = tcpr.first_child_found_in("w:tcMar")
    if tcmar is None:
        tcmar = OxmlElement("w:tcMar")
        tcpr.append(tcmar)
    for tag, value in (("top", top), ("bottom", bottom),
                       ("start", left), ("end", right)):
        element = OxmlElement(f"w:{tag}")
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")
        tcmar.append(element)


def main() -> int:
    headings, tables, codes = convert(SOURCE, OUTPUT)
    doc = Document(str(OUTPUT))

    section = doc.sections[0]
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.header_distance = Cm(1.2)
    section.footer_distance = Cm(1.2)

    normal = doc.styles["Normal"]
    normal.font.size = Pt(10)
    pf = normal.paragraph_format
    pf.line_spacing = 1.25
    pf.space_before = Pt(0)
    pf.space_after = Pt(2.5)
    pf.first_line_indent = Pt(20)

    heading_specs = {
        "Heading 1": (15, 10, 4),
        "Heading 2": (12.5, 7, 2),
        "Heading 3": (11, 5, 1),
    }
    for name, (size, before, after) in heading_specs.items():
        style = doc.styles[name]
        style.font.size = Pt(size)
        hpf = style.paragraph_format
        hpf.space_before = Pt(before)
        hpf.space_after = Pt(after)
        hpf.line_spacing = 1.15

    table_text = doc.styles["TableText"]
    table_text.font.size = Pt(8.5)
    table_text.paragraph_format.line_spacing = 1.0
    table_text.paragraph_format.space_before = Pt(0)
    table_text.paragraph_format.space_after = Pt(0)

    list_text = doc.styles["ListText"]
    list_text.font.size = Pt(10)
    list_text.paragraph_format.line_spacing = 1.2
    list_text.paragraph_format.space_after = Pt(0.5)

    code_style = doc.styles["CodeBlock"]
    code_style.font.size = Pt(8)
    code_style.paragraph_format.line_spacing = 1.0
    code_style.paragraph_format.space_before = Pt(2)
    code_style.paragraph_format.space_after = Pt(4)
    code_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    title = doc.styles["ReportTitle"]
    title.font.size = Pt(22)
    title.paragraph_format.space_before = Pt(60)
    title.paragraph_format.space_after = Pt(14)
    subtitle = doc.styles["ReportSubtitle"]
    subtitle.font.size = Pt(15)
    subtitle.paragraph_format.space_after = Pt(30)

    # Only the abstract starts on a new page; chapter headings flow continuously.
    for paragraph in doc.paragraphs:
        if paragraph.text.strip() != "摘要":
            paragraph.paragraph_format.page_break_before = False

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_margins(cell)
        if table.rows:
            for cell in table.rows[0].cells:
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.keep_with_next = True
        if table.rows and table.rows[0].cells[0].text.strip() == "测试函数":
            for row in table.rows:
                row.cells[0].width = Cm(8.8)
                row.cells[1].width = Cm(6.2)
            table.columns[0].width = Cm(8.8)
            table.columns[1].width = Cm(6.2)

    header = section.header.paragraphs[0]
    for run in list(header.runs):
        run._element.getparent().remove(run._element)
    header_run = header.add_run("基于 MongoDB 的在线问卷系统（第二阶段）")
    set_run_font(header_run, size=8.5, color=RGBColor(0x59, 0x59, 0x59))

    props = doc.core_properties
    props.title = "实验报告（第二阶段）——基于 MongoDB 的在线问卷系统"
    props.subject = "数据管理系统课程实验报告（第二阶段）"
    props.comments = "由 docs/项目完成报告_第二阶段.md 转换生成"
    props.keywords = "MongoDB; Flask; 在线问卷; 题目库; 版本管理; 实验报告"
    props.category = "实验报告"

    doc.save(str(OUTPUT))
    print(f"built: {OUTPUT}")
    print(f"parsed: {headings} headings, {tables} tables, {codes} code blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
