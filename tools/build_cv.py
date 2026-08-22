#!/usr/bin/env python3
"""Generate the print CV as a PDF, in English and French.

Source of truth: data/cv-print.json, itself derived from
Documents/Thèses/cv_master_Hafid_IDRISSI.json (audit of 2026-08-20).

The CV is laid out as a single column so that applicant tracking systems can
parse it, and rendered through headless Chrome so the text stays selectable.
Experience is one section, reverse chronological, with an explicit type label
on every entry — personal, entrepreneurial, academic and research work is
never presented as salaried employment.

Usage:
    python tools/build_cv.py            # both languages
    python tools/build_cv.py en         # one language
"""

import json
import shutil
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "cv-print.json"
OUT_DIR = ROOT / "assets" / "pdf"

# The site links to the English file, so its name must not drift.
# GitHub Pages is case-sensitive: keep this exact casing.
OUT_NAME = {"en": "Hafid_Idrissi_CV.pdf", "fr": "Hafid_Idrissi_CV_FR.pdf"}

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "google-chrome", "chromium", "chromium-browser",
]

CSS = """
@page { size: A4; margin: 11mm 13mm 10mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  margin: 0; font-family: "Inter", "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 9pt; line-height: 1.34; color: #14161a; background: #fff;
}
a { color: inherit; text-decoration: none; }

/* ── header ── */
.hdr { border-bottom: 1.4pt solid #14161a; padding-bottom: 4.5pt; margin-bottom: 6.5pt; }
.hdr h1 { margin: 0; font-size: 18pt; letter-spacing: -.02em; font-weight: 700; }
.hdr .role { margin: 1pt 0 0; font-size: 10.2pt; color: #d1440f; font-weight: 600; letter-spacing: -.01em; }
.hdr .loc { margin: 2pt 0 0; font-size: 8.4pt; color: #5a6270; }
.hdr .meta { margin: 3pt 0 0; font-size: 8.2pt; color: #3a4048; }
.hdr .meta span { white-space: nowrap; }
.hdr .meta .sep { color: #b6bcc5; margin: 0 5pt; }

/* ── sections ── */
h2 {
  margin: 6.5pt 0 3.5pt; font-size: 8.2pt; font-weight: 700; letter-spacing: .13em;
  text-transform: uppercase; color: #d1440f;
  border-bottom: .6pt solid #dcdfe4; padding-bottom: 1.8pt;
}
h2:first-of-type { margin-top: 0; }
p.profile { margin: 0; text-align: justify; }

/* ── skills ── */
table.skills { width: 100%; border-collapse: collapse; }
table.skills td { padding: 1.2pt 0; vertical-align: top; }
table.skills td.k { width: 30mm; font-weight: 650; color: #14161a; padding-right: 4pt; }
table.skills td.v { color: #33383f; }

/* ── experience ── */
.xp { margin-bottom: 4.5pt; page-break-inside: avoid; break-inside: avoid; }
.xp .top { display: flex; align-items: baseline; gap: 6pt; }
.xp .role { font-size: 10pt; font-weight: 700; letter-spacing: -.01em; }
.xp .dates { margin-left: auto; font-size: 8.2pt; color: #5a6270; white-space: nowrap; }
.xp .org { font-size: 9pt; color: #33383f; margin-top: .5pt; }
.xp .org b { font-weight: 650; color: #14161a; }
.xp .org .sep { color: #b6bcc5; margin: 0 4pt; }
.badge {
  display: inline-block; font-size: 6.9pt; font-weight: 700; letter-spacing: .07em;
  text-transform: uppercase; padding: 1pt 3.6pt; border-radius: 2pt;
  border: .6pt solid currentColor; vertical-align: 1.5pt;
}
.b-internship, .b-employment { color: #1d4ed8; }
.b-venture { color: #c2410c; }
.b-personal { color: #6d28d9; }
.b-research { color: #0f766e; }
.b-academic { color: #15803d; }

.xp ul { margin: 2.2pt 0 0; padding: 0; list-style: none; }
.xp li { position: relative; padding-left: 8pt; margin-bottom: 1pt; text-align: justify; }
.xp li::before {
  content: ""; position: absolute; left: 1pt; top: 4.6pt;
  width: 3pt; height: .9pt; background: #d1440f;
}
.xp .tech { margin-top: 1.8pt; font-size: 8.1pt; color: #5a6270; }
.xp .note { margin-top: 2pt; font-size: 8pt; color: #6b7280; font-style: italic; }

.other { margin-top: 1pt; font-size: 8.4pt; color: #33383f; text-align: justify; }
.other .k { font-weight: 700; color: #14161a; margin-right: 5pt; }

/* ── education ── */
.edu .top { display: flex; align-items: baseline; gap: 6pt; }
.edu .deg { font-size: 10pt; font-weight: 700; }
.edu .dates { margin-left: auto; font-size: 8.2pt; color: #5a6270; }
.edu .school { font-size: 9pt; color: #33383f; margin-top: .5pt; }
.edu .notes { font-size: 8.4pt; color: #5a6270; margin-top: 1.5pt; }

.langs { font-size: 9.2pt; }
.foot {
  margin-top: 6pt; padding-top: 4pt; border-top: .6pt solid #dcdfe4;
  font-size: 7.6pt; color: #7c848f;
}
"""


