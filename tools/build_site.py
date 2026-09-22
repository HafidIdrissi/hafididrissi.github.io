#!/usr/bin/env python3
"""Render the data-driven sections of index.html as static HTML.

Source of truth: data/cv-site.json, itself derived from
Documents/Thèses/cv_master_Hafid_IDRISSI.json (audit of 2026-08-20).

The output is static so that the CV content is readable by search engines,
recruiting tools and printers without depending on JavaScript. The remaining
JS handles filtering, theme preference, direct links and print state.

Usage: python tools/build_site.py
"""

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "cv-site.json"
INDEX = ROOT / "index.html"

ICON_LINK = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M9 7h8v8"/></svg>')
ICON_REPO = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="m8 6-6 6 6 6M16 6l6 6-6 6"/></svg>')
ICON_PLAY = ('<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linejoin="round"><path d="m9 7 9 5-9 5V7Z"/></svg>')


def attr(value):
    """Escape a string meant for a double-quoted HTML attribute."""
    return value.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def render_experience(xp, types):
    t = types[xp["type"]]
    role = xp["role"]
    org = xp.get("org") or role
    bullets = "".join(f"\n        <li>{b}</li>" for b in xp["bullets"])
    tags = ("\n      <div class=\"tags\">"
            + "".join(f'<span class="tag">{t2}</span>' for t2 in xp["tech"])
            + "</div>") if xp["tech"] else ""

    links = []
    if xp.get("url"):
        links.append(f'<a href="{xp["url"]}" target="_blank" rel="noopener">{ICON_LINK} Visit site</a>')
    if xp.get("repo"):
        links.append(f'<a href="{xp["repo"]}" target="_blank" rel="noopener">{ICON_REPO} Source code</a>')
    if xp.get("demo"):
        links.append(f'<a href="{xp["demo"]}" target="_blank" rel="noopener">{ICON_PLAY} Watch demo</a>')
    linkbar = f'\n      <div class="xplinks">{"".join(links)}</div>' if links else ""

    source = f'<p class="source-context">{escape(xp["src"])}</p>' if xp.get("src") else ""

    ctx = f'\n      <p class="xpctx">{xp["ctx"]}</p>' if xp.get("ctx") else ""

    return f'''    <article class="xp" id="xp-{xp["id"]}" data-group="{xp["group"]}" data-star="{1 if xp.get("star") else 0}">
      <details>
        <summary>
          <span class="xp-meta"><span class="badge">{t["label"]}</span><span class="xpdate">{xp["dates"]}</span></span>
          <span class="xp-heading"><strong class="xp-title">{org}</strong><span class="xp-role">{role}</span></span>
        </summary>
        <div class="xp-content">{ctx}
        <ul>{bullets}
        </ul>{tags}{linkbar}{source}
        </div>
      </details>
    </article>'''


def render_filters(filters, experiences):
    counts = {"all": len(experiences), "star": sum(1 for x in experiences if x.get("star"))}
    for x in experiences:
        counts[x["group"]] = counts.get(x["group"], 0) + 1
    out = []
    for i, f in enumerate(filters):
        pressed = "true" if i == 0 else "false"
        out.append(f'    <button class="fbtn" data-f="{f["k"]}" aria-pressed="{pressed}">'
                   f'{f["label"]}<span class="n">{counts.get(f["k"], 0)}</span></button>')
    return "\n".join(out)


def render_repo(r):
    return f'''    <a class="repo" href="https://github.com/HafidIdrissi/{r["n"]}" target="_blank" rel="noopener" data-repo="{r["n"]}">
      <span class="rname">{ICON_REPO}{r["n"]}</span>
      <p>{r["d"]}</p>
      <span class="rfoot">
        <span>{r["l"]}</span><span>View repository ↗</span>
      </span>
    </a>'''


def render_work(work, experiences):
    """Render concise case studies linked to the full, sourced experience."""
    xp = next(x for x in experiences if x["id"] == work["experience"])
    nodes = '<span class="diagram-arrow" aria-hidden="true">→</span>'.join(
        f'<span class="diagram-node">{escape(node)}</span>' for node in work["flow"])
    details = ''.join(f'<div class="case-detail"><dt>{escape(label)}</dt><dd>{escape(work[key])}</dd></div>'
                      for label, key in [("The challenge", "challenge"), ("My contribution", "contribution"), ("The result", "result")])
    extra = (f'<a class="text-link" href="{attr(xp["repo"])}" target="_blank" rel="noopener">Source code ↗</a>'
             if xp.get("repo") else "")
    product_link = (f'<a class="text-link product-link" href="{attr(xp["url"])}" target="_blank" rel="noopener">Open product <span aria-hidden="true">↗</span></a>'
                    if xp.get("url") and work.get("preview") else "")
    visual = f'<div class="diagram-flow" aria-label="{escape(" to ".join(work["flow"]), quote=True)}">{nodes}</div>'
    if work.get("preview"):
        visual = (f'<img class="product-screenshot" src="{attr(work["preview"])}" '
                  f'alt="{attr(work["preview_alt"])}" width="1440" height="{work["preview_height"]}" loading="lazy" />')
    elif xp['id'] == 'hager':
        visual = ('<div class="cloud-blueprint"><p>Private by design.</p>' + visual +
                  '<div class="network-boundary"><span>VNet peering</span><span>Private endpoints</span></div></div>')
    return f'''<article class="work-card" data-project="{xp['id']}">
      <div class="work-visual{' has-preview' if work.get('preview') else ''}">
        <div class="visual-label"><span>{escape(work["discipline"])}</span><span>{escape(work["number"])}</span></div>
        {visual}
        <p class="visual-caption">{escape(work["caption"])}</p>
      </div>
      <div class="work-body"><p class="work-type">{escape(work["stage"])}</p><h3>{xp["org"]}</h3>
        <p class="work-subtitle">{escape(work["highlight"])}</p>
        <details class="case-study"><summary>Behind the build <span aria-hidden="true">+</span></summary><dl>{details}</dl></details>
        <div class="work-links">{product_link}<a class="text-link" href="#xp-{xp["id"]}">Technical details <span aria-hidden="true">↗</span></a>{extra}</div>
      </div>
    </article>'''


def splice(html, marker, body):
    """Replace whatever sits between <!--MARKER:START--> and <!--MARKER:END-->."""
    pattern = re.compile(
        rf"(<!--{marker}:START-->).*?(<!--{marker}:END-->)", re.DOTALL)
    if not pattern.search(html):
        raise SystemExit(f"Marker {marker} not found in index.html")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n  {m.group(2)}", html)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    xps, types = data["experiences"], data["types"]

    html = INDEX.read_text(encoding="utf-8-sig")
    html = splice(html, "WORK", "\n".join(render_work(w, xps) for w in data["selected_work"]))
    html = splice(html, "FILTERS", render_filters(data["filters"], xps))
    html = splice(html, "TIMELINE", "\n".join(render_experience(x, types) for x in xps))
    repo_by_name = {r["n"]: r for r in data["repos"]}
    html = splice(html, "REPOS", "\n".join(render_repo(repo_by_name[n]) for n in data["featured_repos"]))
    INDEX.write_text(html, encoding="utf-8")

    starred = sum(1 for x in xps if x.get("star"))
    verified = sum(1 for x in xps if x.get("verified"))
    print(f"index.html rebuilt — {len(xps)} experiences "
          f"({starred} selected, {verified} verified), {len(data['featured_repos'])} featured repositories.")


if __name__ == "__main__":
    main()
