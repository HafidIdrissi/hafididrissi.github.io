<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/HafidIdrissi/HafidIdrissi/main/assets/profile-header-dark.svg" />
  <img src="https://raw.githubusercontent.com/HafidIdrissi/HafidIdrissi/main/assets/profile-header-light.svg" alt="Hafid Idrissi — Full-stack and cloud software engineer. From interface to infrastructure." width="100%" />
</picture>

**[Explore my portfolio](https://hafididrissi.github.io/)** · **[Download my CV](https://hafididrissi.github.io/assets/pdf/Hafid_Idrissi_CV.pdf)** · [LinkedIn](https://www.linkedin.com/in/hafid-idrissi/) · [Email](mailto:idrissihafez@gmail.com)

I build products and the systems behind them: interfaces, APIs, data models, cloud infrastructure and delivery workflows. My background combines **industrial R&D at Hager Group and Mirion Technologies** with independently built SaaS products and tools that keep data on the user's device.

I graduated from **JUNIA / HEI** with a French engineering degree, master's grade, in 2024. Based in the Paris region, I’m open to **full-stack, cloud and applied AI engineering roles** — permanent or freelance, across France and Europe.

## Selected engineering work

### Hager Group · Private cloud architecture for IoT

*Final-year internship · April–October 2024*

The question: could existing IoT APIs run securely on Azure Kubernetes Service inside a private network?

- **Designed the proof of concept:** three Azure virtual networks, VNet Peering and Private Endpoints connecting AKS, virtual machines and Azure SQL.
- **Worked through deployment constraints:** containerised .NET APIs, resolved SQL connectivity issues and addressed an ARM64/AMD64 compatibility problem.
- **Made the proposal reviewable:** validation testing and a monthly infrastructure cost estimate, with assumptions and limitations documented.

`Azure` `Kubernetes` `Docker` `Azure SQL` `.NET`

[Read the experience →](https://hafididrissi.github.io/#xp-hager)

### CheckAI · The application around the model

*Independent SaaS product · Private source*

A text classification model needs an application around it: account access, usage limits, saved results and billing.

- **Built the application flow** across a React/Vite frontend, Netlify Functions and Supabase.
- **Integrated RoBERTa inference** through Hugging Face, including handling model downtime.
- **Implemented subscription billing** with Stripe, the customer portal and webhook synchronisation; added build validation in GitHub Actions.

`React` `Netlify Functions` `Supabase` `Stripe` `Hugging Face`

[Architecture & implementation →](https://hafididrissi.github.io/#xp-checkai) · [Product](https://checkai-app.com/)

### GoEditPDF · Document processing stays in the browser

*Independent product · Public repository*

The design constraint was simple: PDF documents should not need to reach an application server.

- **Kept document processing client-side**, combining PDF.js, PDF-Lib, Fabric.js and Tesseract.js for local OCR.
- **Built the editing workflows:** merge, reorder, annotate, sign, watermark and visually redact.
- **Delivered a responsive interface** in English, French and Spanish, with help flows and tutorials.

`JavaScript` `PDF.js` `PDF-Lib` `Fabric.js` `Tesseract.js`

[Source code →](https://github.com/HafidIdrissi/goeditpdf-public) · [Try GoEditPDF](https://goeditpdf.com/)

## Start with the code: Local Time Tracker

An open-source Windows tool that records application activity and produces offline reports. **No account, cloud backend or telemetry.**

```text
Application activity  →  Local SQLite database  →  Offline HTML report
```

Automatic tracking of the foreground app, window title, browser tab and idle time; daily and seven-day summaries with categories and charts. Built with **Python, pywin32, psutil and SQLite**, with automated tests in CI.

[Browse the source](https://github.com/HafidIdrissi/Time-Tracker) · [Download a release](https://github.com/HafidIdrissi/Time-Tracker/releases/latest) · [Tests](https://github.com/HafidIdrissi/Time-Tracker/actions/workflows/tests.yml)

<sub>Windows releases include a SHA-256 checksum. The installer is not code-signed; see the repository’s <a href="https://github.com/HafidIdrissi/Time-Tracker/blob/main/SIGNING.md">signing notes</a>.</sub>

## How I approach engineering

| What matters | Where it shows up |
| :--- | :--- |
| **Start with the constraint** | Private networking at Hager; browser-only document processing in GoEditPDF. |
| **Follow through on the full flow** | Authentication, usage entitlements, billing webhooks and model-downtime handling in CheckAI. |
| **Make implementation inspectable** | Public repositories, CI tests in Time Tracker, and architecture walkthroughs for private products. |
| **Be precise about project maturity** | Industry proofs of concept, independent products and research prototypes are labelled separately. |

## More of my work

| Project | Engineering focus | Stage |
| :--- | :--- | :--- |
| [**Mirion Technologies**](https://hafididrissi.github.io/#xp-mirion) | Real-time 2D LiDAR/SLAM on embedded Linux, a Python operator interface and hardware compatibility decisions. | R&D internship · 2023 |
| [**Influence Persona**](https://hafididrissi.github.io/#xp-persona) | Multimodal AI workflows, PostgreSQL row-level security, Deno functions and credit-based billing. | Solo venture · launch preparation |
| [**LexiNegotiate**](https://github.com/HafidIdrissi/LexiNegotiate-) | Structured Gemini output for clause analysis, comparison and negotiation support. | Hackathon prototype; demo statistics are simulated |
| [**Bayesian Battery SOH**](https://github.com/HafidIdrissi/bayesian-soh-batteries) | Per-battery versus hierarchical inference with PyMC and NumPyro. | Research on simulated data; not validated on real cells |
| [**Smart Waste Detector**](https://github.com/HafidIdrissi/smart-waste-detector-yolo) | YOLO transfer learning, reproducible training and error analysis. | Computer vision project |
| [**CV PDF Studio**](https://github.com/HafidIdrissi/cv-pdf-studio) | Evidence-based document generation with provenance and readability checks. | Open-source tooling |

<sub>Project descriptions and stages reflect the career review of August 2026. Full experience details and additional projects are available in the <a href="https://hafididrissi.github.io/#experiences">portfolio</a>.</sub>

## Technical toolkit

| Area | Technologies used in my work |
| :--- | :--- |
| **Product & application** | TypeScript · JavaScript · React · Vite · Python · REST APIs |
| **Cloud & delivery** | Azure · AKS · Docker · Kubernetes · GitHub Actions · Linux |
| **Data & services** | PostgreSQL · Supabase · SQLite · Stripe · Deno |
| **Applied AI & embedded** | Hugging Face · PyTorch · PyMC · OpenCV · ROS · MQTT |

---

## A product to build. A system to figure out.

I’m interested in teams where I can contribute across the product, discuss technical tradeoffs and learn from experienced engineers. I can walk you through the code, the architecture and the decisions behind the projects above.

**[Let’s talk →](mailto:idrissihafez@gmail.com)** · [LinkedIn](https://www.linkedin.com/in/hafid-idrissi/) · [Portfolio](https://hafididrissi.github.io/) · [CV in English](https://hafididrissi.github.io/assets/pdf/Hafid_Idrissi_CV.pdf)

<sub>Paris region, France · French (native) · English (professional)</sub>