def render(cv, contact):
    L, T = cv["labels"], cv["types"]

    meta = '<span class="sep">·</span>'.join(
        f'<span>{v}</span>' for v in (
            contact["phone"],
            f'<a href="mailto:{contact["email"]}">{contact["email"]}</a>',
            f'<a href="https://{contact["site"]}">{contact["site"]}</a>',
            f'<a href="https://{contact["linkedin"]}">{contact["linkedin"]}</a>',
            f'<a href="https://{contact["github"]}">{contact["github"]}</a>',
        )
    )

    skills = "".join(
        f'<tr><td class="k">{escape(s["k"])}</td><td class="v">{escape(s["v"])}</td></tr>'
        for s in cv["skills"]
    )

    xps = []
    for x in cv["experience"]:
        org = f'<b>{escape(x["org"])}</b>'
        if x.get("link"):
            org = f'<b><a href="https://{x["link"]}">{escape(x["org"])}</a></b>'
        parts = [org, f'<span class="badge b-{x["type"]}">{escape(T[x["type"]])}</span>']
        if x.get("place"):
            parts.append(escape(x["place"]))
        org_line = '<span class="sep">·</span>'.join(parts)

        bullets = "".join(f"<li>{escape(b)}</li>" for b in x["bullets"])
        tech = f'<div class="tech">{escape(x["tech"])}</div>' if x.get("tech") else ""
        note = f'<div class="note">{escape(x["note"])}</div>' if x.get("note") else ""

        xps.append(f'''<div class="xp">
  <div class="top"><span class="role">{escape(x["role"])}</span><span class="dates">{escape(x["dates"])}</span></div>
  <div class="org">{org_line}</div>
  <ul>{bullets}</ul>{tech}{note}
</div>''')

    e = cv["education"]

    return f"""<!doctype html>
<html lang="{cv['lang']}">
<head>
<meta charset="utf-8" />
<title>{escape(L['page'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />
<style>{CSS}</style>
</head>
<body>

<header class="hdr">
  <h1>{escape(contact['name'])}</h1>
  <p class="role">{escape(cv['title'])}</p>
  <p class="loc">{escape(cv['location'])}</p>
  <p class="meta">{meta}</p>
</header>

<h2>{escape(L['profile'])}</h2>
<p class="profile">{escape(cv['profile'])}</p>

<h2>{escape(L['skills'])}</h2>
<table class="skills">{skills}</table>

<h2>{escape(L['experience'])}</h2>
{''.join(xps)}

<div class="other"><span class="k">{escape(cv['other']['k'])}</span>{escape(cv['other']['v'])}</div>

<h2>{escape(L['education'])}</h2>
<div class="edu">
  <div class="top"><span class="deg">{escape(e['degree'])}</span><span class="dates">{escape(e['dates'])}</span></div>
  <div class="school">{escape(e['school'])}<span style="color:#b6bcc5;margin:0 4pt">·</span>{escape(e['place'])}</div>
  <div class="notes">{escape(e['notes'])}</div>
</div>

<h2>{escape(L['languages'])}</h2>
<p class="langs">{escape(cv['languages'])}</p>

<p class="foot">{escape(cv['footnote'])}</p>

</body>
</html>
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
        found = shutil.which(c)
        if found:
            return found
    raise SystemExit("No Chrome or Edge binary found for PDF rendering.")


def to_pdf(html, out_path):
    chrome = find_chrome()
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "cv.html"
        src.write_text(html, encoding="utf-8")
        subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=10000", "--no-pdf-header-footer",
             f"--user-data-dir={tmp}/profile",
             f"--print-to-pdf={out_path}", src.as_uri()],
            check=True, capture_output=True, timeout=120,
        )


def page_count(pdf_path):
    """Count pages without a PDF library: /Type /Page objects in the raw file."""
    raw = Path(pdf_path).read_bytes()
    return max(raw.count(b"/Type /Page\n"), raw.count(b"/Type/Page/"), raw.count(b"/Type /Page/"))


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    contact = data["contact"]
    langs = sys.argv[1:] or ["en", "fr"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for lang in langs:
        if lang not in data:
            raise SystemExit(f"Unknown language: {lang}")
        out = OUT_DIR / OUT_NAME[lang]
        to_pdf(render(data[lang], contact), out)
        size_kb = out.stat().st_size // 1024
        print(f"  {out.relative_to(ROOT)} — {page_count(out)} page(s), {size_kb} KB")


if __name__ == "__main__":
    main()
