#!/usr/bin/env python3
"""Generate script-free, animated SVG diagrams for the GitHub profile.

Each asset includes a reduced-motion mode and an explicit still version for
picture sources. Optional --profile-root syncs only the
generated assets into the separate profile repository.
"""
import argparse
from pathlib import Path
import shutil

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
PALETTES = {
    'light': ('#f6f5f0', '#202b27', '#59635b', '#b84628', '#d9ddd3', '#ecefe7'),
    'dark': ('#141c19', '#edf0e7', '#b0bcb0', '#f39b76', '#364339', '#202c25'),
}


def frame(body, theme, width, height, label, still=False):
    bg, ink, muted, accent, line, panel = PALETTES[theme]
    style = f'''
      text{{font-family:Arial,Helvetica,sans-serif;fill:{ink}}}
      .muted{{fill:{muted}}}.accent{{fill:{accent}}}.line{{stroke:{line};fill:none}}
      .panel{{fill:{panel};stroke:{line}}}.paper{{fill:{bg};stroke:{line}}}
      .flow{{fill:none;stroke:{accent};stroke-width:2;stroke-dasharray:6 14;animation:flow 4s linear infinite}}
      .float{{animation:float 6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
      .late{{animation-delay:-3s}}.orbit{{animation:orbit 30s linear infinite;transform-origin:970px 165px}}
      .bar{{transform-box:fill-box;transform-origin:bottom;animation:bar 4s ease-in-out infinite}}
      .scan{{animation:scan 5s ease-in-out infinite}}.breathe{{animation:breathe 5s ease-in-out infinite}}
      @keyframes flow{{to{{stroke-dashoffset:-80}}}}
      @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
      @keyframes orbit{{to{{transform:rotate(360deg)}}}}
      @keyframes bar{{0%,100%{{transform:scaleY(.55)}}50%{{transform:scaleY(1)}}}}
      @keyframes scan{{0%,100%{{transform:translateY(0);opacity:.45}}50%{{transform:translateY(44px);opacity:1}}}}
      @keyframes breathe{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
      @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
      {'*{animation:none!important}' if still else ''}
    '''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
      <title id="title">{label}</title><style>{style}</style>
      <rect width="{width}" height="{height}" rx="12" fill="{bg}"/>{body}</svg>'''


def header(theme, still=False):
    bg, ink, muted, accent, line, panel = PALETTES[theme]
    return frame(f'''
      <circle class="accent breathe" cx="60" cy="54" r="4"/>
      <text x="77" y="59" font-size="12" letter-spacing="2.3" class="muted">FULL-STACK &amp; CLOUD ENGINEER</text>
      <text x="55" y="152" font-size="76" font-weight="600" letter-spacing="-3.5">Hafid Idrissi<tspan class="accent">.</tspan></text>
      <text x="59" y="200" font-size="26" class="muted">Ideas into products. Code into systems.</text>
      <g font-size="13"><rect class="panel" x="58" y="232" width="89" height="32" rx="16"/><text x="80" y="253">Python</text>
      <rect class="panel" x="157" y="232" width="115" height="32" rx="16"/><text x="177" y="253">TypeScript</text>
      <rect class="panel" x="282" y="232" width="82" height="32" rx="16"/><text x="305" y="253">Azure</text>
      <rect class="panel" x="374" y="232" width="112" height="32" rx="16"/><text x="391" y="253">Kubernetes</text></g>
      <g opacity=".65"><circle class="line" cx="970" cy="165" r="113"/><circle class="line" cx="970" cy="165" r="77"/>
      <g class="orbit"><circle cx="970" cy="165" r="113" fill="none" stroke="{accent}" stroke-width="1.5" stroke-dasharray="36 674"/>
      <circle cx="1083" cy="165" r="4" fill="{accent}"/></g></g>
      <path class="flow" d="M813 189H916Q930 189 930 174V165H970M970 165V90M970 165H1060V244"/>
      <circle cx="970" cy="165" r="39" fill="{panel}" stroke="{line}"/>
      <text x="949" y="179" font-size="39" font-weight="bold" letter-spacing="-3">hi<tspan class="accent">.</tspan></text>
      <g class="float"><rect class="paper" x="861" y="52" width="167" height="42" rx="8"/>
      <circle cx="882" cy="73" r="4" fill="{accent}"/><text x="898" y="78" font-size="13">Product thinking</text></g>
      <g class="float late"><rect class="paper" x="755" y="169" width="129" height="42" rx="8"/>
      <text x="776" y="195" font-size="13">Clean APIs</text></g>
      <g class="float"><rect class="paper" x="980" y="238" width="159" height="42" rx="8"/>
      <text x="1002" y="264" font-size="13">Cloud systems</text></g>
      <path class="line" d="M58 308H1142"/>
      <g font-size="12"><text x="58" y="341">HAGER GROUP<tspan class="muted" x="58" dy="20">Cloud &amp; IoT internship</tspan></text>
      <text x="452" y="341">MIRION TECHNOLOGIES<tspan class="muted" x="452" dy="20">Embedded R&amp;D internship</tspan></text>
      <text x="927" y="341">JUNIA / HEI<tspan class="muted" x="927" dy="20">Engineering degree · 2024</tspan></text></g>
    ''', theme, 1200, 400, 'Hafid Idrissi. Full-stack and cloud engineer. Hager, Mirion and JUNIA.', still)


def project(slug, theme, still=False):
    bg, ink, muted, accent, line, panel = PALETTES[theme]
    if slug == 'tracker':
        art = f'''
        <path class="flow" d="M170 89H231M331 89H390"/>
        <rect class="paper" x="36" y="36" width="135" height="107" rx="8"/>
        <g fill="{accent}"><rect class="bar" x="59" y="77" width="15" height="39" rx="3"/>
        <rect class="bar late" x="85" y="59" width="15" height="57" rx="3"/><rect class="bar" style="animation-delay:-1s" x="111" y="69" width="15" height="47" rx="3"/></g>
        <rect class="panel" x="231" y="47" width="100" height="81" rx="8"/>
        <ellipse cx="281" cy="64" rx="27" ry="9" fill="none" stroke="{muted}"/>
        <path d="M254 64v39c0 12 54 12 54 0V64m-54 20c0 12 54 12 54 0" fill="none" stroke="{muted}"/>
        <g class="float"><rect class="paper" x="390" y="36" width="132" height="107" rx="8"/>
        <path d="M411 65h70m-70 18h90m-90 18h52" stroke="{line}" stroke-width="5" stroke-linecap="round"/>
        <path d="M490 109l7 7 14-17" stroke="{accent}" stroke-width="3" fill="none"/></g>
        <g font-size="11" class="muted" text-anchor="middle"><text x="103" y="170">ACTIVITY</text><text x="281" y="170">LOCAL SQLITE</text><text x="455" y="170">OFFLINE REPORT</text></g>'''
    elif slug == 'pdf':
        art = f'''
        <rect class="panel" x="98" y="26" width="362" height="137" rx="12"/>
        <g class="float late"><rect class="paper" x="145" y="43" width="80" height="103" rx="5"/><path d="M162 70h44m-44 14h35m-35 14h44" stroke="{line}" stroke-width="4"/></g>
        <g class="float"><rect class="paper" x="242" y="37" width="80" height="103" rx="5"/><path d="M259 64h44m-44 14h35m-35 14h44" stroke="{line}" stroke-width="4"/>
        <path class="scan" d="M250 59h64" stroke="{accent}" stroke-width="3"/></g>
        <g class="float late"><rect class="paper" x="339" y="43" width="80" height="103" rx="5"/><path d="M356 70h44m-44 14h35" stroke="{line}" stroke-width="4"/><path d="M357 115l12 10 26-30" fill="none" stroke="{accent}" stroke-width="3"/></g>
        <text x="280" y="185" text-anchor="middle" font-size="11" class="muted">YOUR DOCUMENTS. YOUR BROWSER.</text>'''
    elif slug == 'checkai':
        art = f'''
        <path class="flow" d="M169 92H250M319 92H365V49H410M365 92H410M365 92V139H410"/>
        <rect class="paper" x="37" y="39" width="132" height="108" rx="8"/>
        <path d="M56 65h85m-85 17h70m-70 17h80" stroke="{line}" stroke-width="5" stroke-linecap="round"/>
        <rect class="breathe" x="57" y="114" width="64" height="13" rx="4" fill="{accent}"/>
        <g class="float"><rect class="panel" x="245" y="56" width="77" height="73" rx="12"/><text x="284" y="100" font-size="24" text-anchor="middle">API</text></g>
        <rect class="paper" x="410" y="32" width="111" height="33" rx="6"/><rect class="paper" x="410" y="77" width="111" height="33" rx="6"/><rect class="paper" x="410" y="123" width="111" height="33" rx="6"/>
        <g text-anchor="middle" font-size="11"><text x="465" y="53">Auth &amp; data</text><text x="465" y="98">Inference</text><text x="465" y="144">Billing</text></g>'''
    else:
        art = f'''
        <path class="flow" d="M167 92H240M320 92H398"/>
        <g class="float"><rect class="paper" x="47" y="41" width="119" height="107" rx="10"/><circle cx="107" cy="80" r="16" fill="none" stroke="{muted}" stroke-width="2"/>
        <path d="M77 129v-8a30 25 0 0 1 60 0v8" stroke="{muted}" stroke-width="2" fill="none"/></g>
        <rect class="panel" x="240" y="56" width="80" height="76" rx="12"/>
        <path class="breathe" d="M280 71l6 17 17 6-17 6-6 17-6-17-17-6 17-6z" fill="{accent}"/>
        <g class="float late"><rect class="paper" x="398" y="41" width="119" height="107" rx="10"/><path d="M445 72l31 21-31 21z" fill="none" stroke="{accent}" stroke-width="2.5"/></g>
        <g text-anchor="middle" font-size="11" class="muted"><text x="106" y="178">AVATAR</text><text x="280" y="178">GENERATE</text><text x="457" y="178">VIDEO</text></g>'''
    labels = {'tracker': 'Local Time Tracker: activity to local SQLite to offline report', 'pdf': 'GoEditPDF: local document editing and OCR', 'checkai': 'CheckAI: application, API and backend services', 'persona': 'Influence Persona: avatar, generation and video workflow'}
    return frame(art, theme, 560, 200, labels[slug], still)


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
        for slug in ('tracker', 'pdf', 'checkai', 'persona'):
            for still in (False, True):
                path = ASSETS / f'project-{slug}-{"still-" if still else ""}{theme}.svg'
                path.write_text(project(slug, theme, still), encoding='utf-8')
                generated.append(path)
    if args.profile_root:
        dest = args.profile_root.resolve() / 'assets'
        if not dest.is_dir():
            raise SystemExit(f'Profile assets directory does not exist: {dest}')
        for path in generated:
            shutil.copyfile(path, dest / path.name)
    print(f'Built {len(generated)} SVG assets' + (' and synced the profile repository.' if args.profile_root else '.'))


if __name__ == '__main__':
    main()
