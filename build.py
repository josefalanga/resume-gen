#!/usr/bin/env python3
"""
build.py — Render resume.md → resume.html (via Jinja2 template) → resume.pdf

Usage:
    python3 build.py                                      # default paths
    python3 build.py --md resume.md                       # custom markdown source
    python3 build.py --template resume.template.html      # custom template
    python3 build.py --out out/cv.pdf                     # custom output path
    python3 build.py --html-only                          # skip PDF, just render HTML
"""

import argparse
import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright


def parse_md(md_path: Path) -> dict:
    """Extract YAML front matter from a markdown file."""
    text = md_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML front matter found in {md_path}")
    return yaml.safe_load(match.group(1))


def render_template(template_path: Path, context: dict) -> str:
    """Render a Jinja2 HTML template with the given context."""
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=False,
    )
    template = env.get_template(template_path.name)
    return template.render(**context)


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    """Use Playwright/Chromium to print an HTML file to PDF."""
    with sync_playwright() as p:
        browser = p.chromium.launch(args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu",
            "--single-process",
        ])
        page = browser.new_page()
        page.goto(f"file://{html_path}", wait_until="domcontentloaded")
        page.wait_for_timeout(800)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def build(md: str, template: str, out: str, html_only: bool = False) -> None:
    md_path       = Path(md).resolve()
    template_path = Path(template).resolve()
    pdf_path      = Path(out).resolve()

    print(f"  Markdown : {md_path}")
    print(f"  Template : {template_path}")

    # 1. Parse markdown front matter
    context = parse_md(md_path)

    # 2. Render HTML template
    rendered_html = render_template(template_path, context)

    if html_only:
        html_out = pdf_path.with_suffix(".html")
        html_out.write_text(rendered_html, encoding="utf-8")
        print(f"  HTML out : {html_out}")
        return

    # 3. Write rendered HTML next to the markdown file
    #    so relative paths like photo.jpg resolve correctly
    tmp_html = md_path.parent / "_resume_rendered.html"
    try:
        tmp_html.write_text(rendered_html, encoding="utf-8")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"  Output   : {pdf_path}")
        html_to_pdf(tmp_html, pdf_path)
        print("  Done!")
    finally:
        if tmp_html.exists():
            tmp_html.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build resume PDF from Markdown")
    parser.add_argument("--md",        default="resume.md",            help="Markdown source file")
    parser.add_argument("--template",  default="resume.template.html", help="Jinja2 HTML template")
    parser.add_argument("--out",       default="resume.pdf",           help="Output PDF path")
    parser.add_argument("--html-only", action="store_true",            help="Only render HTML, skip PDF")
    args = parser.parse_args()

    build(args.md, args.template, args.out, args.html_only)
