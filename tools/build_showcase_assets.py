#!/usr/bin/env python3
"""Build self-contained animated GitHub artwork from real product screenshots.

Embedded JPEGs avoid remote image/font dependencies inside SVG image contexts.
Every animated image has a separate still source for GitHub's <picture> markup.
Screenshots and their provenance live in assets/products/.
"""
import argparse
import base64
from html import escape
from pathlib import Path
import shutil

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
PALETTES = {
    'dark': dict(bg='#101313', ink='#f1f3eb', muted='#b0b8b1', accent='#d6f58b', line='#343d38', panel='#1b2722'),
    'light': dict(bg='#f5f5ef', ink='#18231d', muted='#53614f', accent='#3d642c', line='#d4dbcc', panel='#e0e9d5'),
}
PRODUCTS = {
    'pdf': ('goeditpdf.jpg', 'goeditpdf.com', 'BROWSER-BASED PDF TOOLS', 'Actual interface / Sample document', '#344737', '#d6f58b'),
    'persona': ('persona.jpg', 'influencepersona.com', 'AI CONTENT STUDIO', 'Actual interface / Public product page', '#352847', '#cbbbfc'),
    'tracker': ('tracker.jpg', 'Local Time Tracker / Windows', 'LOCAL-FIRST DESKTOP SOFTWARE', 'Actual interface / Repository sample data', '#2d4352', '#9ed6eb'),
    'checkai': ('checkai.jpg', 'checkai-app.com', 'FULL-STACK AI APPLICATION', 'Actual interface / Public product page', '#3e3852', '#d5c9fb'),
}


def screen(slug, x, y, width, height, ident, animate='float', angle=0):
    filename, domain, *_ = PRODUCTS[slug]
    data = base64.b64encode((ASSETS/'products'/filename).read_bytes()).decode('ascii')
    return f'''<g transform="translate({x} {y}) rotate({angle} {width/2} {height/2})"><g class="{animate}">
      <defs><clipPath id="{ident}"><rect width="{width}" height="{height}" rx="8"/></clipPath></defs>
      <rect x="0" y="9" width="{width}" height="{height}" rx="8" fill="#000" opacity=".2"/>
      <g clip-path="url(#{ident})"><rect width="{width}" height="{height}" fill="#eff1eb"/>
      <image href="data:image/jpeg;base64,{data}" x="0" y="23" width="{width}" height="{height-23}" preserveAspectRatio="xMidYMin slice"/>
      <circle cx="12" cy="11.5" r="2.5" fill="#d89582"/><circle cx="21" cy="11.5" r="2.5" fill="#d6bb72"/><circle cx="30" cy="11.5" r="2.5" fill="#8baa83"/>
      <text x="{width/2}" y="15" text-anchor="middle" font-size="8" fill="#45523e">{escape(domain)}</text>
      </g><rect width="{width}" height="{height}" rx="8" fill="none" stroke="#ffffff44"/>
      </g></g>'''


