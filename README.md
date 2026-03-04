# Resume Generator

This repository contains the source and build pipeline for my resume.

I got tired of maintaining my resume up to date like an animal, with visual tools, so I automated the process.

You can grab the latest release in the relevant section, or download and compile it yourself!

Below, there is some AI generated documentation for anyone curious. I was too lazy to explain it myself.

## About

The resume is maintained as structured data in a single Markdown file and rendered automatically into a PDF using a Jinja2 HTML template and a headless Chromium renderer. GitHub Actions builds the PDF and publishes it as a release artifact.

The repository serves two purposes:

* Maintain a single source of truth for the resume.
* Demonstrate a simple automated document build pipeline.

## Overview

The build process is:

```
resume.md (YAML front matter)
        │
        ▼
Jinja2 HTML template
        │
        ▼
Rendered HTML
        │
        ▼
Playwright / Chromium
        │
        ▼
resume.pdf
```

The Markdown file contains structured resume data using YAML front matter.
The template (`resume.template.html`) renders this data into HTML.
Playwright launches a headless Chromium instance to print the HTML into a PDF.

## Repository Structure

```
.
├── build.py
├── requirements.txt
├── resume.md
├── resume.template.html
├── photo.jpg
└── .github/workflows/release.yml
```

| File                            | Purpose                                                |
| ------------------------------- | ------------------------------------------------------ |
| `resume.md`                     | Source of truth for resume content                     |
| `resume.template.html`          | Jinja2 template for rendering                          |
| `build.py`                      | Build script                                           |
| `requirements.txt`              | Python dependencies                                    |
| `photo.jpg`                     | Resume photo                                           |
| `.github/workflows/release.yml` | CI pipeline that builds the PDF and publishes releases |

## Local Build

Install dependencies:

```
pip install -r requirements.txt
playwright install chromium
```

Generate the PDF:

```
python build.py
```

Output:

```
resume.pdf
```

Generate HTML only:

```
python build.py --html-only
```

## Automated Releases

Releases are generated automatically via GitHub Actions.

When a version tag is pushed:

```
git tag v1.0
git push origin v1.0
```

the workflow will:

1. Install Python dependencies
2. Install Playwright and Chromium
3. Run `build.py`
4. Upload `resume.pdf` to the GitHub Release

## Latest Resume

The most recent PDF is always available at:

```
https://github.com/josefalanga/resume-gen/releases/latest/download/resume.pdf
```

## Dependencies

* Python 3.11+
* Jinja2
* PyYAML
* Playwright
* Chromium (installed via Playwright)

The generator code is provided for reference and reuse.
Resume content is personal and not intended for redistribution.
