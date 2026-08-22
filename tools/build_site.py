#!/usr/bin/env python3
"""Rend les sections dynamiques de index.html en HTML statique.

Source de vérité : data/cv-site.json, lui-même dérivé de
Documents/Thèses/cv_master_Hafid_IDRISSI.json (audit du 2026-08-20).

Le rendu est statique pour que le contenu du CV soit lisible par les moteurs
de recherche, les scrapers de recrutement et à l'impression, sans dépendre de
JavaScript. Le JS restant ne gère que le filtrage, le thème et le scrollspy.

Usage : python tools/build_site.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "cv-site.json"
INDEX = ROOT / "index.html"

ICON_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
              'stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>')
ICON_LINK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M9 7h8v8"/></svg>')
ICON_REPO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="m8 6-6 6 6 6M16 6l6 6-6 6"/></svg>')
ICON_PLAY = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linejoin="round"><path d="m9 7 9 5-9 5V7Z"/></svg>')
ICON_STAR = ('<svg viewBox="0 0 24 24" fill="currentColor">'
             '<path d="m12 3 2.6 5.6 6.1.8-4.5 4.2 1.2 6L12 16.8 6.6 19.6l1.2-6L3.3 9.4l6.1-.8L12 3Z"/></svg>')


def attr(value):
    """Échappe une chaîne destinée à un attribut HTML entre guillemets doubles."""
    return value.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def render_experience(xp, types):
    t = types[xp["type"]]
    role = xp["role"]
    title = (f'<a href="{xp["url"]}" target="_blank" rel="noopener">{role}</a>'
             if xp.get("url") else role)

    org = '<span class="sep">·</span>'.join(p for p in (xp.get("org"), xp.get("place")) if p)
    bullets = "".join(f"\n        <li>{b}</li>" for b in xp["bullets"])
    tags = ("\n      <div class=\"tags\">"
            + "".join(f'<span class="tag">{t2}</span>' for t2 in xp["tech"])
            + "</div>") if xp["tech"] else ""

    links = []
    if xp.get("url"):
        links.append(f'<a href="{xp["url"]}" target="_blank" rel="noopener">{ICON_LINK} Voir en ligne</a>')
    if xp.get("repo"):
        links.append(f'<a href="{xp["repo"]}" target="_blank" rel="noopener">{ICON_REPO} Code source</a>')
    if xp.get("demo"):
        links.append(f'<a href="{xp["demo"]}" target="_blank" rel="noopener">{ICON_PLAY} Démonstration</a>')
    linkbar = f'\n      <div class="xplinks">{"".join(links)}</div>' if links else ""

    verif = ""
    if xp.get("verified"):
        title_attr = f' title="{attr(xp["src"])}"' if xp.get("src") else ""
        verif = f'\n        <span class="verif"{title_attr}>{ICON_CHECK}Vérifié</span>'

    ctx = f'\n      <p class="xpctx">{xp["ctx"]}</p>' if xp.get("ctx") else ""

    return f'''    <article class="xp" id="xp-{xp["id"]}" data-group="{xp["group"]}" data-star="{1 if xp.get("star") else 0}">
      <div class="xpcard">
        <div class="xptop">
          <span class="badge {t["cls"]}">{t["label"]}</span>{verif}
          <span class="xpdate">{xp["dates"]}</span>
        </div>
        <h3>{title}</h3>
        <p class="xporg">{org}</p>{ctx}
        <ul>{bullets}
        </ul>{tags}{linkbar}
      </div>
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
    live = f'\n        <span class="live">{r["live"]}</span>' if r.get("live") else ""
    return f'''    <a class="repo" href="https://github.com/HafidIdrissi/{r["n"]}" target="_blank" rel="noopener" data-repo="{r["n"]}">
      <span class="rname">{ICON_REPO}{r["n"]}</span>
      <p>{r["d"]}</p>
      <span class="rfoot">
        <span class="lang"><i style="background:{r["lc"]}"></i>{r["l"]}</span>
        <span class="star" data-stars>{ICON_STAR}{r["s"]}</span>{live}
      </span>
    </a>'''


def splice(html, marker, body):
    """Remplace le contenu entre <!--MARKER:START--> et <!--MARKER:END-->."""
    pattern = re.compile(
        rf"(<!--{marker}:START-->).*?(<!--{marker}:END-->)", re.DOTALL)
    if not pattern.search(html):
        raise SystemExit(f"Marqueur {marker} introuvable dans index.html")
    return pattern.sub(lambda m: f"{m.group(1)}\n{body}\n  {m.group(2)}", html)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    xps, types = data["experiences"], data["types"]

    html = INDEX.read_text(encoding="utf-8")
    html = splice(html, "FILTERS", render_filters(data["filters"], xps))
    html = splice(html, "TIMELINE", "\n".join(render_experience(x, types) for x in xps))
    html = splice(html, "REPOS", "\n".join(render_repo(r) for r in data["repos"]))
    INDEX.write_text(html, encoding="utf-8")

    starred = sum(1 for x in xps if x.get("star"))
    verified = sum(1 for x in xps if x.get("verified"))
    print(f"index.html régénéré — {len(xps)} expériences "
          f"({starred} en sélection, {verified} vérifiées), {len(data['repos'])} dépôts.")


if __name__ == "__main__":
    main()
