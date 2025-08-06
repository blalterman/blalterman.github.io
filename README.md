# Personal Academic Website of B. L. Alterman

[![Developed with Firebase](/public/icons/firebase.svg?width=24&height=24)](https://firebase.google.com/)

This repository contains the source code for the personal academic and professional portfolio of B. L. Alterman, a research astrophysicist. The website is built as a static site using Next.js and is hosted on GitHub Pages. It is designed to be a clean, professional, and easily maintainable platform to showcase research, publications, and professional experience.

A key feature of this project is its set of automated data workflows, which use GitHub Actions to periodically fetch and process data, ensuring the content remains up-to-date with minimal manual intervention.

## Automated Data Workflows

The website relies on a series of GitHub Actions to automate content updates. Here is a breakdown of the key workflows found in the `.github/workflows/` directory:

-   **`update-ads-publications.yml`**: Runs on a weekly schedule to fetch the latest publication list from the NASA ADS API using a personal ORCID. It saves the formatted data to `public/data/ads_publications.json`.
-   **`update-ads-metrics.yml`**: Runs on a weekly schedule to fetch up-to-date citation metrics (like h-index and total citations) from the NASA ADS API. It saves the data to `public/data/ads_metrics.json`.
-   **`update_annual_citations.yml`**: Runs weekly to fetch year-by-year citation data from NASA ADS. It generates both a data file (`public/data/citations_by_year.json`) and a plot (`assets/images/citations_by_year.svg`).
-   **`convert-pdfs.yml`**: Triggers on any push to the `public/paper-figures/pdfs/` directory. It automatically converts any new or modified PDF files into SVG format and saves them in `public/paper-figures/svg/`, making them web-ready.
-   **`generate-figure-data.yml`**: Triggers whenever publication data or research project info is updated. It runs a Python script (`scripts/generate_figure_data.py`) to combine publication metadata, figure details, and license information into a single, structured file: `data/research-figures-with-captions.json`. This file is used to generate the detailed research subpages.
-   **`deploy.yaml`**: This is the final deployment workflow. It triggers automatically after the successful completion of any of the data-updating workflows. It builds the static Next.js site and deploys the output to the `gh-pages` branch, making the updated website live.

## Website Architecture

The site is built with Next.js using the App Router, which allows for a statically generated website (`output: 'export'`) that is fast, secure, and ideal for hosting on GitHub Pages.

### Publications Page

-   **File:** `src/app/publications/page.tsx`
-   **How it works:** At build time, this page reads the `ads_publications.json` and `ads_metrics.json` files directly from the filesystem. It then uses this data to statically render the tables of publications, ensuring the page is generated with the latest information fetched by the GitHub Actions.

### Research Pages

-   **Files:** `src/app/research/page.tsx` (main page) and individual research pages (e.g., `src/app/research/[slug]/page.tsx`).
-   **How it works:**
    -   The main research page reads from `data/research-projects.json` to create the grid of featured research cards.
    -   Each individual research subpage is generated at build time. Next.js reads from `data/research-paragraphs.json` and `data/research-figures-with-captions.json` to generate a static page for each research topic, complete with its descriptive text and associated figure.

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
