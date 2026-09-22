# Product preview sources

Captured on 22 September 2026 for Hafid Idrissi's portfolio and GitHub profile.
These are actual public product interfaces. No authenticated account was used.

| File | Source and context |
| --- | --- |
| `goeditpdf.jpg` | [GoEditPDF editor](https://goeditpdf.com/pages/editor.html), English UI, with a synthetic demo PDF created by the capture script. The sample contains no personal or client data. |
| `persona.jpg` | [Influence Persona](https://influencepersona.com/) public product page, with its AI-generated avatar examples. The capture is a product-page preview, not a claim that all advertised features have been validated. |
| `checkai.jpg` | [CheckAI](https://checkai-app.com/) public landing-page hero. The screenshot does not include customer logos or testimonials. |
| `tracker.jpg` | [Time Tracker's repository screenshot](https://github.com/HafidIdrissi/Time-Tracker/blob/main/assets/dashboard-preview.png), containing sample activity data. |

`python tools/capture_product_previews.py` refreshes the captures using Playwright
and Chrome. It creates its synthetic PDF in a temporary directory. Capturing
screenshots is optional development tooling; the deployed site is static.

Review future captures visually before publishing. Screenshots document the
interface as captured, and do not independently validate product claims.
