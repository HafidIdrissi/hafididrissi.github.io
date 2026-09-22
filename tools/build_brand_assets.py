#!/usr/bin/env python3
"""Build the self-hosted, motion-free profile banners and sharing artwork.

The SVGs have no external fonts or dependencies. To rasterise the sharing SVG,
open it at 1200x630 in a browser and save a screenshot as social-preview.png.
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / 'assets'


def banner(dark=False, social=False):
    bg, ink, muted, accent, line, panel = (
        ('#141c19', '#edf0e7', '#b0bcb0', '#f39b76', '#364339', '#202c25') if dark else
        ('#f6f5f0', '#202b27', '#59635b', '#b84628', '#d9ddd3', '#ecefe7'))
    height = 630 if social else 400
    offset = 95 if social else 0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">
<title id="title">Hafid Idrissi — Software Engineer</title>
<desc id="desc">From interface to infrastructure. Full-stack products, cloud architecture and embedded systems.</desc>
<rect width="1200" height="{height}" rx="12" fill="{bg}"/>
<g transform="translate(0 {offset})" font-family="Arial, Helvetica, sans-serif">
  <circle cx="61" cy="55" r="4" fill="{accent}"/>
  <text x="77" y="60" fill="{muted}" font-size="13" letter-spacing="2">HAFID IDRISSI / SOFTWARE ENGINEER</text>
  <text x="55" y="151" fill="{ink}" font-size="59" letter-spacing="-2.4">From interface</text>
  <text x="55" y="219" fill="{accent}" font-size="59" letter-spacing="-2.4">to infrastructure.</text>
  <text x="58" y="266" fill="{muted}" font-size="16">Full-stack products. Cloud architecture. Embedded systems.</text>
  <line x1="58" y1="312" x2="1142" y2="312" stroke="{line}"/>
  <text x="58" y="350" fill="{ink}" font-size="13">HAGER GROUP <tspan fill="{muted}">/ Cloud &amp; IoT internship</tspan></text>
  <text x="465" y="350" fill="{ink}" font-size="13">MIRION <tspan fill="{muted}">/ Embedded R&amp;D internship</tspan></text>
  <text x="888" y="350" fill="{ink}" font-size="13">JUNIA <tspan fill="{muted}">/ Engineering degree</tspan></text>
  <g transform="translate(805 65)">
    <path d="M156 41v175" stroke="{line}" stroke-width="2"/>
    <rect x="0" y="0" width="312" height="52" rx="6" fill="{bg}" stroke="{line}"/>
    <text x="20" y="32" fill="{muted}" font-size="11">01</text><text x="53" y="32" fill="{ink}" font-size="15">Product &amp; interface</text>
    <rect x="0" y="76" width="312" height="52" rx="6" fill="{panel}" stroke="{line}"/>
    <text x="20" y="108" fill="{muted}" font-size="11">02</text><text x="53" y="108" fill="{ink}" font-size="15">Application &amp; data</text>
    <rect x="0" y="152" width="312" height="52" rx="6" fill="{bg}" stroke="{accent}"/>
    <text x="20" y="184" fill="{accent}" font-size="11">03</text><text x="53" y="184" fill="{ink}" font-size="15">Infrastructure &amp; delivery</text>
  </g>
</g>
{'<text x="58" y="560" fill="' + muted + '" font-family="Arial, sans-serif" font-size="18">hafididrissi.github.io</text>' if social else ''}
</svg>'''


if __name__ == '__main__':
    for dark in (False, True):
        (ASSETS / f'profile-header-{"dark" if dark else "light"}.svg').write_text(banner(dark), encoding='utf-8')
    (ASSETS / 'social-preview.svg').write_text(banner(social=True), encoding='utf-8')
    print('Built two profile banners and social-preview.svg.')
