# Personal Academic Website of B. L. Alterman

[![Developed with Firebase](httpss://img.shields.io/badge/Developed%20with-Firebase-orange?logo=firebase&logoColor=white)](https://firebase.google.com/)

This repository contains the source code for the personal academic and professional portfolio of B. L. Alterman, a research astrophysicist. The website is built as a static site using Next.js and is hosted on GitHub Pages. It is designed to be a clean, professional, and easily maintainable platform to showcase research, publications, and professional experience.

A key feature of this project is its set of automated data workflows, which use GitHub Actions to periodically fetch and process data, ensuring the content remains up-to-date with minimal manual intervention.

## Automated Data Workflows

The website relies on a series of GitHub Actions to automate content updates, primarily from the NASA Astrophysics Data System (ADS).

### Publication & Citation Workflow

- **What it does:** Automatically fetches publication lists, citation counts, and author metrics from the NASA ADS API.
- **How it works:**
    1.  A set of scheduled GitHub Actions (e.g., `update-ads-publications.yml`, `update-ads-metrics.yml`) run on a weekly basis.
    2.  These actions execute Python scripts located in the `/scripts` directory (e.g., `fetch_ads_publications_to_data_dir.py`, `fetch_ads_metrics_to_data_dir.py`).
    3.  The scripts query the NASA ADS API using a personal developer key and ORCID.
    4.  The retrieved data is processed and saved as JSON files (`ads_publications.json`, `ads_metrics.json`) in the `/public/data` directory.
    5.  The updated JSON files are then committed back to the repository, triggering a new deployment.

### Research Figure Workflow

- **What it does:** Automates the generation of figure captions and converts figures from PDF to SVG format for the web.
- **How it works:**
    1.  **SVG Conversion:** The `convert-pdfs.yml` workflow watches the `public/paper-figures/pdfs/` directory. When a new PDF is added, it automatically converts it to an SVG and saves it in `public/paper-figures/svg/`.
    2.  **Caption Generation:** The `generate-figure-data.yml` workflow runs when publication data is updated. It executes the `scripts/generate_figure_data.py` script, which combines publication metadata (from `ads_publications.json`) with figure-specific information (from `captions-bibcodes.json`) to generate the final `data/research-figures-with-captions.json` file. This file contains the complete, cited captions used on the research subpages.

## Website Architecture

The site is built with Next.js using the App Router, which allows for a statically generated website (`output: 'export'`) that is fast, secure, and ideal for hosting on GitHub Pages.

### Publications Page

- **File:** `src/app/publications/page.tsx`
- **How it works:** At build time, this page reads the `ads_publications.json` and `ads_metrics.json` files directly from the filesystem. It then uses this data to statically render the tables of publications, ensuring the page is generated with the latest information fetched by the GitHub Actions.

### Research Pages

- **Files:** `src/app/research/page.tsx` (main page) and `src/app/research/[slug]/page.tsx` (subpages).
- **How it works:**
    - The main research page reads from `data/research-projects.json` to create the grid of featured research cards.
    - Each individual research subpage (e.g., `/research/turbulence`) is a dynamic route. At build time, Next.js reads from `data/research-paragraphs.json` and `data/research-figures-with-captions.json` to generate a static page for each research topic, complete with its descriptive text and associated figure.

## Local Development

To run the website locally, follow these steps:

1.  **Install Dependencies:**
    ```bash
    npm install
    ```

2.  **Run the Development Server:**
    ```bash
    npm run dev
    ```

This will start the Next.js development server, typically on `http://localhost:9002`.
