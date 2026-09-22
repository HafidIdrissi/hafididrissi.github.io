#!/usr/bin/env python3
"""Capture public product interfaces for the portfolio; never uses an account.

GoEditPDF is shown with a synthetic demo document. Time Tracker's dashboard
is the sample screenshot published in its own repository. No private data.
Requires Playwright and Chrome; this is optional tooling, not a site dependency.
"""
from pathlib import Path
import tempfile
import urllib.request
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'products'
DEMO = '''<!doctype html><html><style>
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;padding:68px;background:#fcfcf8;color:#17251f;font:15px/1.8 Arial,sans-serif}.eyebrow{font-size:10px;letter-spacing:3px;color:#587254}h1{font-size:60px;line-height:1.06;letter-spacing:-3px;margin:50px 0 25px;font-weight:600}h1 span{color:#587254}.line{height:1px;background:#ced8c9;margin:36px 0}.label{font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#587254}.row{display:flex;justify-content:space-between;gap:30px}h2{font-size:24px;font-weight:500;margin:24px 0 8px}.box{background:#ecf1e6;border-radius:10px;padding:22px;margin-top:30px}.footer{position:absolute;bottom:55px;left:68px;right:68px;font-size:10px;color:#667060;display:flex;justify-content:space-between}</style>
<body><div class="row"><span class="eyebrow">GOEDITPDF / DEMO DOCUMENT</span><span class="eyebrow">01</span></div><h1>Good ideas.<br><span>Better documents.</span></h1><p>A sample brief for exploring browser-based PDF editing.<br>Open it. Make it yours. Keep it on your device.</p><div class="line"></div><div class="row"><div><span class="label">01 / Review</span><h2>Start with the brief.</h2><p>Read, reorder and annotate<br>your pages in one place.</p></div><div><span class="label">02 / Refine</span><h2>Add your perspective.</h2><p>Insert text and signatures.<br>Export when you are ready.</p></div></div><div class="box"><span class="label">Your workspace</span><p>This is a synthetic sample document created for<br>the portfolio preview. It contains no personal data.</p></div><div class="footer"><span>Sample document / Portfolio preview</span><span>GOEDITPDF.COM</span></div></body></html>'''


def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='hafid-product-') as scratch:
        scratch = Path(scratch)
        with sync_playwright() as p:
            browser = p.chromium.launch(channel='chrome', headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 960}, color_scheme='light', reduced_motion='reduce')
            page.set_content(DEMO)
            page.pdf(path=str(scratch/'demo.pdf'), print_background=True, prefer_css_page_size=True)
            page.goto('https://goeditpdf.com/', wait_until='networkidle')
            page.locator('#langSelect').select_option('en')
            page.goto('https://goeditpdf.com/pages/editor.html', wait_until='networkidle')
            page.locator('#fileInput').set_input_files(scratch/'demo.pdf')
            page.wait_for_function('document.querySelectorAll("canvas").length > 0')
            page.locator('#toast').wait_for(state='hidden')
            page.locator('#zoomOutBtn').click(click_count=2, delay=350)
            page.wait_for_timeout(700)
            page.screenshot(path=str(OUT/'goeditpdf.jpg'), type='jpeg', quality=88)

            page.set_viewport_size({'width':1440,'height':940})
            page.goto('https://influencepersona.com/', wait_until='networkidle')
            decline = page.get_by_role('button', name='Decline', exact=True)
            if decline.is_visible():
                decline.click()
            page.screenshot(path=str(OUT/'persona.jpg'), type='jpeg', quality=88)

            page.set_viewport_size({'width':1440,'height':600})
            page.goto('https://checkai-app.com/', wait_until='networkidle')
            # Only the product's hero, without customer-logo or testimonial sections.
            page.screenshot(path=str(OUT/'checkai.jpg'), type='jpeg', quality=88)

            url='https://raw.githubusercontent.com/HafidIdrissi/Time-Tracker/main/assets/dashboard-preview.png'
            with urllib.request.urlopen(url, timeout=20) as response:
                (scratch/'tracker.png').write_bytes(response.read())
            page.set_viewport_size({'width':1060,'height':845})
            page.goto((scratch/'tracker.png').as_uri())
            page.screenshot(path=str(OUT/'tracker.jpg'), type='jpeg', quality=90)
            browser.close()
    print('Captured four product previews in assets/products/.')


if __name__=='__main__':
    main()