def frame(body, theme, width, height, title, still=False):
    p = PALETTES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
    <title id="title">{escape(title)}</title>
    <style>text{{font-family:Arial,Helvetica,sans-serif}}.ink{{fill:{p['ink']}}}.muted{{fill:{p['muted']}}}.accent{{fill:{p['accent']}}}
    .float{{animation:drift 8s ease-in-out infinite}}.float-back{{animation:drift-back 9s ease-in-out infinite}}.signal{{animation:signal 4s ease-in-out infinite}}
    @keyframes drift{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
    @keyframes drift-back{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(7px)}}}}
    @keyframes signal{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    {'*{animation:none!important}' if still else ''}</style>
    <rect width="{width}" height="{height}" rx="14" fill="{p['bg']}"/>{body}</svg>'''


def header(theme, still=False):
    p = PALETTES[theme]
    scene = screen('persona', 774, 51, 357, 222, 'back-screen', 'float-back', 6)
    scene += screen('pdf', 687, 166, 390, 237, 'front-screen', 'float', -4)
    return frame(f'''
      <rect x="650" y="27" width="520" height="382" rx="17" fill="{p['panel']}"/>
      <path d="M670 120H1150M670 220H1150M670 320H1150M760 48V390M880 48V390M1000 48V390M1120 48V390" stroke="{p['line']}" opacity=".5"/>
      <circle cx="58" cy="63" r="4" class="accent signal"/><text x="73" y="68" font-size="12" letter-spacing="2.2" class="muted">FULL-STACK &amp; CLOUD ENGINEER</text>
      <text x="51" y="163" font-size="77" letter-spacing="-4" font-weight="600" class="ink">Hafid Idrissi<tspan class="accent">.</tspan></text>
      <text x="55" y="231" font-size="38" letter-spacing="-1.8" class="ink">Built from</text>
      <text x="55" y="278" font-size="38" letter-spacing="-1.8" class="ink">the <tspan class="accent">inside out.</tspan></text>
      <text x="57" y="325" font-size="16" class="muted">Full-stack products. Cloud systems. Applied AI.</text>
      <path d="M58 361h27m-8-6 8 6-8 6" stroke="{p['accent']}" stroke-width="1.5" fill="none"/>
      <text x="98" y="366" font-size="13" class="ink">Explore the work below</text>
      {scene}
      <path d="M55 433H1145" stroke="{p['line']}"/>
      <g font-size="12"><text x="55" y="463" class="ink">HAGER GROUP<tspan x="55" dy="19" class="muted" font-size="11">Cloud &amp; IoT internship</tspan></text>
      <text x="450" y="463" class="ink">MIRION TECHNOLOGIES<tspan x="450" dy="19" class="muted" font-size="11">Embedded R&amp;D internship</tspan></text>
      <text x="935" y="463" class="ink">JUNIA / HEI<tspan x="935" dy="19" class="muted" font-size="11">Engineering degree · 2024</tspan></text></g>
    ''', theme, 1200, 510, 'Hafid Idrissi. Full-stack and cloud engineer. Real product previews of GoEditPDF and Influence Persona.', still)


def project(slug, theme, still=False):
    _, _, label, caption, color, tint = PRODUCTS[slug]
    p = PALETTES[theme]
    art = screen(slug, 27, 58, 506, 236, 'product-screen', 'float', -1.5)
    return frame(f'''
      <rect width="560" height="350" rx="14" fill="{color}"/>
      <path d="M25 45H535M25 310H535" stroke="{tint}" opacity=".16"/>
      <circle cx="29" cy="26" r="3" fill="{tint}" class="signal"/>
      <text x="42" y="30" font-size="10" letter-spacing="1.4" fill="{tint}">{label}</text>
      {art}
      <text x="27" y="333" font-size="9" fill="#e2e8e4">{caption}</text>
      <path d="M514 334l15-15m-12 0h12v12" stroke="{tint}" stroke-width="1.5" fill="none"/>
    ''', theme, 560, 350, label.title() + '. ' + caption + '.', still)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile-root', type=Path)
    args = parser.parse_args()
    generated = []
    for theme in PALETTES:
        for still in (False, True):
            path = ASSETS / f'profile-{"still" if still else "motion"}-{theme}.svg'
            path.write_text(header(theme, still), encoding='utf-8')
            generated.append(path)
            for slug in PRODUCTS:
                path = ASSETS / f'project-{slug}-{"still-" if still else ""}{theme}.svg'
                path.write_text(project(slug, theme, still), encoding='utf-8')
                generated.append(path)
    # Social sharing uses the same identity without animation.
    social = header('dark', True).replace('height="510" viewBox="0 0 1200 510"', 'height="630" viewBox="0 0 1200 630"', 1)
    social = social.replace('<rect width="1200" height="510"', '<rect width="1200" height="630"', 1)
    social = social.replace('</svg>', '<text x="55" y="570" font-family="Arial,Helvetica,sans-serif" font-size="19" fill="#b0b8b1">hafididrissi.github.io</text></svg>')
    (ASSETS / 'social-preview.svg').write_text(social, encoding='utf-8')
    if args.profile_root:
        dest = args.profile_root.resolve() / 'assets'
        if not dest.is_dir():
            raise SystemExit(f'Profile assets directory does not exist: {dest}')
        for path in generated:
            shutil.copyfile(path, dest / path.name)
    print(f'Built {len(generated)} profile images and static social artwork.' + (' Synced profile assets.' if args.profile_root else ''))


if __name__ == '__main__':
    main()
