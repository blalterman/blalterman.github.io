# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Next.js-based academic portfolio website for B. L. Alterman, a research astrophysicist. The site is statically generated and deployed to GitHub Pages, featuring an automated data pipeline that fetches research publications and metrics from NASA ADS.

## Development Commands

- **Development server**: `npm run dev` (runs on port 9002 with Turbopack)
- **Build**: `npm run build` (static export for GitHub Pages)
- **Start production**: `npm start`
- **Lint**: `npm run lint`
- **Type check**: `npm run typecheck`

## Architecture Overview

### Static Site Generation
The site uses Next.js App Router with `output: 'export'` configuration for static site generation. TypeScript and ESLint errors are ignored during builds to accommodate the automated CI/CD pipeline.

### Data Pipeline Architecture
The site operates on a data-driven architecture with all content stored in `/public/data/` as JSON files:

**Automated Data (via GitHub Actions):**
- `ads_publications.json` - Publications from NASA ADS (weekly updates)
- `ads_metrics.json` - Citation metrics and h-index (weekly updates)
- `citations_by_year.json` - Annual citation counts (weekly updates)
- `research-figures-with-captions.json` - Generated from combining manual data with publication metadata

**Manual Data:**
- `research-projects.json` - Featured research project definitions
- `research-figures.json` - Figure metadata for research projects
- `research-paragraphs.json` - Detailed descriptions for research subpages
- `education.json` & `positions.json` - Academic and professional history
- `skills.json` - Technical skills data

### Key GitHub Actions Workflows
- `update-ads-publications.yml` - Fetches publications weekly
- `update-ads-metrics.yml` - Updates citation metrics weekly
- `update_annual_citations.yml` - Generates yearly citation data and plots
- `convert-pdfs.yml` - Converts PDFs to web-ready SVGs
- `generate-figure-data.yml` - Combines research data with publication metadata
- `deploy.yaml` - Builds and deploys to gh-pages branch

### Component Structure
- **App Router Pages**: Each research topic has its own route (`/research/[topic]/page.tsx`)
- **Shadcn/ui Components**: UI components in `/src/components/ui/`
- **Custom Components**: Main application components in `/src/components/`
- **Path Aliases**: `@/*` maps to `./src/*`

### Styling
- **Tailwind CSS**: Primary styling framework with custom configuration
- **Shadcn/ui**: Component library with neutral base color theme
- **CSS Variables**: Theme customization via CSS custom properties

## Python Scripts (in `/scripts/`)
- `fetch_ads_*.py` - NASA ADS API integration scripts
- `generate_figure_data.py` - Combines research metadata with publication data
- `utils.py` - Shared utilities for path management and repository structure
- `requirements.txt` - Python dependencies for automation scripts

### Script Utilities
All Python scripts use a shared `scripts/utils.py` module that provides:
- `get_repo_root()`: Returns the repository root directory using `Path(__file__).parent.parent`
- `get_public_data_dir()`: Returns the `public/data` directory path
- `get_public_plots_dir()`: Returns the `public/plots` directory path

This ensures scripts work correctly regardless of which directory they're invoked from, eliminating path-related issues.

## Important Notes
- Site is configured for GitHub Pages deployment with asset prefix handling
- Images are unoptimized for static export compatibility
- Research subpages are dynamically generated from data files
- All external data sources are automatically updated via scheduled workflows
- Scripts only write to `public/data/` directory (no duplicate `data/` directory)