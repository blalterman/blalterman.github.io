# Architecture Documentation

> **Last Updated:** 2025-10-25
> **Purpose:** Comprehensive reference for developers and AI assistants working with this codebase
>
> **Related Documentation:**
> - [CLAUDE.md](./CLAUDE.md) - AI assistant quick reference and startup guide
> - [AGENTS.md](./docs/AGENTS.md) - AI development protocols and prompting guidelines
> - [README.md](./README.md) - Project overview for users

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Directory Structure](#directory-structure)
4. [Data Flow Architecture](#data-flow-architecture)
5. [GitHub Actions Workflows](#github-actions-workflows)
6. [Python Scripts](#python-scripts)
7. [Dynamic Route System](#dynamic-route-system)
8. [Component Architecture](#component-architecture)
9. [Data Management](#data-management)
10. [Configuration Files](#configuration-files)
11. [Development Workflow](#development-workflow)
12. [Deployment Process](#deployment-process)

---

## How to Use This Document

### Reading Paths by Role

Choose your path based on what you need:

**🎯 Quick Reference** → See [CLAUDE.md](./CLAUDE.md) for AI assistant quick start
**📋 Quick Lookup** → See [Architecture Quick Reference](./docs/architecture-quick-reference.md) for fast topic finder

**Frontend Developer**
- Start: [Component Architecture](#component-architecture)
- Then: [Dynamic Route System](#dynamic-route-system)
- Reference: [Data Management](#data-management)

**Backend/Automation Engineer**
- Start: [GitHub Actions Workflows](#github-actions-workflows)
- Then: [Python Scripts](#python-scripts)
- Reference: [Data Flow Architecture](#data-flow-architecture)

**Data Engineer/Content Manager**
- Start: [Data Management](#data-management)
- Then: [Common Tasks](#common-tasks)
- Reference: [Python Scripts](#python-scripts)

**DevOps/Site Reliability**
- Start: [Deployment Process](#deployment-process)
- Then: [Troubleshooting](#troubleshooting)
- Reference: [Configuration Files](#configuration-files)

**New Developer (First Time)**
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Directory Structure](#directory-structure)
4. [Development Workflow](#development-workflow)
5. [Common Tasks](#common-tasks)

**AI Assistant (Full Context)**
- Read entire document for comprehensive understanding

---
---

## 🏗️ Project Overview

> **Purpose:** High-level introduction to the project, its goals, and key features
>
> **When to use this section:** First-time orientation, understanding project scope
>
> **Related Sections:** [Technology Stack](#technology-stack) • [Development Workflow](#development-workflow)

---

This is a **statically-generated academic portfolio website** for B. L. Alterman, a Research Astrophysicist at NASA Goddard Space Flight Center. The site showcases research, publications, and professional experience with automated data pipelines that pull live citation metrics from NASA's Astrophysics Data System (ADS).

### Key Features

- **Automated Data Pipeline:** Weekly updates from NASA ADS API for publications and citations
- **Dynamic Route System:** Single React component generates all research subpages from JSON data
- **Static Site Generation:** Fast, secure deployment to GitHub Pages
- **Modern Stack:** Next.js 15 with App Router, TypeScript, Tailwind CSS
- **Professional Design:** Responsive, accessible, SEO-optimized
- **Zero-Maintenance Content:** Add research pages by editing JSON files only

---
---

## 🛠️ Technology Stack

> **Purpose:** Complete reference of all technologies, frameworks, and dependencies used in the project
>
> **When to use this section:** Understanding tech choices, checking versions, adding new dependencies
>
> **Related Sections:** [Configuration Files](#configuration-files) • [Development Workflow](#development-workflow)

---

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 15.5.3 | React framework with App Router |
| **React** | 18.3.1 | UI library |
| **TypeScript** | 5 | Type safety |
| **Tailwind CSS** | 3.4.1 | Utility-first styling |
| **Shadcn/ui** | Latest | Component library (based on Radix UI) |
| **KaTeX** | 0.16.22 | LaTeX math rendering |
| **Recharts** | 2.15.1 | Data visualization |
| **Lucide React** | 0.475.0 | Icon library |

### Backend/Automation

| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Data fetching and processing scripts |
| **GitHub Actions** | CI/CD automation |
| **NASA ADS API** | Publications and citation data source |
| **Poppler Utils** | PDF to SVG conversion |
| **Matplotlib** | Citation plot generation |

### Build & Development

- **Package Manager:** npm
- **Build Tool:** Turbopack (Next.js)
- **Development Server:** Port 9002
- **Static Export:** `output: 'export'` for GitHub Pages compatibility

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 📁 Directory Structure

> **Purpose:** Visual map of the entire project file and folder organization
>
> **When to use this section:** Finding where files live, understanding project layout
>
> **Related Sections:** [Component Architecture](#component-architecture) • [Data Management](#data-management) • [Python Scripts](#python-scripts)

---

```
blalterman.github.io/
├── .github/
│   └── workflows/                    # GitHub Actions automation
│       ├── update-ads-publications.yml
│       ├── update-ads-metrics.yml
│       ├── update_annual_citations.yml
│       ├── convert-pdfs.yml
│       ├── generate-figure-data.yml
│       └── deploy.yaml (implied)
│
├── src/
│   ├── app/                          # Next.js App Router pages
│   │   ├── page.tsx                  # Home page (/)
│   │   ├── layout.tsx                # Root layout with metadata
│   │   ├── globals.css               # Global Tailwind styles
│   │   ├── research/
│   │   │   ├── page.tsx              # Research overview (/research)
│   │   │   ├── [slug]/page.tsx       # Dynamic research subpages
│   │   │   └── layout.tsx
│   │   ├── publications/
│   │   │   ├── page.tsx              # Publications list
│   │   │   ├── loading.tsx
│   │   │   └── layout.tsx
│   │   └── experience/
│   │       ├── page.tsx              # Education & positions
│   │       └── layout.tsx
│   │
│   ├── components/                   # React components
│   │   ├── ui/                       # Shadcn/ui components (52 files)
│   │   ├── icons/                    # Custom SVG icons
│   │   ├── header.tsx                # Navigation header
│   │   ├── research-figure.tsx       # Figure display with captions
│   │   ├── featured-research.tsx     # Research grid
│   │   ├── research.tsx
│   │   ├── about.tsx
│   │   ├── experience.tsx
│   │   ├── contact.tsx
│   │   └── mobile-nav.tsx
│   │
│   ├── lib/                          # Utility functions
│   │   ├── data-loader.ts            # JSON data loading
│   │   ├── publication-utils.ts      # Publication filtering/sorting
│   │   ├── render-math.ts            # LaTeX rendering
│   │   └── utils.ts                  # General utilities
│   │
│   ├── hooks/                        # React hooks
│   │   └── use-toast.ts
│   │
│   └── types/                        # TypeScript interfaces
│       └── publication.ts
│
├── public/                           # Static assets
│   ├── data/                         # JSON data files
│   │   ├── ads_publications.json           # AUTO: Publications from ADS
│   │   ├── ads_metrics.json                # AUTO: Citation metrics
│   │   ├── citations_by_year.json          # AUTO: Yearly citations
│   │   ├── research-figures-with-captions.json  # AUTO: Combined figure data
│   │   ├── research-projects.json          # MANUAL: Featured research topics
│   │   ├── research-paragraphs.json        # MANUAL: Detailed descriptions
│   │   ├── page-figure-mappings.json       # MANUAL: Maps pages to figures
│   │   ├── figure-metadata.json            # MANUAL: Figure database
│   │   ├── ben-page.json                   # MANUAL: Ben page structure & content
│   │   ├── publications-categories.json    # MANUAL: Publication category definitions
│   │   ├── research-page.json              # MANUAL: Research overview content
│   │   ├── publications-page.json          # MANUAL: Publications overview content
│   │   ├── experience-page.json            # MANUAL: Experience overview content
│   │   ├── biography-homepage.json         # MANUAL: Homepage biography content
│   │   ├── education.json                  # MANUAL: Education history
│   │   ├── positions.json                  # MANUAL: Professional positions
│   │   └── skills.json                     # MANUAL: Technical skills
│   │
│   ├── paper-figures/                # Research figures
│   │   ├── pdfs/                     # Source PDF figures
│   │   └── svg/                      # Auto-converted SVG figures
│   │
│   ├── plots/                        # Generated visualizations
│   │   └── citations_by_year.svg     # AUTO: Citation trend plot
│   │
│   ├── images/                       # Static images
│   └── icons/                        # Logo and icon assets
│
├── scripts/                          # Python automation
│   ├── fetch_ads_publications_to_data_dir.py  # Fetch publications
│   ├── fetch_ads_metrics_to_data_dir.py       # Fetch metrics
│   ├── fetch_ads_citations_by_year.py         # Fetch & plot citations
│   ├── generate_figure_data.py                # Combine data sources
│   ├── create_research_page.py                # Interactive page creation
│   ├── fetch_figure_licenses.py               # License fetching
│   ├── test_create_research_page.py           # Unit tests
│   ├── utils.py                               # Shared utilities
│   └── requirements.txt                       # Python dependencies
│
├── Configuration Files
│   ├── package.json                  # NPM dependencies & scripts
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── next.config.ts                # Next.js configuration
│   ├── tailwind.config.ts            # Tailwind CSS configuration
│   ├── components.json               # Shadcn/ui configuration
│   ├── postcss.config.mjs            # PostCSS configuration
│   └── .eslintrc.json                # ESLint configuration
│
├── Documentation
│   ├── README.md                     # Project overview
│   ├── CLAUDE.md                     # Claude Code instructions
│   ├── ARCHITECTURE.md               # This file
│   ├── AGENTS.md                     # Agent documentation
│   └── NVM_SETUP.md                  # Node version management
│
└── Build Outputs
    ├── .next/                        # Next.js build cache
    ├── out/                          # Static export output
    └── .git/                         # Git repository
```

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 📊 Data Flow Architecture

> **Purpose:** Understand how data moves from NASA ADS API through scripts to the deployed site
>
> **When to use this section:** Debugging data pipelines, understanding automation flow, adding new data sources
>
> **Related Sections:** [GitHub Actions Workflows](#github-actions-workflows) • [Python Scripts](#python-scripts) • [Data Management](#data-management)

---

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     NASA ADS API                            │
│          (Publications, Citations, Metrics)                 │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Publications │  │   Metrics    │  │  Citations   │
│   Fetcher    │  │   Fetcher    │  │   Fetcher    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ ads_publica- │  │ ads_metrics  │  │ citations_   │
│ tions.json   │  │ .json        │  │ by_year.json │
└──────┬───────┘  └──────────────┘  └──────┬───────┘
       │                                    │
       │                                    ▼
       │                          ┌──────────────────┐
       │                          │ Citation Plot    │
       │                          │ Generator        │
       │                          └──────────────────┘
       │                                    │
       │                                    ▼
       │                          ┌──────────────────┐
       │                          │ citations_by_    │
       │                          │ year.svg         │
       │                          └──────────────────┘
       │
       └────────────────┐
                        │
        ┌───────────────┴────────────────┐
        │                                │
        ▼                                ▼
┌──────────────┐              ┌──────────────────┐
│ Figure       │              │ Page-Figure      │
│ Metadata     │              │ Mappings         │
│ (Manual)     │              │ (Manual)         │
└──────┬───────┘              └──────┬───────────┘
       │                             │
       └──────────┬──────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  generate_figure_   │
        │  data.py            │
        │  (Combines sources) │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ research-figures-   │
        │ with-captions.json  │
        │ (Combined output)   │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  Next.js Static     │
        │  Site Generation    │
        │  (Dynamic Routes)   │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  GitHub Pages       │
        │  Deployment         │
        └─────────────────────┘
```

### Data Categories

**Automated Data** (generated by GitHub Actions):
- `ads_publications.json` - Publications from NASA ADS
- `ads_metrics.json` - Citation metrics and h-index
- `citations_by_year.json` - Annual citation counts
- `research-figures-with-captions.json` - Combined figure data
- `citations_by_year.svg` - Citation trend visualization

**Manual Data** (curated by maintainer):
- `research-projects.json` - Featured research project definitions
- `figure-metadata.json` - Figure database with captions, alt text, bibcodes
- `page-figure-mappings.json` - Simple mapping of research pages to figures
- `research-paragraphs.json` - Detailed descriptions for research subpages
- `education.json` & `positions.json` - Academic and professional history
- `skills.json` - Technical skills data

[↑ Back to Table of Contents](#table-of-contents)

---
---

## ⚙️ GitHub Actions Workflows

> **Purpose:** Complete reference for all automated CI/CD workflows
>
> **When to use this section:** Debugging automation failures, understanding update schedules, modifying workflows
>
> **Related Sections:** [Data Flow Architecture](#data-flow-architecture) • [Python Scripts](#python-scripts) • [Deployment Process](#deployment-process)
>
> **Quick Links:**
> - [Update Publications](#1-update-ads-publications)
> - [Update Metrics](#2-update-ads-metrics)
> - [Update Citations](#3-update-annual-citations)
> - [Convert PDFs](#4-convert-pdfs-to-svg)
> - [Generate Figure Data](#5-generate-figure-data)

---

### 1. Update ADS Publications

**File:** `.github/workflows/update-ads-publications.yml`

**Trigger:** Weekly on Mondays at 04:00 UTC (or manual dispatch)

**Purpose:** Fetch latest publications from NASA ADS using ORCID

**Process:**
1. Checkout repository
2. Set up Python 3.10
3. Install dependencies from `scripts/requirements.txt`
4. Run `fetch_ads_publications_to_data_dir.py`
5. Commit changes to main if any exist

**Output:** `/public/data/ads_publications.json`

**Dependencies:**
- `ADS_DEV_KEY` (GitHub secret)
- `ADS_ORCID` (GitHub secret)

**Data Format:**
```json
[
  {
    "bibcode": "2025ApJ...980...70R",
    "title": "Publication title",
    "authors": ["Lastname, F.", "..."],
    "month": "Month name or empty",
    "year": "YYYY-MM-DD",
    "journal": "Publication venue",
    "publication_type": "article|dataset|inproceedings|...",
    "citations": 5,
    "url": "https://dx.doi.org/... or https://ui.adsabs.harvard.edu/abs/..."
  }
]
```

---

### 2. Update ADS Metrics

**File:** `.github/workflows/update-ads-metrics.yml`

**Trigger:** Weekly on Mondays at 03:00 UTC (or manual dispatch)

**Purpose:** Fetch citation metrics (h-index, total citations, etc.)

**Process:**
1. Run `fetch_ads_metrics_to_data_dir.py` with ORCID argument
2. Make API request to NASA ADS metrics endpoint
3. Commit updated metrics

**Output:** `/public/data/ads_metrics.json`

**Used By:** Publications page for displaying h-index and citation statistics

**Data Format:**
```json
{
  "indicators": { "h": 8 },
  "basic stats": { "number of papers": 15 },
  "citation stats": { "total number of citations": 42 },
  "basic stats refereed": { "number of papers": 12 },
  "citation stats refereed": { "total number of citations": 38 }
}
```

---

### 3. Update Annual Citations

**File:** `.github/workflows/update_annual_citations.yml`

**Trigger:** Weekly on Mondays at 00:00 UTC (or manual dispatch)

**Purpose:** Generate yearly citation data and visualization

**Process:**
1. Run `fetch_ads_citations_by_year.py`
2. 7-day caching to avoid redundant API calls
3. Fetch citation histogram per year from ADS
4. Generate SVG plot using matplotlib
5. Commit both JSON data and SVG plot

**Output:**
- `/public/data/citations_by_year.json`
- `/public/plots/citations_by_year.svg`

**Features:**
- Rate limiting with Retry-After headers
- Timezone handling (Eastern Time)
- Separates refereed vs. non-refereed citations

**Data Format:**
```json
{
  "2024": {
    "refereed to refereed": 5,
    "refereed to nonrefereed": 1,
    "nonrefereed to refereed": 0,
    "nonrefereed to nonrefereed": 2
  }
}
```

---

### 4. Convert PDFs to SVG

**File:** `.github/workflows/convert-pdfs.yml`

**Trigger:** On push to `public/paper-figures/pdfs/` directory

**Purpose:** Auto-convert PDF figures to web-friendly SVG format

**Process:**
1. Install `poppler-utils` for PDF conversion
2. Use `pdftocairo` to convert each PDF to SVG
3. Save to `/public/paper-figures/svg/`
4. Auto-commit SVG files

**Benefit:** Simplifies figure management - just upload PDFs and they're automatically converted

---

### 5. Generate Figure Data

**File:** `.github/workflows/generate-figure-data.yml`

**Trigger:** On push to paths:
- `public/data/ads_publications.json`
- `public/paper-figures/figure-metadata.json`
- `public/data/page-figure-mappings.json`
- `public/data/research-projects.json`

**Purpose:** Combine figure metadata with publication data and citations

**Process:**
1. Run `generate_figure_data.py`
2. Merge figure info, publication metadata, and citation data
3. Fetch figure licenses from external sources
4. Generate rich captions with citations
5. Commit output

**Output:** `/public/data/research-figures-with-captions.json`

**Data Format:**
```json
[
  {
    "slug": "proton-beams",
    "title": "Proton Beams",
    "figure": {
      "src": "/paper-figures/svg/filename.svg",
      "alt": "Alternative text",
      "caption": "From Alterman et al. (2024), The Astrophysical Journal [link]"
    }
  }
]
```

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 🐍 Python Scripts

> **Purpose:** Detailed reference for all automation scripts in `/scripts/` directory
>
> **When to use this section:** Adding new data fetching automation, understanding how figures are processed, debugging data pipeline issues, creating new research pages programmatically
>
> **Related Sections:** [GitHub Actions Workflows](#github-actions-workflows) • [Data Management](#data-management) • [Common Tasks](#common-tasks)
>
> **Quick Links:**
> - [Shared Utilities](#shared-utilities-utilspy)
> - [Publications Fetcher](#1-fetch_ads_publications_to_data_dirpy)
> - [Metrics Fetcher](#2-fetch_ads_metrics_to_data_dirpy)
> - [Citations Fetcher](#3-fetch_ads_citations_by_yearpy)
> - [Figure Data Generator](#4-generate_figure_datapy)
> - [Research Page Creator](#5-create_research_pagepy)

---

All scripts are located in the `/scripts/` directory and use shared utilities from `utils.py`.

### Shared Utilities: `utils.py`

**Purpose:** Consistent path management across all scripts

**Functions:**
```python
get_repo_root() -> Path
    # Returns repository root directory
    # Uses Path(__file__).parent.parent

get_public_data_dir() -> Path
    # Returns /public/data/ directory

get_public_plots_dir() -> Path
    # Returns /public/plots/ directory

get_relative_path(absolute_path: Path) -> str
    # Converts absolute paths to relative for display
```

**Benefit:** Scripts work correctly regardless of invocation directory

---

### 1. `fetch_ads_publications_to_data_dir.py`

**Purpose:** Fetch publications from NASA ADS using ORCID

**Input:**
- `ADS_ORCID` environment variable
- `ADS_DEV_KEY` environment variable

**Process:**
1. Query NASA ADS using ORCID
2. Fetch 2000 publications with fields: bibcode, title, author, pubdate, journal, doctype, citations, DOI
3. Format author names: "Lastname, F. M."
4. Highlight "Alterman" author with `<strong>` tags
5. Generate URLs (DOI preferred, fallback to ADS link)
6. Output structured JSON

**Output:** `/public/data/ads_publications.json`

**API Endpoint:** `https://api.adsabs.harvard.edu/v1/search/query`

---

### 2. `fetch_ads_metrics_to_data_dir.py`

**Purpose:** Fetch citation metrics from NASA ADS

**Input:**
- ORCID (command-line argument)
- `ADS_DEV_KEY` environment variable

**Process:**
1. Get all bibcodes for the ORCID
2. Make POST request to NASA ADS metrics API
3. Receive comprehensive metrics including h-index
4. Save full metrics JSON

**Output:** `/public/data/ads_metrics.json`

**API Endpoint:** `https://api.adsabs.harvard.edu/v1/metrics`

---

### 3. `fetch_ads_citations_by_year.py`

**Purpose:** Fetch annual citation data and generate visualization

**Features:**
- 7-day caching to prevent redundant API calls
- Rate limiting with Retry-After header handling
- Matplotlib visualization generation
- Timezone handling (Eastern Time)

**Process:**
1. Get all bibcodes for ORCID
2. Query citation histogram by year from ADS
3. Separate refereed vs. non-refereed citations
4. Generate matplotlib bar chart
5. Save both JSON data and SVG plot

**Output:**
- `/public/data/citations_by_year.json`
- `/public/plots/citations_by_year.svg`

**API Endpoint:** `https://api.adsabs.harvard.edu/v1/metrics`

---

### 4. `generate_figure_data.py`

**Purpose:** Combine figure metadata with publication data to create rich captions

**Inputs:**
1. `/public/data/research-projects.json` - Featured research topics
2. `/public/paper-figures/figure-metadata.json` - Figure database
3. `/public/data/page-figure-mappings.json` - Maps pages to figures
4. `/public/data/ads_publications.json` - Publication details

**Process:**
1. For each research project (slug):
   - Look up assigned figure from page mappings
   - Get figure metadata (src, alt, caption, bibcode)
   - Find publication info via bibcode
   - Generate caption with citation formatting
   - Fetch figure licenses
2. Handle placeholders (figures without real publication links)
3. Generate rich captions like: "From Alterman et al. (2024), The Astrophysical Journal [linked]"

**Output:** `/public/data/research-figures-with-captions.json`

**Caption Format:**
```
From {first_author} et al. ({year}), {journal}
```

**Placeholder Handling:**
- If figure is `placeholder.png` or similar, returns simple structure
- No publication lookup for placeholders

---

### 5. `create_research_page.py`

**Purpose:** Interactive CLI tool for creating new research pages

**Features:**
- Displays existing pages and available figures
- Smart slug generation from titles with uniqueness checking
- Input validation
- Preview mode (shows changes before applying)
- Dry-run support: `python scripts/create_research_page.py --dry-run`
- Automatic backup of modified files
- Updates all three JSON files atomically

**Workflow:**
1. Display existing research pages
2. Prompt for title (validates non-empty)
3. Generate unique slug from title
4. Prompt for description
5. Display available figures (not already assigned)
6. Prompt for figure selection
7. Prompt for detailed content (paragraph)
8. Preview all changes
9. Ask for confirmation
10. Update three JSON files:
    - `research-projects.json`
    - `page-figure-mappings.json`
    - `research-paragraphs.json`

**Usage:**
```bash
# Interactive mode
python scripts/create_research_page.py

# Preview mode (no changes made)
python scripts/create_research_page.py --dry-run
```

**Testing:**
```bash
python scripts/test_create_research_page.py
```

---

### 6. `fetch_figure_licenses.py`

**Purpose:** Fetch Creative Commons license information for figures

**Used By:** `generate_figure_data.py`

**Process:** Looks up DOI to find licensing info

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 🔀 Dynamic Route System

> **Purpose:** Understand how single React components generate multiple static pages from JSON data
>
> **When to use this section:** Adding new research/ben/publication pages, understanding page generation, modifying page templates
>
> **Related Sections:** [Data Management](#data-management) • [Component Architecture](#component-architecture) • [Common Tasks](#common-tasks)

---

### Overview

The site uses **Next.js App Router's dynamic routing** with static generation to avoid duplicating React/TypeScript code for each research page.

### How It Works

**Single Template:** `/src/app/research/[slug]/page.tsx`

```typescript
export async function generateStaticParams() {
  const projects = loadJSONData<ResearchProject[]>('research-projects.json');
  return projects.map(project => ({ slug: project.slug }));
}

export default function ResearchSubPage({ params }: { params: { slug: string } }) {
  // Load data dynamically based on slug
  const projects = loadJSONData<ResearchProject[]>('research-projects.json');
  const paragraphs = loadJSONData<Record<string, string>>('research-paragraphs.json');
  const figuresData = loadJSONData<ResearchFigureData[]>('research-figures-with-captions.json');

  // Find data for this specific slug
  const project = projects.find(p => p.slug === params.slug);
  const paragraph = paragraphs[params.slug];
  const figureData = figuresData.find(f => f.slug === params.slug);

  // Render page
  return (
    <div>
      <h1>{project.title}</h1>
      <p>{paragraph}</p>
      <ResearchFigure {...figureData.figure} />
    </div>
  );
}
```

### Build Process

**At Build Time:**
1. `generateStaticParams()` reads `research-projects.json`
2. Extracts all slugs: `["proton-beams", "helium-abundance", "coulomb-collisions", ...]`
3. Next.js generates static HTML for each slug:
   - `/out/research/proton-beams.html`
   - `/out/research/helium-abundance.html`
   - `/out/research/coulomb-collisions.html`
   - etc.

**At Runtime (Static Site):**
- Each HTML file contains pre-rendered content
- No server-side processing needed
- Fast page loads

### Benefits

1. **DRY Principle:** One template instead of 8+ duplicate files
2. **Data-Driven:** Adding pages requires only JSON updates
3. **Consistent Styling:** All pages guaranteed to have identical structure
4. **Easier Maintenance:** Layout changes only need updating in one place
5. **Static Export Compatible:** Generates individual HTML files for GitHub Pages
6. **Type Safety:** TypeScript ensures data structure consistency

### Research Card Randomization

**Behavior:** Research project cards on `/research` are shuffled at build time

**Implementation:** `/src/app/research/page.tsx` (line 30)
```typescript
const shuffledProjects = [...researchProjects].sort(() => Math.random() - 0.5);
```

**Characteristics:**
- Shuffle occurs once during `npm run build`
- All visitors see identical order until next deployment
- Order refreshes automatically via:
  - Weekly GitHub Actions deployments (every Monday)
  - Manual deployments/rebuilds
  - Any push to main branch that triggers deployment

**Rationale:** Prevents implied priority hierarchy among research topics

### Adding a New Research Page

**Option 1: Interactive Script (Recommended)**
```bash
python scripts/create_research_page.py
```

**Option 2: Manual JSON Updates**

1. **Add to `research-projects.json`:**
```json
{
  "title": "Solar Energetic Particles",
  "slug": "solar-energetic-particles",
  "description": "Studying particle acceleration in solar events",
  "image": "https://placehold.co/600x400.png",
  "imageHint": "solar particles"
}
```

2. **Add to `page-figure-mappings.json`:**
```json
{
  "solar-energetic-particles": "sep-figure.svg"
}
```

3. **Add to `research-paragraphs.json`:**
```json
{
  "solar-energetic-particles": "Detailed research description discussing particle acceleration mechanisms..."
}
```

4. **Push to main:**
```bash
git add public/data/*.json
git commit -m "Add solar energetic particles research page"
git push
```

5. **Result:** Page automatically exists at `/research/solar-energetic-particles`

**No React/TypeScript files need to be created!**

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 🧩 Component Architecture

> **Purpose:** Complete reference for React components, page structure, and utility functions
>
> **When to use this section:** Building new UI components, understanding page layouts, adding utilities
>
> **Related Sections:** [Dynamic Route System](#dynamic-route-system) • [Technology Stack](#technology-stack) • [Configuration Files](#configuration-files)

---

### Page Structure (App Router)

```
/src/app/
├── page.tsx                    # Home page (/)
│   └── Components: Header, About, Contact
│
├── layout.tsx                  # Root layout
│   ├── Metadata (SEO, OpenGraph, Twitter)
│   ├── JSON-LD structured data for Person schema
│   ├── Global styles
│   └── Font loading (Inter from Google Fonts)
│
├── research/
│   ├── page.tsx               # Research overview (/research)
│   │   └── Featured research grid (from research-projects.json)
│   │
│   ├── [slug]/page.tsx         # Dynamic research subpages
│   │   ├── generateStaticParams() reads from research-projects.json
│   │   ├── Loads figure data, paragraphs, publication info
│   │   ├── ResearchFigure component with caption
│   │   └── Math rendering via LaTeX
│   │
│   └── layout.tsx
│
├── publications/
│   ├── page.tsx               # Publications overview page (/publications)
│   │   ├── Displays ads_metrics.json (h-index, citations)
│   │   ├── Loads publications-categories.json for card display
│   │   ├── Card grid layout for publication categories
│   │   ├── Conditional rendering (only shows categories with publications)
│   │   ├── Links to /publications/[category] subpages
│   │   └── Count badges on each card
│   │
│   ├── [category]/
│   │   └── page.tsx           # Dynamic publication category pages
│   │       ├── generateStaticParams() from publications-categories.json
│   │       ├── Filters publications by publicationType
│   │       ├── Displays full publication table for category
│   │       ├── Conditional Citations column (showCitations flag)
│   │       └── Breadcrumb navigation
│   │
│   ├── loading.tsx            # Loading state component
│   └── layout.tsx
│
├── experience/
│   ├── page.tsx               # Education & positions (/experience)
│   │   └── Timeline view of education.json and positions.json
│   │
│   └── layout.tsx
│
├── ben/
│   ├── page.tsx               # Ben overview page (/ben) - card grid
│   │   ├── Loads ben-page.json (heading, tagline, sections array)
│   │   ├── Filters published sections (environment-aware)
│   │   ├── Card grid layout (responsive 1/2/3 columns)
│   │   ├── Icon mapping with Lucide React (Telescope, Compass, HeartHandshake)
│   │   ├── Displays title, icon, excerpt on each card
│   │   └── Links to /ben/[slug] subpages
│   │
│   ├── [slug]/
│   │   └── page.tsx           # Dynamic Ben subpages
│   │       ├── generateStaticParams() from ben-page.json
│   │       ├── Finds section by slug
│   │       ├── Renders title, icon, full paragraphs
│   │       ├── Environment-aware publishing (dev shows all, production filters)
│   │       └── Breadcrumb navigation
│   │
│   └── layout.tsx
│
└── globals.css                # Global Tailwind styles
```

### Key Components

#### UI Layer (`src/components/ui/`)

Shadcn/ui pre-built components (52 files) based on Radix UI primitives with Tailwind styling:

- **Layout:** Card, Separator, Tabs, Accordion
- **Forms:** Button, Input, Select, Checkbox, Radio Group, Form, Label
- **Data Display:** Table, Badge, Avatar, Tooltip, Popover
- **Feedback:** Toast, Dialog, Alert Dialog, Sheet, Drawer
- **Navigation:** Navigation Menu, Dropdown Menu, Context Menu, Menubar
- **Overlays:** Dialog, Sheet, Drawer, Popover, Hover Card
- **Charts:** Chart components with Recharts integration

#### Custom Components (`src/components/`)

**`header.tsx`** - Navigation Header
- Sticky, responsive (mobile/desktop)
- Main navigation links: Research, Publications, Experience, Contact
- Social media buttons:
  - GitHub
  - ORCID
  - NASA ADS
  - Google Scholar
  - arXiv
  - LinkedIn
- Mobile navigation menu

**`research-figure.tsx`** - Figure Display Component
```typescript
interface ResearchFigureProps {
  src: string;
  alt: string;
  caption: string;
}
```
- Image with aspect ratio container
- Caption with HTML rendering support (for links)
- LaTeX math expression rendering
- Responsive sizing

**`featured-research.tsx`** - Research Grid
- Card-based layout showing research projects
- Displays project title, description, image
- Responsive grid (1 column mobile → 2 columns tablet → 3 columns desktop)
- Hover effects and transitions

**Card Order:**
- Research project cards are shuffled at build time using `Array.sort(() => Math.random() - 0.5)`
- All visitors see the same random order until the next build/deployment
- Order changes automatically with weekly automated builds (Monday deployments)
- Manual rebuilds (`npm run build`) will generate a new random order

**`research.tsx`** - Featured Research Projects Section
- Section header
- Grid of featured research cards
- Currently uses data from research-projects.json

**`experience.tsx`** - Professional Timeline
- Education and position cards
- Institution, dates, location info
- Chronological ordering (most recent first)
- Degree/position title display

**`about.tsx`** - About Section
- Professional bio and introduction
- Research interests
- Current affiliation

**`contact.tsx`** - Contact Information
- Footer section with contact details
- Email address
- Links to professional profiles

#### Icon Components (`src/components/icons/`)

Custom SVG icons for external services:
- **ORCID Icon** - Research identifier
- **Google Scholar Icon** - Academic profile
- **NASA ADS Icon** - Astrophysics database
- **arXiv Icon** - Preprint repository
- **LinkedIn Icon** - Professional network
- **GitHub Icon** - Code repository
- **Firebase Icon** - Backend services

### Utility Functions

#### `lib/data-loader.ts`

```typescript
export function loadJSONData<T>(fileName: string): T {
  const filePath = path.join(process.cwd(), 'public', 'data', fileName);
  const fileContents = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(fileContents) as T;
}
```

**Purpose:** Load JSON data from `/public/data/` at build time

**Usage:**
```typescript
const projects = loadJSONData<ResearchProject[]>('research-projects.json');
const metrics = loadJSONData<ADSMetrics>('ads_metrics.json');
```

**Note:** Works with synchronous file reading (server-side only)

#### `lib/publication-utils.ts`

```typescript
sortPublicationsByDate(publications: Publication[]): Publication[]
filterPublicationsByType(publications: Publication[], type: string): Publication[]
getPublicationsByType(publications: Publication[], type: string): Publication[]
sortPublicationsByCitations(publications: Publication[]): Publication[]
```

**Purpose:** Publication filtering, sorting, and display utilities

**Usage Example:**
```typescript
const articles = getPublicationsByType(publications, 'article');
const sortedByDate = sortPublicationsByDate(articles);
```

#### `lib/render-math.ts`

```typescript
export function renderMath(text: string): string {
  // Converts LaTeX expressions to HTML using KaTeX
  // Processes $...$ (inline) and $$...$$ (display) math
}
```

**Purpose:** Render LaTeX mathematical expressions in research content

**Example Input:**
```
The energy is given by $E = mc^2$, which shows:
$$E = \gamma m c^2$$
```

**Example Output:**
```html
The energy is given by <span class="katex">...</span>, which shows:
<div class="katex-display">...</div>
```

#### `lib/utils.ts`

```typescript
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

**Purpose:** Merge Tailwind CSS class names with conflict resolution

#### `lib/research-utils.ts`

```typescript
export function filterPublishedProjects<T extends { published?: boolean }>(
    projects: T[]
): T[]
```

**Purpose:** Environment-aware filtering for research projects

**Behavior:**
- **Development:** Returns all projects (including unpublished) for testing
- **Production:** Returns only projects where `published !== false`

**Usage Example:**
```typescript
const projects = loadJSONData<ResearchProject[]>('research-projects.json');
const publishedProjects = filterPublishedProjects(projects);
// Development: all 9 projects | Production: only published projects
```

**Used By:**
- `/src/app/research/page.tsx` - Filter cards on research overview
- `/src/app/research/[slug]/page.tsx` - Filter static params generation

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 💾 Data Management

> **Purpose:** Complete reference for all JSON data files and their schemas
>
> **When to use this section:** Understanding data file formats, adding new data, debugging data issues, creating content
>
> **Related Sections:** [Data Flow Architecture](#data-flow-architecture) • [Python Scripts](#python-scripts) • [Common Tasks](#common-tasks)

---

### In This Section

**Automated Data Files (Generated by GitHub Actions):**
- [ads_publications.json](#ads_publicationsjson-3600-lines) - Publications from NASA ADS
- [ads_metrics.json](#ads_metricsjson-679-lines) - Citation metrics
- [citations_by_year.json](#citations_by_yearjson-43-lines) - Annual citations
- [research-figures-with-captions.json](#research-figures-with-captionsjson-82-lines) - Combined figure data

**Manual Data Files (Curated):**
- [research-projects.json](#research-projectsjson-65-lines) - Featured research topics
- [page-figure-mappings.json](#page-figure-mappingsjson-11-lines) - Figure assignments
- [research-paragraphs.json](#research-paragraphsjson-12-lines) - Detailed descriptions
- [figure-metadata.json](#figure-metadatajson) - Figure database
- [ben-page.json](#ben-pagejson-40-lines) - Ben page structure
- [publications-categories.json](#publications-categoriesjson-50-lines) - Publication categories
- [education.json](#educationjson-16-lines) - Academic credentials
- [positions.json](#positionsjson-21-lines) - Employment history
- [skills.json](#skillsjson-18-lines) - Technical skills

[↑ Back to Table of Contents](#table-of-contents)

---

### Automated Data Files

#### `ads_publications.json` (~3,600 lines)

**Updated:** Weekly on Mondays at 04:00 UTC

**Source:** NASA ADS API via ORCID

**Structure:**
```json
[
  {
    "bibcode": "2025ApJ...980...70R",
    "title": "Paper title here",
    "authors": [
      "Lastname, F. M.",
      "<strong>Alterman, B. L.</strong>",
      "Another, A. B."
    ],
    "month": "January",
    "year": "2025-01-15",
    "journal": "The Astrophysical Journal",
    "publication_type": "article",
    "citations": 5,
    "url": "https://dx.doi.org/10.3847/..."
  }
]
```

**Publication Types:**
- `article` - Journal articles
- `eprint` - Preprints
- `inproceedings` - Conference papers
- `dataset` - Data publications
- `software` - Software releases
- `poster` - Conference posters
- `abstract` - Conference abstracts

**Used By:**
- Publications page (/publications)
- generate_figure_data.py (for caption generation)

---

#### `ads_metrics.json` (~679 lines)

**Updated:** Weekly on Mondays at 03:00 UTC

**Source:** NASA ADS Metrics API

**Structure:**
```json
{
  "indicators": {
    "h": 8,
    "g": 12,
    "i10": 7,
    "tori": 5.2,
    "riq": 42,
    "m": 1.6
  },
  "basic stats": {
    "number of papers": 15,
    "normalized paper count": 12.5
  },
  "citation stats": {
    "total number of citations": 42,
    "number of citing papers": 35,
    "average citations": 2.8,
    "median citations": 2.0,
    "normalized citations": 38.5
  },
  "basic stats refereed": {
    "number of papers": 12,
    "normalized paper count": 10.8
  },
  "citation stats refereed": {
    "total number of citations": 38,
    "number of citing papers": 32,
    "average citations": 3.2
  }
}
```

**Key Metrics:**
- **h-index:** Number h where h papers have at least h citations
- **g-index:** Largest number g where top g papers have at least g² citations
- **i10-index:** Number of papers with at least 10 citations

**Used By:** Publications page (displayed as summary cards)

---

#### `citations_by_year.json` (~43 lines)

**Updated:** Weekly on Mondays at 00:00 UTC

**Source:** NASA ADS Metrics API

**Structure:**
```json
{
  "2019": {
    "refereed to refereed": 2,
    "refereed to nonrefereed": 1,
    "nonrefereed to refereed": 0,
    "nonrefereed to nonrefereed": 3
  },
  "2020": {
    "refereed to refereed": 5,
    "refereed to nonrefereed": 2,
    "nonrefereed to refereed": 1,
    "nonrefereed to nonrefereed": 4
  }
}
```

**Citation Types:**
- **refereed to refereed:** Peer-reviewed paper citing peer-reviewed paper
- **refereed to nonrefereed:** Peer-reviewed citing non-peer-reviewed
- **nonrefereed to refereed:** Non-peer-reviewed citing peer-reviewed
- **nonrefereed to nonrefereed:** Non-peer-reviewed citing non-peer-reviewed

**Used By:**
- SVG plot generation (citations_by_year.svg)
- Publications page (future implementation)

---

#### `research-figures-with-captions.json` (~82 lines)

**Updated:** When publications, figure-metadata, or mappings change

**Source:** Generated by `generate_figure_data.py`

**Structure:**
```json
[
  {
    "slug": "proton-beams",
    "title": "Proton Beams",
    "figure": {
      "src": "/paper-figures/svg/P9-Fig9.svg",
      "alt": "Proton velocity distributions showing beam features",
      "caption": "From <a href=\"https://dx.doi.org/...\">Alterman et al. (2024), The Astrophysical Journal</a>"
    }
  }
]
```

**Caption Format:**
- Includes author list (first author et al.)
- Publication year
- Journal name
- Clickable link to DOI or ADS

**Used By:** Research detail pages ([slug] dynamic route)

---

### Manual Data Files

#### `research-projects.json` (~65 lines)

**Purpose:** Define featured research topics

**Structure:**
```json
[
  {
    "title": "Proton Beams",
    "slug": "proton-beams",
    "description": "Investigating how proton beams form and evolve in the solar wind",
    "image": "https://placehold.co/600x400.png",
    "imageHint": "solar wind particles",
    "published": false
  }
]
```

**Fields:**
- **title:** Display title (used in navigation, headers)
- **slug:** URL-safe identifier (used in /research/[slug])
- **description:** Brief summary (shown on research overview page)
- **image:** Placeholder image URL (for overview grid)
- **imageHint:** Alt text hint for image
- **published:** (optional, boolean) Whether page is visible in production. Defaults to `true`. Set to `false` to hide page in production builds while keeping it visible in development

**Used By:**
- Research overview page (/research) - displayed in random order (shuffled at build time)
- Research detail pages (generateStaticParams)
- generate_figure_data.py

---

#### `page-figure-mappings.json` (~11 lines)

**Purpose:** Map research page slugs to figure filenames

**Structure:**
```json
{
  "proton-beams": "placeholder.png",
  "helium-abundance": "Ahe-bilinear.svg",
  "coulomb-collisions": "P9-Fig9.svg",
  "magnetic-switchbacks": "placeholder.png",
  "solar-wind-thermodynamics": "placeholder.png",
  "turbulence-heating": "placeholder.png"
}
```

**Pattern:** `slug` → `figure_filename.svg`

**Notes:**
- Filenames refer to files in `/public/paper-figures/svg/`
- `placeholder.png` used for pages without specific figures
- One-to-one mapping (each page gets exactly one figure)

**Used By:** generate_figure_data.py

---

#### `research-paragraphs.json` (~12 lines)

**Purpose:** Detailed descriptions for each research subpage

**Structure:**
```json
{
  "proton-beams": "Detailed introductory paragraph about proton beams. Can include multiple sentences describing the research topic, methods, findings, and implications.",
  "helium-abundance": "Another detailed paragraph for this topic..."
}
```

**Content Guidelines:**
- 3-5 sentences recommended
- Focus on research significance and approach
- Can include LaTeX math expressions: `$E = mc^2$`
- Avoid overly technical jargon

**Used By:** Research detail pages (shown above figure)

---

#### `figure-metadata.json`

**Purpose:** Figure database with captions, alt text, and bibcodes

**Structure:**
```json
{
  "P9-Fig9.svg": {
    "src": "/paper-figures/svg/P9-Fig9.svg",
    "alt": "Proton velocity distributions from Parker Solar Probe",
    "caption": "Proton velocity distribution functions showing beam features",
    "bibcode": "2024ApJ...960...70A",
    "license": "CC-BY-4.0"
  }
}
```

**Fields:**
- **src:** Path to figure file (relative to public/)
- **alt:** Accessibility text describing visual content
- **caption:** Figure caption (without citation)
- **bibcode:** NASA ADS bibcode for source publication
- **license:** Creative Commons license (optional)

**Used By:** generate_figure_data.py (to look up figure details)

---

#### `education.json` (~16 lines)

**Purpose:** Academic credentials

**Structure:**
```json
[
  {
    "Institution": "University of Michigan",
    "Department": "Applied Physics",
    "Location": "Ann Arbor, MI",
    "Dates": "2012 – 2019",
    "Degree": "Doctor of Philosophy"
  },
  {
    "Institution": "University of Michigan",
    "Department": "Applied Physics",
    "Location": "Ann Arbor, MI",
    "Dates": "2012 – 2014",
    "Degree": "Master of Science"
  }
]
```

**Used By:** Experience page (/experience)

---

#### `positions.json` (~21 lines)

**Purpose:** Professional employment history

**Structure:**
```json
[
  {
    "Company": "NASA Goddard Space Flight Center",
    "Position Title": "Research Astrophysicist",
    "Dates": "2024 – Present",
    "Location": "Greenbelt, MD"
  },
  {
    "Company": "NASA Goddard Space Flight Center",
    "Position Title": "Postdoctoral Research Associate",
    "Dates": "2019 – 2024",
    "Location": "Greenbelt, MD"
  }
]
```

**Used By:** Experience page (/experience)

---

#### `skills.json` (~18 lines)

**Purpose:** Technical skills and competencies

**Structure:**
```json
{
  "Programming Languages": ["Python", "JavaScript", "TypeScript", "IDL"],
  "Frameworks & Tools": ["Next.js", "React", "Tailwind CSS", "Git"],
  "Scientific Computing": ["NumPy", "SciPy", "Matplotlib", "Pandas"],
  "Data Analysis": ["Statistical modeling", "Data visualization", "Machine learning"]
}
```

**Used By:** Future resume/CV page

---

#### `ben-page.json` (~40 lines)

**Purpose:** Defines Ben page overview structure and subpage content

**Type:** Manual (curated)

**Structure:**
```json
{
  "heading": "About Ben",
  "tagline": "How I ask big questions and who I ask them with.",
  "sections": [
    {
      "title": "Research Vision",
      "slug": "research-vision",
      "icon": "Telescope",
      "excerpt": "I study the Sun and solar wind to discover what it means for a Sun to create a habitable zone and to power life on Earth.",
      "paragraphs": ["...", "..."],
      "published": true
    }
  ]
}
```

**Schema:**
- `heading` (string): Page title
- `tagline` (string): Page subtitle
- `sections` (array):
  - `title` (string): Section title
  - `slug` (string): URL-safe identifier for subpage route
  - `icon` (string): Lucide React icon name (e.g., "Telescope", "Compass", "HeartHandshake")
  - `excerpt` (string): Short description (~100 chars) for card preview on overview page
  - `paragraphs` (string[]): Full content paragraphs for subpage
  - `published` (boolean, optional): Whether to show in production (defaults to true)

**Used By:**
- Ben overview page (`/src/app/ben/page.tsx`)
- Ben subpages (`/src/app/ben/[slug]/page.tsx`)

**Environment-Aware Publishing:**
- Development mode: Shows all sections regardless of `published` field
- Production mode: Only generates routes for sections with `published: true`

---

#### `publications-categories.json` (~50 lines)

**Purpose:** Defines publication categories for overview cards and subpage routing

**Type:** Manual (curated)

**Structure:**
```json
{
  "heading": "Publications",
  "tagline": "Peer-reviewed research, datasets, and conference contributions",
  "categories": [
    {
      "title": "Refereed Publications",
      "slug": "refereed",
      "icon": "BookOpen",
      "description": "Peer-reviewed journal articles",
      "publicationType": "article",
      "showCitations": true
    }
  ]
}
```

**Schema:**
- `heading` (string): Page title
- `tagline` (string): Page subtitle
- `categories` (array):
  - `title` (string): Display name for category
  - `slug` (string): URL-safe identifier for subpage route
  - `icon` (string): Lucide React icon name (e.g., "BookOpen", "Database", "FileText")
  - `description` (string): Short description for card
  - `publicationType` (string): ADS publication type to filter (`article`, `dataset`, `inproceedings`, `abstract`, `techreport`, `eprint`, `phdthesis`)
  - `showCitations` (boolean): Whether to display citations column in table

**Used By:**
- Publications overview page (`/src/app/publications/page.tsx`)
- Publications category subpages (`/src/app/publications/[category]/page.tsx`)

**Conditional Rendering:**
- Categories with zero publications are automatically hidden from overview cards
- Only generates static routes for categories that have publications

**Publication Type Mapping:**
- `article` → Refereed Publications
- `dataset` → Datasets
- `inproceedings` → Conference Proceedings
- `abstract` → Conference Presentations
- `techreport` → White Papers
- `eprint` → Pre-Prints
- `phdthesis` → PhD Thesis

[↑ Back to Table of Contents](#table-of-contents)

---
---

## ⚙️ Configuration Files

> **Purpose:** Complete reference for all configuration files and their settings
>
> **When to use this section:** Modifying build settings, updating dependencies, configuring tools
>
> **Related Sections:** [Technology Stack](#technology-stack) • [Development Workflow](#development-workflow) • [Deployment Process](#deployment-process)

---

### `package.json`

**Development Scripts:**
```json
{
  "scripts": {
    "dev": "next dev --turbopack -p 9002",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  }
}
```

**Key Dependencies:**
- `next@15.5.3` - React framework
- `react@18.3.1` - UI library
- `typescript@5` - Type safety
- `tailwindcss@3.4.1` - Styling
- `katex@0.16.22` - Math rendering
- `recharts@2.15.1` - Charts
- `lucide-react@0.475.0` - Icons
- `zod@3.24.2` - Validation
- `react-hook-form` - Forms

**Development:**
- Port: 9002
- Turbopack: Enabled for faster builds
- Hot Module Replacement: Automatic

---

### `next.config.ts`

**Critical Configuration:**
```typescript
const isProd = process.env.NODE_ENV === 'production';
const baseUrl = 'https://blalterman.github.io';

const nextConfig: NextConfig = {
  output: 'export',                    // Static site generation
  assetPrefix: isProd ? baseUrl : '',  // GitHub Pages URL prefix
  basePath: '',

  typescript: {
    ignoreBuildErrors: true,           // Allow build despite TS errors
  },

  eslint: {
    ignoreDuringBuilds: true,          // Allow build despite lint errors
  },

  images: {
    unoptimized: true,                 // Required for static export
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'placehold.co',
      },
    ],
  },

  trailingSlash: false,
};
```

**Why These Settings:**

1. **`output: 'export'`** - Generates static HTML files (required for GitHub Pages)
2. **`assetPrefix`** - Ensures assets load correctly on GitHub Pages subdomain
3. **`ignoreBuildErrors`** - Allows CI/CD to complete even with type issues
4. **`images.unoptimized`** - Next.js Image Optimization requires server, disabled for static export
5. **`trailingSlash: false`** - Cleaner URLs without trailing slashes

---

### `tsconfig.json`

**Key Settings:**
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**Path Aliases:**
- `@/*` maps to `./src/*`
- Enables clean imports: `import { Header } from '@/components/header'`

---

### `tailwind.config.ts`

**Theme Configuration:**
```typescript
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        // ... 20+ semantic color tokens
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

**Features:**
- CSS variables for dynamic theming
- Dark mode support (class-based)
- Custom color system with 10+ semantic tokens
- Chart colors (5 variables)
- Sidebar component colors
- Animation utilities

---

### `components.json` (Shadcn/ui)

**Configuration:**
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

**Usage:**
```bash
# Add new component
npx shadcn@latest add button

# Component installed to: src/components/ui/button.tsx
```

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 👨‍💻 Development Workflow

> **Purpose:** Step-by-step guide for local development, testing, and building
>
> **When to use this section:** Setting up dev environment, running tests, building for production
>
> **Related Sections:** [Configuration Files](#configuration-files) • [Common Tasks](#common-tasks) • [Troubleshooting](#troubleshooting)

---

### Local Development

**1. Install Dependencies:**
```bash
npm install
```

**2. Start Development Server:**
```bash
npm run dev
# Runs on http://localhost:9002 with Turbopack
```

**3. Make Changes:**
- Edit React components in `/src/`
- Update data files in `/public/data/`
- Modify styles in `/src/app/globals.css`
- Hot Module Replacement updates automatically

**4. Type Check:**
```bash
npm run typecheck
```

**5. Lint:**
```bash
npm run lint
```

---

### Testing Python Scripts

**1. Install Python Dependencies:**
```bash
pip install -r scripts/requirements.txt
```

**2. Test Data Fetching (requires ADS credentials):**
```bash
export ADS_DEV_KEY="your-ads-api-key"
export ADS_ORCID="0000-0001-2345-6789"

python scripts/fetch_ads_publications_to_data_dir.py
python scripts/fetch_ads_metrics_to_data_dir.py
python scripts/fetch_ads_citations_by_year.py
```

**3. Test Figure Data Generation:**
```bash
python scripts/generate_figure_data.py
```

**4. Test Research Page Creation (Dry Run):**
```bash
python scripts/create_research_page.py --dry-run
```

**5. Run Tests:**
```bash
python scripts/test_create_research_page.py
```

---

### Adding Content

#### Add a New Research Page

**Option 1: Interactive Script**
```bash
python scripts/create_research_page.py
```

**Option 2: Manual Updates**

1. **Edit `research-projects.json`:**
```json
{
  "title": "New Research Topic",
  "slug": "new-research-topic",
  "description": "Brief description of the research",
  "image": "https://placehold.co/600x400.png",
  "imageHint": "descriptive text"
}
```

**Note:** By default, pages are published. To create a draft page visible only in development, add `"published": false` to the project definition.

2. **Edit `page-figure-mappings.json`:**
```json
{
  "new-research-topic": "figure-name.svg"
}
```

3. **Edit `research-paragraphs.json`:**
```json
{
  "new-research-topic": "Detailed description of the research topic..."
}
```

4. **Commit and push:**
```bash
git add public/data/*.json
git commit -m "Add new research topic"
git push
```

---

#### Add a New Figure

1. **Upload PDF to `/public/paper-figures/pdfs/`:**
```bash
cp my-figure.pdf public/paper-figures/pdfs/
git add public/paper-figures/pdfs/my-figure.pdf
git commit -m "Add new research figure"
git push
```

2. **Automatic Conversion:**
- GitHub Actions workflow triggers on push
- PDF automatically converted to SVG
- SVG saved to `/public/paper-figures/svg/my-figure.svg`

3. **Add Metadata to `figure-metadata.json`:**
```json
{
  "my-figure.svg": {
    "src": "/paper-figures/svg/my-figure.svg",
    "alt": "Description of what the figure shows",
    "caption": "Figure caption text",
    "bibcode": "2024ApJ...960...70A"
  }
}
```

4. **Map Figure to Page in `page-figure-mappings.json`:**
```json
{
  "existing-research-slug": "my-figure.svg"
}
```

---

#### Update Professional Information

**Education:**
Edit `/public/data/education.json`

**Positions:**
Edit `/public/data/positions.json`

**Skills:**
Edit `/public/data/skills.json`

**Commit Changes:**
```bash
git add public/data/education.json public/data/positions.json
git commit -m "Update professional information"
git push
```

---

### Building for Production

**1. Build Static Site:**
```bash
npm run build
```

**2. Output Location:**
```
/out/
├── index.html
├── research/
│   ├── index.html
│   ├── proton-beams.html
│   ├── helium-abundance.html
│   └── ...
├── publications/
│   └── index.html
├── experience/
│   └── index.html
└── _next/
    └── static/...
```

**Note:** Each build generates a new random order for research project cards on `/research`.

**3. Test Locally:**
```bash
npm run start
# Or serve the /out directory with any static server
```

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 🚀 Deployment Process

> **Purpose:** Understand automated and manual deployment to GitHub Pages
>
> **When to use this section:** Deploying changes, debugging deployment issues, understanding CI/CD flow
>
> **Related Sections:** [GitHub Actions Workflows](#github-actions-workflows) • [Configuration Files](#configuration-files) • [Troubleshooting](#troubleshooting)

---

### Automated Deployment

**Trigger:** Push to `main` branch

**Process:**
1. **Data Workflows Run:**
   - Update ADS publications (if Monday 04:00 UTC)
   - Update ADS metrics (if Monday 03:00 UTC)
   - Update annual citations (if Monday 00:00 UTC)
   - Generate figure data (if data files changed)

2. **Build Workflow:**
   - Checkout repository
   - Install Node.js dependencies
   - Run `npm run build`
   - Generate static site to `/out`

3. **Deploy to GitHub Pages:**
   - Push `/out` contents to `gh-pages` branch
   - GitHub Pages serves from `gh-pages` branch
   - Site available at: https://blalterman.github.io

**Result:** Site automatically updates with latest data and content

---

### Manual Deployment

**1. Build Locally:**
```bash
npm run build
```

**2. Deploy to GitHub Pages:**
```bash
# Install gh-pages package if not already installed
npm install -g gh-pages

# Deploy /out directory to gh-pages branch
gh-pages -d out
```

**3. Verify Deployment:**
Visit https://blalterman.github.io

---

### Deployment Flow Diagram

```
┌─────────────────┐
│  Push to main   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  GitHub Actions Triggered   │
└────────┬────────────────────┘
         │
         ├──→ Data Workflows (if scheduled)
         │    ├─ Update publications
         │    ├─ Update metrics
         │    └─ Update citations
         │
         ├──→ Figure Data Generation (if data changed)
         │
         └──→ Build Workflow
              ├─ npm install
              ├─ npm run build
              └─ Generate /out
                       │
                       ▼
              ┌────────────────┐
              │  Deploy to     │
              │  gh-pages      │
              └────────┬───────┘
                       │
                       ▼
              ┌────────────────┐
              │  GitHub Pages  │
              │  Serves Site   │
              └────────────────┘
```

[↑ Back to Table of Contents](#table-of-contents)

---
---

## ✅ Common Tasks

> **Purpose:** Step-by-step guides for frequently performed operations
>
> **When to use this section:** Adding content, updating information, performing routine maintenance
>
> **Related Sections:** [Data Management](#data-management) • [Development Workflow](#development-workflow) • [Troubleshooting](#troubleshooting)

---

### Task: Add a New Publication Manually

**Note:** Publications are automatically fetched from ADS. Manual addition only needed for non-ADS publications.

**1. Edit `ads_publications.json`:**
```json
{
  "bibcode": "custom-bibcode-2024",
  "title": "Publication title",
  "authors": ["Author, A.", "<strong>Alterman, B. L.</strong>"],
  "month": "January",
  "year": "2024-01-15",
  "journal": "Journal Name",
  "publication_type": "article",
  "citations": 0,
  "url": "https://doi.org/..."
}
```

**2. Commit and push:**
```bash
git add public/data/ads_publications.json
git commit -m "Add manual publication entry"
git push
```

---

### Task: Update Site Metadata (SEO)

**Edit `/src/app/layout.tsx`:**

```typescript
export const metadata: Metadata = {
  title: 'B. L. Alterman | Research Astrophysicist',
  description: 'Updated description here',
  keywords: ['astrophysics', 'solar wind', 'heliophysics'],
  openGraph: {
    title: 'B. L. Alterman',
    description: 'Updated description',
    url: 'https://blalterman.github.io',
    siteName: 'B. L. Alterman',
    images: [
      {
        url: 'https://blalterman.github.io/images/og-image.png',
        width: 1200,
        height: 630,
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'B. L. Alterman',
    description: 'Updated description',
    images: ['https://blalterman.github.io/images/og-image.png'],
  },
};
```

---

### Task: Change Theme Colors

**Edit `/src/app/globals.css`:**

```css
@layer base {
  :root {
    --background: 0 0% 100%;        /* White */
    --foreground: 0 0% 3.9%;        /* Near black */
    --primary: 0 0% 9%;             /* Dark gray */
    --primary-foreground: 0 0% 98%; /* Light gray */
    /* ... update other color variables ... */
  }

  .dark {
    --background: 0 0% 3.9%;        /* Dark background */
    --foreground: 0 0% 98%;         /* Light text */
    /* ... dark mode colors ... */
  }
}
```

[↑ Back to Table of Contents](#table-of-contents)

---

### Task: Add New Social Media Link

**1. Create Icon Component (if needed):**
Create `/src/components/icons/NewServiceIcon.tsx`

**2. Edit `/src/components/header.tsx`:**

```typescript
import { NewServiceIcon } from '@/components/icons/NewServiceIcon';

// In the social buttons section:
<Button variant="ghost" size="icon" asChild>
  <a
    href="https://newservice.com/username"
    target="_blank"
    rel="noopener noreferrer"
    aria-label="New Service Profile"
  >
    <NewServiceIcon className="h-5 w-5" />
  </a>
</Button>
```

---

### Task: Debug Build Issues

**1. Check TypeScript Errors:**
```bash
npm run typecheck
```

**2. Check ESLint Errors:**
```bash
npm run lint
```

**3. Check Data Files:**
```bash
# Validate JSON syntax
python -m json.tool public/data/research-projects.json
python -m json.tool public/data/ads_publications.json
```

**4. Check Next.js Build Output:**
```bash
npm run build
# Look for errors in terminal output
```

**5. Common Issues:**
- **Missing data files:** Ensure all JSON files exist in `/public/data/`
- **Invalid JSON:** Check for syntax errors in data files
- **Image paths:** Verify image paths are correct and files exist
- **TypeScript errors:** May be ignored in production build, but should be fixed
- **Module not found:** Run `npm install` to ensure all dependencies are installed

---

### Task: Hide/Show Research Pages (Environment-Aware)

Use the `published` field to control research page visibility in production while keeping them accessible in development.

**Hide a Research Page:**

1. **Edit `/public/data/research-projects.json`:**
```json
{
  "title": "Proton Beams",
  "slug": "proton-beams",
  "published": false  ← Add this field
}
```

2. **Rebuild:**
```bash
npm run build
```

**Result:**
- ✅ Development (`npm run dev`): Page visible, card appears
- ❌ Production (`npm run build`): Page not built, card hidden
- 🔗 Direct URL: Redirects to `/research` in production

**Re-enable a Page:**

Set `"published": true` or remove the field entirely (defaults to true).

**Environment Behavior:**
- **Development:** All pages visible (including unpublished) for testing
- **Production:** Only published pages built and displayed
- **Direct URLs:** Unpublished pages redirect to `/research` in production

**Use Cases:**
- Draft pages without figures or content
- Placeholder topics for future research
- Temporarily hide pages during updates

---

### Task: Add a New Section to the Ben Page

The Ben page (`/ben`) follows the data-driven architecture pattern - all content lives in JSON and is automatically rendered by the React component.

**Current Sections:**
- "Research Vision" (Telescope icon)
- "Team Ethos" (Compass icon)

---

#### Method 1: Add Section with Existing Icons

**If using Telescope or Compass icons (already imported):**

**1. Edit JSON file:**
```bash
# Edit: public/data/ben-page.json
```

**2. Add new section to the `sections` array:**
```json
{
  "heading": "Collaboration & Mentoring",
  "icon": "Telescope",
  "paragraphs": [
    "First paragraph of your content...",
    "Second paragraph of your content...",
    "Additional paragraphs as needed..."
  ]
}
```

**3. Rebuild:**
```bash
npm run build
```

✅ **Done!** The component automatically generates a new card.

---

#### Method 2: Add Section with New Icon

**If you want a new icon from Lucide React:**

**1. Update the React component (`src/app/ben/page.tsx`):**

a. Import the new icon:
```typescript
import { Telescope, Compass, Users } from "lucide-react";
//                               ^^^^^ new icon
```

b. Add to `iconMap`:
```typescript
const iconMap = {
    Telescope: Telescope,
    Compass: Compass,
    Users: Users,  // new icon
};
```

**2. Edit JSON file (`public/data/ben-page.json`):**
```json
{
  "heading": "Collaboration & Mentoring",
  "icon": "Users",
  "paragraphs": [
    "Mentoring is central to how I build teams...",
    "I believe in creating opportunities for growth..."
  ]
}
```

**3. Rebuild:**
```bash
npm run build
```

---

#### Available Lucide Icons

Browse all icons at: **https://lucide.dev/icons/**

**Popular options for additional sections:**
- `Users` - Team/collaboration
- `BookOpen` - Learning/education
- `Lightbulb` - Ideas/innovation
- `Target` - Goals/objectives
- `Award` - Achievements
- `TrendingUp` - Growth/progress
- `GitBranch` - Collaboration/workflow
- `Heart` - Values/culture
- `Sparkles` - Innovation/creativity
- `Rocket` - Vision/ambition

---

#### Data Structure

**File:** `/public/data/ben-page.json`

```json
{
  "heading": "About Ben",
  "tagline": "How I ask big questions and who I ask them with.",
  "sections": [
    {
      "heading": "Section Title",
      "icon": "IconName",
      "paragraphs": [
        "Paragraph 1...",
        "Paragraph 2...",
        "..."
      ]
    }
  ]
}
```

**Key Points:**
- ✅ Sections display in array order
- ✅ Icon names must match keys in `iconMap`
- ✅ Paragraphs array can have unlimited items
- ✅ All styling is automatic (Shadcn/ui Card components)

---

#### Testing

**1. Development server:**
```bash
npm run dev
# Visit http://localhost:9002/ben
```

**2. Type checking:**
```bash
npm run typecheck
```

**3. Validate JSON:**
```bash
python -m json.tool public/data/ben-page.json
```

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 🔧 Troubleshooting

> **Purpose:** Solutions for common problems and debugging strategies
>
> **When to use this section:** Debugging issues, fixing errors, understanding failures
>
> **Related Sections:** [Development Workflow](#development-workflow) • [GitHub Actions Workflows](#github-actions-workflows) • [Common Tasks](#common-tasks)

---

### Issue: Publications Not Updating

**Check:**
1. GitHub Actions workflow runs: https://github.com/blalterman/blalterman.github.io/actions
2. Workflow logs for errors
3. `ADS_DEV_KEY` and `ADS_ORCID` secrets are set in repository settings
4. NASA ADS API is accessible (not rate-limited)

**Manual Update:**
```bash
export ADS_DEV_KEY="your-key"
export ADS_ORCID="your-orcid"
python scripts/fetch_ads_publications_to_data_dir.py
```

---

### Issue: Research Page Not Appearing

**Check:**
1. Entry exists in `research-projects.json` with correct slug
2. Entry exists in `page-figure-mappings.json` with matching slug
3. Entry exists in `research-paragraphs.json` with matching slug
4. Site was rebuilt after JSON changes
5. No typos in slug names (must match exactly)

**Debug:**
```typescript
// Add console.log in [slug]/page.tsx
console.log('Available projects:', projects.map(p => p.slug));
console.log('Requested slug:', params.slug);
```

---

### Issue: Figure Not Displaying

**Check:**
1. Figure file exists in `/public/paper-figures/svg/`
2. Filename matches entry in `page-figure-mappings.json`
3. Figure metadata exists in `figure-metadata.json`
4. Path in figure metadata is correct: `/paper-figures/svg/filename.svg`
5. `generate_figure_data.py` was run after adding figure

**Regenerate Figure Data:**
```bash
python scripts/generate_figure_data.py
git add public/data/research-figures-with-captions.json
git commit -m "Regenerate figure data"
git push
```

---

### Issue: Build Failing

**Common Causes:**

1. **Invalid JSON Syntax:**
```bash
# Validate all JSON files
for file in public/data/*.json; do
  echo "Checking $file"
  python -m json.tool "$file" > /dev/null || echo "ERROR in $file"
done
```

2. **Missing Dependencies:**
```bash
rm -rf node_modules package-lock.json
npm install
```

3. **Next.js Cache Issues:**
```bash
rm -rf .next out
npm run build
```

4. **TypeScript Errors:**
```bash
npm run typecheck
# Fix errors or update next.config.ts to ignore
```

[↑ Back to Table of Contents](#table-of-contents)

---

### Issue: GitHub Actions Failing

**Check:**
1. Workflow file syntax (YAML validation)
2. Secrets are set correctly in repository settings
3. Python dependencies are correct in `requirements.txt`
4. Script paths are correct
5. Permissions are set correctly for workflow

**View Logs:**
1. Go to https://github.com/blalterman/blalterman.github.io/actions
2. Click on failed workflow run
3. Expand failed step to see error details

[↑ Back to Table of Contents](#table-of-contents)

---
---

## ⭐ Best Practices

> **Purpose:** Guidelines for maintaining code quality, consistency, and project health
>
> **When to use this section:** Establishing conventions, reviewing code, maintaining standards
>
> **Related Sections:** [Development Workflow](#development-workflow) • [Component Architecture](#component-architecture)

---

### Code Organization

1. **Use Path Aliases:** Import with `@/` prefix instead of relative paths
   ```typescript
   // Good
   import { Header } from '@/components/header';

   // Avoid
   import { Header } from '../../../components/header';
   ```

2. **Separate Concerns:** Keep data, logic, and UI separate
   - Data: `/public/data/*.json`
   - Logic: `/src/lib/*.ts`
   - UI: `/src/components/*.tsx`

3. **Type Everything:** Use TypeScript interfaces for all data structures
   ```typescript
   // Good
   interface ResearchProject {
     title: string;
     slug: string;
     description: string;
   }

   // Avoid
   const project: any = {...};
   ```

---

### Data Management

1. **Validate JSON:** Always validate JSON files before committing
   ```bash
   python -m json.tool file.json
   ```

2. **Consistent Naming:** Use kebab-case for slugs
   ```
   proton-beams ✓
   ProtonBeams ✗
   proton_beams ✗
   ```

3. **Backup Before Edits:** Scripts create backups automatically, but keep manual backups too

4. **Use Scripts:** Prefer `create_research_page.py` over manual JSON edits

---

### Git Workflow

1. **Descriptive Commits:** Use clear commit messages
   ```bash
   # Good
   git commit -m "Add solar energetic particles research page"

   # Avoid
   git commit -m "Update files"
   ```

2. **Atomic Commits:** One logical change per commit

3. **Test Before Push:** Build locally before pushing
   ```bash
   npm run build
   # Verify no errors
   git push
   ```

---

### Performance

1. **Optimize Images:** Use SVG for figures when possible (done automatically by PDF converter)

2. **Lazy Load:** Next.js handles this automatically for App Router

3. **Static Generation:** Site is fully static - no server-side overhead

4. **Minimize Data Files:** Keep JSON files focused and minimal

---

### AI Development

This project is developed with assistance from AI tools. Follow these guidelines:

1. **Human Review Required:** All AI-generated code must be reviewed and approved by a human developer

2. **Follow Conventions:** Adhere to Next.js patterns, semantic HTML in React components, and maintain type safety

3. **Prompt Analysis:** For moderate-to-complex tasks, AI should proactively analyze prompts for clarity, missing context, and efficiency opportunities

4. **Incremental Changes:** Request small, verifiable changes instead of sweeping rewrites

5. **Document AI Contributions:** Use commit message prefixes (e.g., `AI:`) or co-author tags for AI-assisted work

**📘 See [AGENTS.md](./docs/AGENTS.md) for complete AI development protocols:**
- [Prompt Improvement Protocol](./docs/AGENTS.md#prompt-improvement-protocol) - When and how to analyze prompts
- [Development Conventions](./docs/AGENTS.md#development-conventions) - Code standards and review requirements
- [Prompting Guidelines](./docs/AGENTS.md#prompting-guidelines) - Best practices for effective AI collaboration
- [Agent Use Cases](./docs/AGENTS.md#agent-use-cases) - Common AI-assisted tasks

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 🔮 Future Enhancements

> **Purpose:** Planned features and potential improvements for future development
>
> **When to use this section:** Planning new features, understanding roadmap, proposing improvements

---

### Potential Improvements

1. **Interactive Citation Graphs:** Add interactive Recharts visualization for citations over time

2. **Search Functionality:** Add client-side search for publications

3. **Dark Mode Toggle:** Add user-selectable dark mode (currently class-based)

4. **RSS Feed:** Generate RSS feed for publications

5. **Blog Section:** Add research blog with markdown support

6. **CV Download:** Auto-generate PDF CV from data files

7. **Publication Filters:** Add more advanced filtering (by year, journal, topic)

8. **Figure Lightbox:** Add lightbox/modal for viewing figures in detail

9. **Collaboration Network:** Visualize co-author network

10. **Research Timeline:** Interactive timeline of research projects

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 📚 Resources

> **Purpose:** Links to external documentation, tools, and community resources
>
> **When to use this section:** Learning about technologies, finding documentation, getting help

---

### Project Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** (this file) - Comprehensive technical reference for developers and AI assistants
- **[CLAUDE.md](./CLAUDE.md)** - AI assistant quick reference and startup guide
- **[AGENTS.md](./docs/AGENTS.md)** - AI development protocols, prompting guidelines, and best practices
- **[README.md](./README.md)** - Project overview and user documentation
- **[NVM_SETUP.md](./docs/NVM_SETUP.md)** - Node version management setup instructions

### External Documentation

- **Next.js:** https://nextjs.org/docs
- **React:** https://react.dev/
- **TypeScript:** https://www.typescriptlang.org/docs/
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Shadcn/ui:** https://ui.shadcn.com/
- **NASA ADS API:** https://ui.adsabs.harvard.edu/help/api/

### Tools

- **Node Version Manager:** https://github.com/nvm-sh/nvm
- **GitHub Actions:** https://docs.github.com/en/actions
- **GitHub Pages:** https://docs.github.com/en/pages

### Community

- **Next.js Discord:** https://nextjs.org/discord
- **Tailwind Discord:** https://tailwindcss.com/discord
- **Shadcn/ui GitHub:** https://github.com/shadcn/ui

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 📝 Changelog

> **Purpose:** Track major changes and updates to this documentation
>
> **When to use this section:** Understanding recent changes, tracking documentation evolution

---

### 2025-10-29
- Added "How to Use This Document" section with role-based reading paths
- Added visual separators (icons and horizontal rules) to all 18 major sections
- Added purpose blocks to all major sections explaining when to use each section
- Added "Jump to Top" navigation links throughout document (~15 locations)
- Created Architecture Quick Reference companion file for fast topic lookup
- Added navigation tips in CLAUDE.md for using ARCHITECTURE.md more effectively
- Improved document navigation and reduced cognitive load while keeping unified structure

### 2025-10-25
- Added cross-references to AGENTS.md throughout document
- Added "AI Development" subsection in Best Practices
- Added "Project Documentation" section in Resources
- Updated header with related documentation links
- Improved documentation discoverability and navigation

### 2025-10-24
- Initial architecture documentation created
- Comprehensive reference for developers and AI assistants
- Documented all workflows, scripts, and data structures

---

## License

This project is open source. Research content and publications are subject to respective journal copyright policies.

---

**For questions or issues, please open an issue on GitHub or contact the maintainer.**
