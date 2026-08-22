# hafididrissi.github.io

CV and portfolio of **Hafid Idrissi** — Full-Stack & Cloud software engineer.
Live at **[hafididrissi.github.io](https://hafididrissi.github.io/)**

## Principle

The site content is derived from an **audited CV master** (`cv_master_Hafid_IDRISSI.json`, kept outside this
repository) in which every entry carries a validation status. The governing rule, taken from that file:

> Never invent, extrapolate or strengthen a fact that is absent from the source file.
> Only reuse a figure if it appears explicitly in a validated entry, and keep its context.

Entries checked against a primary source — a code repository, an internship report, a contract, a diploma —
are marked **Verified** on the site, with the source in a tooltip.

Following the master file's `schema_section_unique` rule, the site presents **a single "Experience" section**:
personal, entrepreneurial, academic and research projects all appear there with an explicit type label, and
are never presented as salaried employment.

## Structure

```
index.html            single page — CSS and JS inlined, no dependency beyond Google Fonts
data/cv-site.json     source of truth for the content (experience, repositories, filters)
tools/build_site.py   renders data/cv-site.json into static HTML inside index.html
assets/pdf/           downloadable CV
assets/*.svg          animated banners for the GitHub profile README

github-profile-README.md          working copy of github.com/HafidIdrissi/HafidIdrissi's README
github-profile-snake-workflow.yml working copy of that repository's .github/workflows/snake.yml
```

## Editing the content

1. Edit `data/cv-site.json`.
2. Rebuild the page:

   ```bash
   python tools/build_site.py
   ```

3. Check it locally:

   ```bash
   python -m http.server 8777
   # http://127.0.0.1:8777/
   ```

Rendering is **static**: the CV content is present in the served HTML, so it is readable by search engines,
recruiting tools and printers. JavaScript only handles experience filtering, the theme toggle, scroll reveals
and an optional refresh of the GitHub star counts — the page is complete without it.

## Design decisions

- Single page, no framework and no front-end build: nothing to install in order to serve the site.
- Light and dark themes following the system preference, with the toggle remembered in `localStorage`.
- Experience filters by nature — selected, industry, products, research, academic.
- `prefers-reduced-motion` respected, and a `<noscript>` fallback that reveals all content.

## Note on asset paths

GitHub Pages is case-sensitive while Windows is not. The CV is tracked as
`assets/pdf/Hafid_Idrissi_CV.pdf` — keep that exact casing in any link, or the file 404s in production
while working fine locally.

## Licence

The page code is reusable; the CV content, documents and personal imagery are not.
