# Research Website of B. L. Alterman

This repository contains the source code for the personal academic and professional portfolio of B. L. Alterman, a research astrophysicist. The website is built as a static site using Next.js and is hosted on GitHub Pages. It is designed to be a clean, professional, and easily maintainable platform to showcase research, publications, and professional experience.

A key feature of this project is its set of automated data workflows, which use GitHub Actions to periodically fetch and process data, ensuring the content remains up-to-date with minimal manual intervention.

## Automated Data Workflows

The website relies on a series of GitHub Actions to automate content updates. Here is a breakdown of the key workflows found in the `.github/workflows/` directory:

-   **`update-ads-publications.yml`**: Runs on a weekly schedule to fetch the latest publication list from the NASA ADS API using a personal ORCID. It saves the formatted data to `public/data/ads_publications.json`.
-   **`update-ads-metrics.yml`**: Runs on a weekly schedule to fetch up-to-date citation metrics (like h-index and total citations) from the NASA ADS API. It saves the data to `public/data/ads_metrics.json`.
-   **`update_annual_citations.yml`**: Runs weekly to fetch year-by-year citation data from NASA ADS. It generates both a data file (`public/data/citations_by_year.json`) and a plot (`public/plots/citations_by_year.svg`).
-   **`convert-pdfs.yml`**: Triggers on any push to the `public/paper-figures/pdfs/` directory. It automatically converts any new or modified PDF files into SVG format and saves them in `public/paper-figures/svg/`, making them web-ready.
-   **`generate-figure-data.yml`**: Triggers whenever publication data or research project info is updated. It runs a Python script (`scripts/generate_figure_data.py`) to combine publication metadata, figure details, and license information into a single, structured file: `public/data/research-figures-with-captions.json`. This file is used to generate the detailed research subpages.
-   **`deploy.yaml`**: This is the final deployment workflow. It triggers automatically after the successful completion of any of the data-updating workflows. It builds the static Next.js site and a badge from shields.io, then deploys the output to the `gh-pages` branch, making the updated website live.

## Data Architecture and Content Pipeline

The site is built with Next.js using the App Router, which allows for a statically generated website (`output: 'export'`) that is fast, secure, and ideal for hosting on GitHub Pages. All data used to build the site is consolidated in the `/public/data` directory, which serves as the single source of truth.

Below is a breakdown of the key data files and their role in the content pipeline.

### Publication Data

-   **`ads_publications.json`**:
    -   **Origin**: Auto-generated weekly by the `update-ads-publications.yml` workflow.
    -   **Purpose**: Contains the comprehensive list of all publications from NASA ADS.
    -   **Usage**: Consumed by the **Publications Page** (`src/app/publications/page.tsx`) to build the various publication tables. It is also a key input for the `generate_figure_data.py` script.
-   **`ads_metrics.json`**:
    -   **Origin**: Auto-generated weekly by the `update-ads-metrics.yml` workflow.
    -   **Purpose**: Contains key citation statistics (h-index, total citations, etc.).
    -   **Usage**: Consumed by the **Publications Page** to display the summary metric cards.
-   **`citations_by_year.json`**:
    -   **Origin**: Auto-generated weekly by the `update_annual_citations.yml` workflow.
    -   **Purpose**: Contains yearly citation counts.
    -   **Usage**: Used by its corresponding script to generate the plot at `public/plots/citations_by_year.svg`.

### Research Content Data

-   **`research-projects.json`**:
    -   **Origin**: Manually curated.
    -   **Purpose**: Defines the title, description, and slug for each featured research project.
    -   **Usage**: Consumed by the main **Research Page** (`src/app/research/page.tsx`) to create the grid of featured research cards.
-   **`research-figures.json`**:
    -   **Origin**: Manually curated.
    -   **Purpose**: Maps a research project's slug (e.g., `proton-beams`) to the source path, caption, and alt text for its representative figure.
    -   **Usage**: It is a key input for the `scripts/generate_figure_data.py` script. The script uses this file to find the correct figure for each research topic before combining it with publication data to generate the final `research-figures-with-captions.json`.
-   **`research-paragraphs.json`**:
    -   **Origin**: Manually curated.
    -   **Purpose**: Provides the detailed introductory paragraph for each individual research subpage.
    -   **Usage**: Consumed by each research subpage (e.g., `src/app/research/coulomb-collisions/page.tsx`) to display its main descriptive text.
-   **`research-figures-with-captions.json`**:
    -   **Origin**: Auto-generated by the `generate-figure-data.yml` workflow.
    -   **Purpose**: This is the final, processed data file for research figures. It combines figure metadata with publication and citation info to generate rich, complete captions.
    -   **Usage**: Consumed by each individual research subpage to display the correct figure and its fully formatted caption, including links and attribution.

### Experience Data

-   **`education.json` & `positions.json`**:
    -   **Origin**: Manually curated.
    -   **Purpose**: Contain structured data about academic degrees and professional history.
    -   **Usage**: Consumed by the **Experience Page** (`src/app/experience/page.tsx`) to populate the education and professional position cards.


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
