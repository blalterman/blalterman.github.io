# Architecture Documentation

> **Last Updated:** 2026-03-08
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
│       └── deploy.yaml (implied)
│
├── src/
│   ├── app/                          # Next.js App Router pages
│   │   ├── page.tsx                  # Home page (/)
│   │   ├── layout.tsx                # Root layout with metadata
│   │   ├── globals.css               # Global Tailwind styles
│   │   ├── research/
│   │   │   ├── page.tsx              # Research overview (/research)
│   │   │   ├── [slug]/page.tsx       # Dynamic research topic pages
│   │   │   ├── figure/[paper_id]/[figure_id]/page.tsx  # Figure detail pages
│   │   │   └── layout.tsx            # Header + Contact wrapper
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
│   │   ├── research-topic.tsx        # Research topic page component
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
│   ├── Alterman-CV.pdf               # AUTO: CV PDF (pushed by private CV repo)
│   ├── data/                         # JSON data files
│   │   ├── ads_publications.json           # AUTO: Publications from ADS
│   │   ├── ads_metrics.json                # AUTO: Citation metrics
│   │   ├── citations_by_year.json          # AUTO: Yearly citations
│   │   ├── publication_statistics.json     # AUTO: Aggregated publication stats
│   │   ├── invited_metrics.json            # AUTO: Invited talk statistics
│   │   ├── non_ads_publications.json       # MANUAL: Non-ADS publications (merged at load time)
│   │   ├── invited_conferences.json        # MANUAL: Invited conference presentations
│   │   ├── invited_presentations.json      # MANUAL: Other invited presentations
│   │   ├── invited_public.json             # MANUAL: Invited public/outreach talks
│   │   ├── figure-registry.json            # MANUAL: Figure metadata registry
│   │   ├── research-topics/                # MANUAL: Per-topic research data
│   │   │   ├── proton-beams.json
│   │   │   ├── helium-abundance.json
│   │   │   ├── coulomb-collisions.json
│   │   │   └── ...                         # One file per research topic
│   │   ├── ben-page.json                   # MANUAL: Ben page structure & content
│   │   ├── publications-categories.json    # MANUAL: Publication category definitions
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
│   ├── fetch_ads_citations_to_data_dir.py     # Fetch citations data
│   ├── generate_citations_timeline.py         # Generate citations plot
│   ├── generate_h_index_timeline.py           # Generate h-index plot
│   ├── generate_publications_timeline.py      # Generate publications timeline
│   ├── generate_publication_statistics.py     # Aggregate publication stats
│   ├── generate_figure_registry_from_corpus.py # Generate figure registry (manual)
│   ├── merge_invited_conferences.py           # Enrich pubs with invited flags
│   ├── compute_invited_metrics.py             # Generate invited talk metrics
│   ├── add_non_ads_publication.py             # Add non-ADS publications
│   ├── plot_config.py                         # Shared plot styling
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
       │
       ▼
┌──────────────────────────────────────────────┐
│                                              │
│  Manual Data (Research Content)              │
│                                              │
│  ┌──────────────────┐  ┌──────────────────┐  │
│  │ research-topics/ │  │ figure-registry  │  │
│  │ *.json           │  │ .json            │  │
│  │ (Per-topic data) │  │ (Figure metadata)│  │
│  └────────┬─────────┘  └────────┬─────────┘  │
│           └──────────┬──────────┘            │
│                      │                       │
└──────────────────────┼───────────────────────┘
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
- `ads_publications.json` - Publications from NASA ADS (overwritten weekly — non-ADS entries must NOT go here)
- `ads_metrics.json` - Citation metrics and h-index
- `citations_by_year.json` - Annual citation counts
- `publication_statistics.json` - Aggregated stats from all publication sources
- `invited_metrics.json` - Invited talk statistics
- `citations_by_year.svg` - Citation trend visualization

**Manual Data** (curated by maintainer):
- `non_ads_publications.json` - Non-ADS publications (conferences without bibcodes, Zenodo white papers). Merged with `ads_publications.json` at load time via `loadAllPublications()`
- `invited_conferences.json` - Invited conference presentations
- `invited_presentations.json` - Other invited presentations
- `invited_public.json` - Public/outreach talks (merged into "Other Invited" in CV)
- `research-topics/*.json` - Per-topic research data (one file per topic)
- `figure-registry.json` - Figure metadata registry (generated by manual script)
- `education.json` & `positions.json` - Academic and professional history
- `skills.json` - Technical skills data

**Cross-Repo:**
- `Alterman-CV.pdf` - Compiled CV PDF, pushed to `public/` by the private CV repo's GitHub Action. The CV generates its BibTeX from this website's JSON data, making the website the single source of truth for all publications.

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
> - [Generate Timeline Plots](#4-generate-timeline-plots)
> - [Convert PDFs](#5-convert-pdfs-to-svg)
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
    "url": "https://dx.doi.org/... or https://scixplorer.org/abs/.../abstract"
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

**Purpose:** Update yearly citation data and timeline visualizations

**Process:**
1. Run `fetch_ads_citations_to_data_dir.py` (data collection)
   - 7-day caching to avoid redundant API calls
   - Fetch citation histogram per year from ADS
2. Run `generate_citations_timeline.py` (visualization)
   - Generate citations timeline plot
3. Run `generate_h_index_timeline.py` (visualization)
   - Generate h-index timeline plot
4. Commit JSON data and all plots

**Output:**
- `/public/data/citations_by_year.json`
- `/public/plots/citations_by_year.svg`
- `/public/plots/citations_by_year.png`
- `/public/plots/h_index_timeline.svg`
- `/public/plots/h_index_timeline.png`

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

### 4. Generate Timeline Plots

**File:** `.github/workflows/update_plots.yml`

**Trigger:** `workflow_run` (executes after ADS workflows complete successfully) or manual dispatch

**Purpose:** Generate publication, h-index, and citation timeline visualizations after data updates

**Process:**
1. Waits for completion of all 3 ADS data workflows (publications, metrics, citations)
2. Runs `generate_publications_timeline.py` - creates publication counts by year/category
3. Runs `generate_h_index_timeline.py` - creates h-index growth visualization
4. Runs `generate_citations_timeline.py` - creates citation trends visualization
5. Commits generated plots and data files

**Outputs:**
- `/public/data/publications_timeline.json`
- `/public/plots/publications_timeline.svg` and `.png`
- `/public/plots/h_index_timeline.svg` and `.png`
- `/public/plots/citations_by_year.svg` and `.png`

**Key Feature:** Uses `workflow_run` trigger to ensure data dependencies are met before visualization generation

---

### 5. Convert PDFs to SVG

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

### Workflow Dependencies & Triggers

The 5 workflows are orchestrated with specific dependencies and trigger patterns to ensure data consistency and proper update sequencing.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         WEEKLY SCHEDULED UPDATES                         │
│                          (Every Monday, UTC)                             │
└─────────────────────────────────────────────────────────────────────────┘

TIME-BASED TRIGGERS (Parallel Execution):
══════════════════════════════════════════

00:00 UTC ┌──────────────────────────────────────┐
    ┌─────┤ update_annual_citations.yml          │
    │     │ → citations_by_year.json             │
    │     └──────────────────────────────────────┘
    │
03:00 UTC ┌──────────────────────────────────────┐
    ├─────┤ update-ads-metrics.yml                │
    │     │ → ads_metrics.json                    │
    │     └──────────────────────────────────────┘
    │
04:00 UTC ┌──────────────────────────────────────┐
    └─────┤ update-ads-publications.yml           │
          │ → ads_publications.json               │
          │ → invited_metrics.json                │
          │ → publication_statistics.json         │
          └──────────────────────────────────────┘
                        │
                        │ (after all 3 complete)
                        ▼
            ┌──────────────────────────────────────┐
            │ update_plots.yml                     │
            │ TRIGGER: workflow_run (dependency)   │
            │                                       │
            │ → publications_timeline.json/.svg    │
            │ → h_index_timeline.svg/.png          │
            │ → citations_by_year.svg/.png         │
            └──────────────────────────────────────┘

══════════════════════════════════════════
EVENT-BASED TRIGGERS (Independent):
══════════════════════════════════════════

On Push to              ┌──────────────────────────────────────┐
paper-figures/pdfs/     │ convert-pdfs.yml                     │
          └─────────────┤ → paper-figures/svg/*.svg            │
                        └──────────────────────────────────────┘

══════════════════════════════════════════
TRIGGER SUMMARY:
══════════════════════════════════════════

• schedule (cron) ····· 3 workflows (00:00, 03:00, 04:00 UTC Mon)
• workflow_run ········ 1 workflow (plots - waits for data)
• push (path) ········· 1 workflow (PDFs)
• workflow_dispatch ··· All 5 (manual trigger available)
```

**Key Design Decisions:**

1. **Staggered Schedule:** Citations (00:00) → Metrics (03:00) → Publications (04:00) prevents API rate limiting
2. **Dependent Workflow:** Timeline plots wait for all 3 ADS workflows to complete before generating visualizations
3. **Independent Events:** PDF conversion runs independently when figure PDFs are pushed
4. **Manual Overrides:** All workflows support `workflow_dispatch` for on-demand execution

[↑ Back to Table of Contents](#table-of-contents)

---
---

## 🐍 Python Scripts

> **Purpose:** Detailed reference for all automation scripts in `/scripts/` directory
>
> **When to use this section:** Adding new data fetching automation, understanding how figures are processed, debugging data pipeline issues
>
> **Related Sections:** [GitHub Actions Workflows](#github-actions-workflows) • [Data Management](#data-management) • [Common Tasks](#common-tasks)
>
> **Quick Links:**
> - [Shared Utilities](#shared-utilities-utilspy)
> - [Publications Fetcher](#1-fetch_ads_publications_to_data_dirpy)
> - [Metrics Fetcher](#2-fetch_ads_metrics_to_data_dirpy)
> - [Citations Data Fetcher](#3-fetch_ads_citations_to_data_dirpy)
> - [Citations Plot Generator](#4-generate_citations_timelinepy)
> - [Figure Registry Generator](#5-generate_figure_registry_from_corpuspy)
> - [Non-ADS Publication Importer](#8-add_non_ads_publicationpy)

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

### Data Aggregation Pattern

The automation scripts follow a clear **separation of concerns** pattern with three distinct layers:

#### Layer 1: Data Acquisition (Fetch Scripts)

**Purpose:** Retrieve raw data from external APIs and create atomic data files

**Scripts:**
- `fetch_ads_publications_to_data_dir.py` → `ads_publications.json`
- `fetch_ads_metrics_to_data_dir.py` → `ads_metrics.json`
- `fetch_ads_citations_to_data_dir.py` → `citations_by_year.json`

**Characteristics:**
- Each script fetches from a single source (NASA ADS API)
- Outputs one primary JSON file
- No dependencies on other scripts' output
- Run independently on staggered schedule (Monday 00:00, 03:00, 04:00 UTC)

#### Layer 2: Data Enrichment & Aggregation

**Purpose:** Combine multiple data sources into comprehensive datasets

**Master Aggregator:** `generate_publication_statistics.py`
- **Inputs (4 sources):**
  - `ads_metrics.json` (Layer 1)
  - `ads_publications.json` (Layer 1)
  - `invited_presentations.json` (manual)
  - `invited_conferences.json` (manual)
- **Process:**
  - Merges bibliometric metrics with publication counts
  - Computes invited talk statistics
  - Generates comprehensive summary statistics
  - Creates time-series data combining all sources
- **Output:** `publication_statistics.json`

**Other Enrichment Scripts:**
- `merge_invited_conferences.py` - Enriches `ads_publications.json` with invited talk flags
- `compute_invited_metrics.py` - Generates `invited_metrics.json` from publications

**Characteristics:**
- Read from multiple JSON sources
- Cross-reference data via keys (bibcode, slug, year)
- Produce enriched, combined datasets
- Run after Layer 1 completes

#### Layer 3: Visualization

**Purpose:** Generate plots and timeline visualizations from data files

**Scripts:**
- `generate_publications_timeline.py`
  - **Inputs:** `ads_publications.json` + `invited_presentations.json` (optional)
  - **Outputs:** `publications_timeline.json`, `.svg`, `.png` plots

- `generate_citations_timeline.py`
  - **Input:** `citations_by_year.json` (pre-aggregated)
  - **Outputs:** `citations_by_year.svg`, `.png`

- `generate_h_index_timeline.py`
  - **Input:** `ads_metrics.json` (pre-aggregated)
  - **Outputs:** `h_index_timeline.svg`, `.png`

**Characteristics:**
- Read from Layer 1 or Layer 2 outputs
- No API calls - visualization only
- Generate both JSON data and plot files (.svg/.png)
- Triggered by `workflow_run` after data updates complete

#### Benefits of This Pattern

1. **Single Responsibility:** Each script has one clear purpose (fetch OR aggregate OR visualize)
2. **Testability:** Can test aggregation logic without API calls by using mock JSON files
3. **Resilience:** API failures only affect Layer 1; Layers 2-3 can still run with cached data
4. **Flexibility:** Can re-generate visualizations without re-fetching from APIs
5. **Clear Dependencies:** Layer 2 depends on Layer 1; Layer 3 depends on Layers 1-2
6. **Parallel Execution:** Layer 1 scripts run in parallel (staggered for rate limiting)
7. **Caching:** Only Layer 1 implements caching (7-day for citations)

#### Data Flow Example

```
Monday 00:00-04:00 UTC (Layer 1 - Parallel):
├─ fetch_ads_citations → citations_by_year.json
├─ fetch_ads_metrics → ads_metrics.json
└─ fetch_ads_publications → ads_publications.json
           │
           ├─ merge_invited_conferences → ads_publications.json (enriched)
           ├─ compute_invited_metrics → invited_metrics.json
           └─ generate_publication_statistics → publication_statistics.json
                        │
                        └─ (Layer 3 - After all complete):
                           ├─ generate_publications_timeline
                           ├─ generate_citations_timeline
                           └─ generate_h_index_timeline
```

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

### 3. `fetch_ads_citations_to_data_dir.py`

**Purpose:** Fetch annual citation data from NASA ADS (data collection only)

**Features:**
- 7-day caching to prevent redundant API calls
- Rate limiting with Retry-After header handling
- Timezone handling (Eastern Time)
- Separation of concerns (data only, no visualization)

**Process:**
1. Get all bibcodes for ORCID
2. Query citation histogram by year from ADS
3. Separate refereed vs. non-refereed citations
4. Save JSON data only

**Output:**
- `/public/data/citations_by_year.json`

**API Endpoint:** `https://api.adsabs.harvard.edu/v1/metrics`

**Note:** Run `generate_citations_timeline.py` afterward to create plots from this data.

---

### 4. `generate_citations_timeline.py`

**Purpose:** Generate citations timeline plot from cached data (visualization only)

**Features:**
- Reads from existing JSON data (no API calls)
- Matplotlib line plot visualization
- Centralized plot styling via `plot_config.py`
- Matches aesthetic of other timeline plots

**Process:**
1. Load `/public/data/citations_by_year.json`
2. Create styled line plots (refereed + non-refereed)
3. Apply semi-transparent fill under lines
4. Save SVG and PNG to public/plots/

**Output:**
- `/public/plots/citations_by_year.svg`
- `/public/plots/citations_by_year.png`

**Note:** Must run `fetch_ads_citations_to_data_dir.py` first to ensure data is current.

---

### 5. `generate_figure_registry_from_corpus.py`

**Purpose:** Generate `figure-registry.json` from a corpus of paper figure files

**Process:**
1. Scan the figure corpus directory for paper figures
2. Extract metadata (paper ID, figure ID, file paths)
3. Generate registry entries with SVG paths and paper references
4. Write `figure-registry.json` to `/public/data/`

**Output:** `/public/data/figure-registry.json`

**Usage:**
```bash
python scripts/generate_figure_registry_from_corpus.py
```

**Note:** This script is run manually when new figures are added. There is no automated GitHub Actions workflow for figure registry generation.

---

### 6. `fetch_figure_licenses.py`

**Purpose:** Fetch Creative Commons license information for figures

**Process:** Looks up DOI to find licensing info

---

### 8. `add_non_ads_publication.py`

**Purpose:** Add non-ADS publications (conferences without bibcodes, Zenodo white papers) to website data

**Output:** `/public/data/non_ads_publications.json`

**Features:**
- Interactive CLI prompts for publication metadata
- `--dry-run` flag to preview without writing
- `--from-bibtex <file>` flag for batch import from .bib files
- Deduplication check (match by title + year)
- Generates synthetic `NOADS-*` bibcodes for entries without ADS identifiers

**Usage:**
```bash
# Interactive mode
python scripts/add_non_ads_publication.py

# Batch import from BibTeX
python scripts/add_non_ads_publication.py --from-bibtex path/to/file.bib

# Preview mode
python scripts/add_non_ads_publication.py --dry-run
```

**Context:** Created during the CV integration project to migrate non-ADS conferences and Zenodo white papers from the CV's manual .bib files to the website's JSON data.

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

**Topic Pages:** `/src/app/research/[slug]/page.tsx`

```typescript
// Load all raw topic data from JSON files
function loadAllRawTopics(): RawResearchTopicData[] {
  const topicsDir = path.join(process.cwd(), 'public/data/research-topics');
  const files = fs.readdirSync(topicsDir).filter(f => f.endsWith('.json'));
  return files.map(file => {
    const content = fs.readFileSync(path.join(topicsDir, file), 'utf8');
    return JSON.parse(content);
  });
}

export async function generateStaticParams() {
  const topics = loadAllRawTopics();
  const published = filterPublishedProjects(topics);
  return published.map(topic => ({ slug: topic.slug }));
}
```

**Figure Detail Pages:** `/src/app/research/figure/[paper_id]/[figure_id]/page.tsx`

```typescript
function loadFigureRegistry(): FigureRegistry {
  const registryPath = path.join(process.cwd(), 'public/data/figure-registry.json');
  return JSON.parse(fs.readFileSync(registryPath, 'utf8'));
}

export async function generateStaticParams() {
  const registry = loadFigureRegistry();
  return Object.values(registry).map((entry: FigureRegistryEntry) => ({
    paper_id: entry.paper_id,
    figure_id: entry.figure_id,
  }));
}
```

### Build Process

**At Build Time:**
1. `generateStaticParams()` reads all `research-topics/*.json` files
2. Filters to published topics, extracts slugs
3. Next.js generates static HTML for each topic slug:
   - `/out/research/proton-beams.html`
   - `/out/research/helium-abundance.html`
   - `/out/research/coulomb-collisions.html`
   - etc.
4. Separately, figure detail pages read `figure-registry.json` and generate:
   - `/out/research/figure/Alterman_2018_ApJ_864_112/fig_1.html`
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

### Research Topic Organization

**Behavior:** Research topics on `/research` are organized by fundamental research questions

**Implementation:** `/src/app/research/page.tsx`
```typescript
const researchQuestions: ResearchQuestion[] = [
  {
    question: 'Where does the solar wind come from?',
    subtitle: 'Source Identification',
    topics: ['sources-of-the-solar-wind', 'helium-abundance', 'heavy-ion-composition'],
  },
  // ... additional research questions
];
```

**Characteristics:**
- Topics are grouped under parent research questions
- Each question has a subtitle and a list of topic slugs
- Only published topics are displayed (filtered at build time)
- Question sections with no published topics are hidden

### Adding a New Research Page

Create a new JSON file at `public/data/research-topics/<slug>.json`:

```json
{
  "slug": "solar-energetic-particles",
  "title": "Solar Energetic Particles",
  "subtitle": "Brief subtitle for the topic",
  "description": "Brief description for the overview card",
  "primary_figure": {
    "ref": "Paper_ID/fig_N"
  },
  "related_figures": [],
  "related_topics": [],
  "published": true,
  "paper": {
    "id": "Paper_ID",
    "title": "Source paper title",
    "doi": "https://doi.org/...",
    "bibcode": "2024ApJ...960...70A",
    "journal": "The Astrophysical Journal",
    "year": 2024,
    "license": {
      "holder": "American Astronomical Society",
      "year": 2024,
      "type": "CC BY 4.0"
    }
  }
}
```

**Push to main:**
```bash
git add public/data/research-topics/solar-energetic-particles.json
git commit -m "Add solar energetic particles research page"
git push
```

**Result:** Page automatically exists at `/research/solar-energetic-particles`

**No React/TypeScript files need to be created!**

---

### Card-Based Overview Pattern

**Implemented:** 2025-10-29 (Commit: `ab8f371`)

All three major page types (Research, Ben, Publications) now follow a consistent **card-based overview + dynamic subpages** pattern:

```
Overview Page (Card Grid) → Individual Subpages (Dynamic Routes)
```

This architecture provides:
1. **Consistent Navigation:** Users experience identical interaction patterns across all sections
2. **Discoverability:** Card grids with icons and descriptions help users explore content
3. **Scalability:** Adding new pages requires only JSON updates
4. **Single Source of Truth:** One template generates all subpages in each category

---

### 1. Research Pages

**Pattern:** Overview → Dynamic Research Topics → Figure Detail Pages

**Overview Page:** `/src/app/research/page.tsx`
- Displays research topics organized by fundamental questions
- Links to individual research topic pages

**Dynamic Topic Pages:** `/src/app/research/[slug]/page.tsx`
- Generates pages for each research topic
- Data sources: `research-topics/*.json`, `figure-registry.json`
- Renders primary figure, related figures, and topic content via `ResearchTopic` component

**Figure Detail Pages:** `/src/app/research/figure/[paper_id]/[figure_id]/page.tsx`
- Individual pages for each figure in the registry
- Data source: `figure-registry.json`
- Shows full-size figure with metadata and citation info

**Layout:** `/src/app/research/layout.tsx`
- Wraps all research pages (overview, topics, figures) with Header + Contact

**URL Structure:**
- `/research` - Research overview
- `/research/proton-beams` - Individual topic
- `/research/helium-abundance` - Individual topic
- `/research/figure/Alterman_2018_ApJ_864_112/fig_1` - Figure detail
- etc.

---

### 2. Ben Pages

**Pattern:** Card Overview → Dynamic Ben Subpages

**Overview Page:** `/src/app/ben/page.tsx`
- Displays grid of thought leadership topic cards
- Each card shows icon, title, and excerpt
- Links to individual Ben subpages

**Dynamic Subpages:** `/src/app/ben/[slug]/page.tsx`
- Generates pages for each topic (Research Vision, Team Ethos, Mentorship Philosophy, Open Science)
- Data source: `ben-page.json` (single file with `sections` array)

**URL Structure:**
- `/ben` - Card grid overview
- `/ben/research-vision` - Individual topic
- `/ben/team-ethos` - Individual topic
- `/ben/mentorship-philosophy` - Individual topic
- `/ben/open-science` - Individual topic

**Data Schema (`ben-page.json`):**
```json
{
  "heading": "About Ben",
  "tagline": "How I ask big questions and who I ask them with",
  "sections": [
    {
      "title": "Research Vision",
      "slug": "research-vision",
      "icon": "Telescope",
      "excerpt": "1-2 sentence summary for card",
      "paragraphs": ["Full content paragraph 1", "paragraph 2", ...],
      "published": true
    }
  ]
}
```

**Adding New Ben Page:**
1. Edit `public/data/ben-page.json`
2. Add new section to `sections` array with slug, title, icon, excerpt, paragraphs
3. Set `published: true` (or `false` for drafts)
4. Push to main - page automatically exists at `/ben/[slug]`

---

### 3. Publications Pages

**Pattern:** Card Overview → Dynamic Category Pages

**Overview Page:** `/src/app/publications/page.tsx`
- Displays publication metrics dashboard
- Shows grid of publication category cards
- Each card shows count, icon, and description
- Links to individual category pages

**Dynamic Subpages:** `/src/app/publications/[category]/page.tsx`
- Generates pages for each publication category
- Data sources: `publications-categories.json`, `ads_publications.json`
- Includes interactive filtering UI (authorship, year, journal, invited/contributed)

**URL Structure:**
- `/publications` - Metrics dashboard + category card grid
- `/publications/refereed` - Refereed articles table
- `/publications/conferences` - Conference publications table
- `/publications/datasets` - Dataset publications table
- etc.

**Data Schema (`publications-categories.json`):**
```json
{
  "heading": "Publications",
  "tagline": "Peer-reviewed research and data products",
  "categories": [
    {
      "title": "Refereed Articles",
      "slug": "refereed",
      "icon": "BookOpen",
      "description": "Peer-reviewed journal publications",
      "publicationType": "article",
      "showCitations": true,
      "showFilters": true,
      "journalLabel": "Journal",
      "journalField": "journal"
    }
  ]
}
```

**Configuration Options (per category):**
- `showFilters`: Enable/disable interactive filtering UI
- `showCitations`: Show/hide citations column
- `showJournal`: Show/hide journal/venue column
- `showLinks`: Show/hide links column
- `journalLabel`: Custom column header (e.g., "Venue" vs "Journal")
- `journalField`: Which field to display (`"journal"` or `"location"`)

**Adding New Publications Category:**
1. Edit `public/data/publications-categories.json`
2. Add new category to `categories` array
3. Specify `publicationType` to filter publications
4. Configure display options (filters, citations, etc.)
5. Push to main - page automatically exists at `/publications/[slug]`

---

### Environment-Aware Publishing

All three dynamic route systems support **draft pages** via the `published` field:

```typescript
// In generateStaticParams():
const publishedItems = isDev ? allItems : allItems.filter(item => item.published !== false);
```

**Behavior:**
- **Development (`npm run dev`):** All pages accessible, including `published: false`
- **Production (`npm run build`):** Only pages with `published !== false` are generated

**Use Case:** Create and test new pages locally before making them public

---

### Shared Pattern Benefits

1. **Consistency:** Users navigate all major sections identically
2. **Discoverability:** Card grids encourage exploration
3. **Maintainability:** Same routing pattern across all dynamic page types
4. **Scalability:** JSON-only updates to add pages
5. **Type Safety:** TypeScript ensures schema consistency
6. **SEO:** Each page generates individual HTML with proper metadata

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
│   │   └── Topic cards organized by research questions (from research-topics/*.json)
│   │
│   ├── [slug]/page.tsx         # Dynamic research topic pages
│   │   ├── generateStaticParams() reads from research-topics/*.json
│   │   ├── Resolves figure refs against figure-registry.json
│   │   ├── ResearchTopic component with primary + related figures
│   │   └── Math rendering via LaTeX
│   │
│   ├── figure/[paper_id]/[figure_id]/page.tsx  # Figure detail pages
│   │   ├── generateStaticParams() reads from figure-registry.json
│   │   └── Full-size figure display with metadata and citation
│   │
│   └── layout.tsx             # Header + Contact wrapper for all research pages
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

**`research-topic.tsx`** - Research Topic Page Component
- Renders a complete research topic page with primary figure, related figures, and content
- Resolves figure references against the figure registry
- Displays figure attribution (journal, DOI, license)
- Links to figure detail pages
- Responsive layout with constrained figure sizing and white backgrounds

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

**`publication-filters.tsx`** - Interactive Publication Filtering System
- **File:** 429 lines of comprehensive client-side filtering UI
- **Purpose:** Advanced filtering for publication category pages with real-time updates

**Features:**
- **Authorship Filter:** Radio buttons (All / First Author / Co-author)
- **Invited Filter:** Radio buttons for conferences (All / Invited / Contributed)
- **Journal Filter:** Multi-select dropdown with search functionality
- **Year Filter:** Multi-select dropdown with search functionality
- **Active Filter Badges:** Displays current filters with individual remove buttons
- **Filter Count Badge:** Shows number of active filters on filter button
- **Result Count:** "Showing X of Y publications" live update
- **Empty State:** Displays message when no publications match filters
- **Clear All:** Single-click to reset all filters

**Configuration (per category via `publications-categories.json`):**
```typescript
interface PublicationCategory {
  showFilters?: boolean;      // Enable/disable entire filtering UI (default: true)
  showJournal?: boolean;       // Show/hide journal/venue column (default: true)
  journalLabel?: string;       // Custom column header (default: "Journal")
  journalField?: string;       // Field to display: "journal" | "location" (default: "journal")
  showLinks?: boolean;         // Show/hide links column (default: true)
  showCitations?: boolean;     // Show/hide citations column
}
```

**Filter Logic:**
- **AND between filter types:** Must match authorship AND year AND journal
- **OR within filter type:** Match ANY selected journal OR ANY selected year
- **Environment-aware:** Works with both client-side filtering and static generation

**Example Usage:**
```typescript
<PublicationFilters
  publications={filteredPubs}
  categoryData={category}
  labels={{ journal: "Venue" }}  // Custom labels
/>
```

**UI Components Used:**
- Popover for filter panel
- RadioGroup for single-select filters
- MultiSelect for journal/year filters
- Badge for active filter chips
- Button for Apply/Clear actions

**Performance:**
- Client-side filtering via `useMemo` hook
- Re-renders only when filter state or publications change
- Efficient array filtering with early returns

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
const metrics = loadJSONData<ADSMetrics>('ads_metrics.json');
const registry = loadJSONData<FigureRegistry>('figure-registry.json');
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
const topics = loadAllRawTopics(); // from research-topics/*.json
const publishedTopics = filterPublishedProjects(topics);
// Development: all topics | Production: only published topics
```

**Used By:**
- `/src/app/research/page.tsx` - Filter topics on research overview
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
- [publication_statistics.json](#publication_statisticsjson) - Aggregated publication stats
- [invited_metrics.json](#invited_metricsjson) - Invited talk statistics

**Manual Data Files (Curated):**
- [non_ads_publications.json](#non_ads_publicationsjson) - Non-ADS publications (merged with ADS at load time)
- [invited_conferences.json](#invited_conferencesjson) - Invited conference presentations
- [invited_presentations.json](#invited_presentationsjson) - Other invited presentations
- [invited_public.json](#invited_publicjson) - Invited public/outreach talks
- [research-topics/*.json](#research-topicsjson) - Per-topic research data
- [figure-registry.json](#figure-registryjson) - Figure metadata registry
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

#### `publication_statistics.json`

**Updated:** Weekly (generated after publications and metrics update)

**Source:** Generated by `generate_publication_statistics.py`

**Purpose:** Aggregated publication and presentation statistics from all sources

**Inputs:**
- `ads_publications.json` + `non_ads_publications.json` (all publications)
- `ads_metrics.json` (h-index, citation stats)
- `invited_presentations.json` (invited talks)
- `invited_conferences.json` (invited conference presentations)

**Used By:** Publications page (summary statistics display)

---

#### `invited_metrics.json`

**Updated:** Weekly (generated by `compute_invited_metrics.py`)

**Source:** Computed from `ads_publications.json` + invited talk data

**Purpose:** Statistics about invited presentations (counts by year, totals)

**Used By:** Publications page

---

### Manual Data Files

#### `non_ads_publications.json`

**Purpose:** Publications not indexed in NASA ADS (non-ADS conferences, Zenodo white papers)

**Type:** Manual (curated via `add_non_ads_publication.py`)

**Important:** This file exists because the weekly ADS fetch completely overwrites `ads_publications.json`. Non-ADS entries stored here survive weekly updates. Both files are merged at load time via `loadAllPublications()` in `src/lib/data-loader.ts`.

**Structure:**
```json
[
  {
    "bibcode": "NOADS-IAU-CME",
    "title": "Charge-State Dependent Heating...",
    "authors": ["Alterman, B. L."],
    "month": "",
    "year": "2024-05-00",
    "journal": "IAU/CME",
    "publication_type": "inproceedings",
    "citations": 0,
    "url": "",
    "invited": false
  }
]
```

**Key Fields:**
- **bibcode:** Synthetic identifier with `NOADS-` prefix (e.g., `NOADS-Arcetri-2022`)
- Same schema as `ads_publications.json` entries for seamless merging

**Used By:**
- Publications pages (merged with ADS publications at load time)
- CV repo's BibTeX generation script (fetches from live site)

---

#### `invited_conferences.json`

**Purpose:** Invited conference presentations

**Type:** Manual (curated)

**Structure:**
```json
[
  {
    "title": "Collisions in an Expanding Solar Wind (Scene Setting Talk)",
    "authors": ["Alterman, B. L."],
    "year": "2017-07-00",
    "month": "7",
    "publication_type": "inproceedings",
    "citations": 0,
    "invited": true,
    "booktitle": "SHINE Conference",
    "journal": "SHINE Conference",
    "keywords": "invited",
    "url": ""
  }
]
```

**Used By:**
- `generate_publication_statistics.py` (aggregation)
- `merge_invited_conferences.py` (enriches publications with invited flags)
- CV repo's BibTeX generation

---

#### `invited_presentations.json`

**Purpose:** Other invited presentations (seminars, colloquia, tutorials)

**Type:** Manual (curated)

**Structure:** Same schema as `invited_conferences.json`

**Used By:**
- `generate_publication_statistics.py` (aggregation)
- `generate_publications_timeline.py` (timeline visualization)
- CV repo's BibTeX generation

---

#### `invited_public.json`

**Purpose:** Invited public/outreach talks (public lectures, science communication events)

**Type:** Manual (curated). Currently empty — placeholder for future entries.

**Structure:** Same schema as `invited_conferences.json`

**CV Integration:** Merged into "Other Invited Presentations" (`keyword=invitedother`) by the CV's `generate_bibtex_from_website.py`. Entries added here will automatically appear in the CV's "Other Invited Presentations" section on next build.

**Used By:**
- CV repo's BibTeX generation (merged with `invited_presentations.json`)

---

#### `research-topics/*.json`

**Purpose:** Per-topic research data files. Each research topic has its own JSON file in `public/data/research-topics/`.

**Structure (per file):**
```json
{
  "slug": "proton-beams",
  "title": "Proton Beams",
  "subtitle": "Brief subtitle for the topic",
  "description": "Brief description for the overview card",
  "primary_figure": {
    "ref": "Alterman_2018_ApJ_864_112/fig_2"
  },
  "related_figures": [
    {
      "ref": "Alterman_2018_ApJ_864_112/fig_1",
      "relevance": "Description of why this figure is relevant"
    }
  ],
  "related_topics": [],
  "published": false,
  "paper": {
    "id": "Alterman_2018_ApJ_864_112",
    "title": "Paper title",
    "doi": "https://doi.org/...",
    "bibcode": "2018ApJ...864..112A",
    "journal": "The Astrophysical Journal",
    "year": 2018,
    "license": {
      "holder": "American Astronomical Society",
      "year": 2018,
      "type": "CC BY 3.0"
    }
  }
}
```

**Fields:**
- **slug:** URL-safe identifier (used in /research/[slug]), must match the filename
- **title:** Display title (used in headers)
- **subtitle:** Brief subtitle displayed below the title
- **description:** Brief summary (shown on research overview page)
- **primary_figure.ref:** Reference to figure in `figure-registry.json` (format: `paper_id/figure_id`)
- **related_figures:** Array of additional figures with relevance descriptions
- **related_topics:** Slugs of related research topics
- **published:** (optional, boolean) Whether page is visible in production. Defaults to `true`. Set to `false` to hide page in production builds while keeping it visible in development
- **paper:** Source publication metadata including DOI, bibcode, journal, and license

**Used By:**
- Research overview page (/research)
- Research topic pages (generateStaticParams)

---

#### `figure-registry.json`

**Purpose:** Central registry of all figures available for use on research pages. Maps figure references to file paths and metadata.

**Structure:**
```json
{
  "Alterman_2018_ApJ_864_112/fig_1": {
    "paper_id": "Alterman_2018_ApJ_864_112",
    "figure_id": "fig_1",
    "svg_path": "/paper-figures/svg/Alterman_2018_ApJ_864_112_fig_1.svg",
    "alt": "Description of the figure",
    "caption": "Figure caption text"
  }
}
```

**Key Format:** `paper_id/figure_id` — used as the lookup key in topic files' `primary_figure.ref` and `related_figures[].ref` fields

**Generated By:** `scripts/generate_figure_registry_from_corpus.py` (run manually)

**Used By:**
- Research topic pages (resolve figure refs to file paths)
- Figure detail pages (generateStaticParams, display)

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
  - `publicationType` (string | string[]): ADS publication type(s) to filter (`article`, `dataset`, `inproceedings`, `abstract`, `techreport`, `eprint`, `phdthesis`)
  - `showCitations` (boolean): Whether to display citations column in table

**Filter & Display Configuration (Optional):**
  - `showFilters` (boolean): Enable/disable interactive filtering UI (default: `true`)
  - `showJournal` (boolean): Show/hide journal/venue column (default: `true`)
  - `showLinks` (boolean): Show/hide links column (default: `true`)
  - `journalLabel` (string): Custom column header (default: `"Journal"`)
    - Example: `"Venue"` for conferences
  - `journalField` (string): Field to display in column (default: `"journal"`)
    - Options: `"journal"` | `"location"`
    - Use `"location"` for conferences to show venue instead of journal name

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

# Fetch data from NASA ADS
python scripts/fetch_ads_publications_to_data_dir.py
python scripts/fetch_ads_metrics_to_data_dir.py
python scripts/fetch_ads_citations_to_data_dir.py

# Generate visualizations
python scripts/generate_citations_timeline.py
python scripts/generate_h_index_timeline.py
```

**3. Test Figure Registry Generation:**
```bash
python scripts/generate_figure_registry_from_corpus.py
```

---

### Adding Content

#### Add a New Research Page

Create a new topic file at `public/data/research-topics/<slug>.json` with the topic data structure (see [research-topics/*.json](#research-topicsjson) for the full schema).

**Note:** By default, pages are published. To create a draft page visible only in development, add `"published": false` to the topic definition.

**Commit and push:**
```bash
git add public/data/research-topics/new-research-topic.json
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

3. **Regenerate figure registry:**
```bash
python scripts/generate_figure_registry_from_corpus.py
git add public/data/figure-registry.json
git commit -m "Regenerate figure registry"
git push
```

4. **Reference the figure in a topic file** using its registry key (e.g., `Paper_ID/fig_N`) in the `primary_figure.ref` or `related_figures[].ref` field.

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
│   ├── figure/
│   │   └── Alterman_2018_ApJ_864_112/
│   │       ├── fig_1.html
│   │       └── fig_2.html
│   └── ...
├── publications/
│   └── index.html
├── experience/
│   └── index.html
└── _next/
    └── static/...
```

**Note:** Research topics are organized by research questions defined in the overview page component.

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
python -m json.tool public/data/figure-registry.json
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

Use the `published` field in each topic's JSON file to control research page visibility in production while keeping them accessible in development.

**Hide a Research Page:**

1. **Edit `/public/data/research-topics/<slug>.json`:**
```json
{
  "slug": "proton-beams",
  "title": "Proton Beams",
  "published": false
}
```

2. **Rebuild:**
```bash
npm run build
```

**Result:**
- Development (`npm run dev`): Page visible, card appears
- Production (`npm run build`): Page not built, card hidden

**Re-enable a Page:**

Set `"published": true` or remove the field entirely (defaults to true).

**Environment Behavior:**
- **Development:** All pages visible (including unpublished) for testing
- **Production:** Only published pages built and displayed

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
1. Topic file exists at `public/data/research-topics/<slug>.json`
2. File contains valid JSON with correct `slug` field matching the filename
3. `published` field is not set to `false` (or running in development mode)
4. Site was rebuilt after JSON changes
5. No typos in slug names (must match exactly)

**Debug:**
```bash
# List all topic slugs
ls public/data/research-topics/
# Validate a topic file
python -m json.tool public/data/research-topics/<slug>.json
```

---

### Issue: Figure Not Displaying

**Check:**
1. Figure SVG file exists in `/public/paper-figures/svg/`
2. Figure has an entry in `figure-registry.json` with correct `svg_path`
3. Topic file's `primary_figure.ref` or `related_figures[].ref` matches a key in the registry
4. Registry was regenerated after adding new figures

**Regenerate Figure Registry:**
```bash
python scripts/generate_figure_registry_from_corpus.py
git add public/data/figure-registry.json
git commit -m "Regenerate figure registry"
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

4. **Per-Topic Files:** Each research topic gets its own JSON file in `research-topics/`

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
- **NASA ADS / SciX API:** https://scixplorer.org/help/api/

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

### 2026-04-14
- Updated research pages documentation to reflect migration from old system to figure registry architecture
- Removed references to deleted files: `research-projects.json`, `research-paragraphs.json`, `research-figures-with-captions.json`, `page-figure-mappings.json`, `figure-metadata.json`, `research-page.json`
- Removed references to deleted components: `research-figure.tsx`, `featured-research.tsx`, `research.tsx`
- Removed references to deleted scripts: `create_research_page.py`, `generate_figure_data.py`, `test_create_research_page.py`
- Removed `generate-figure-data.yml` workflow documentation
- Added documentation for new data sources: `research-topics/*.json`, `figure-registry.json`
- Added documentation for new route: `/research/figure/[paper_id]/[figure_id]`
- Added documentation for `research-topic.tsx` component and `generate_figure_registry_from_corpus.py` script

### 2026-03-08
- Added documentation for CV integration (cross-repo GitHub Action, BibTeX generation from website JSON)
- Added `non_ads_publications.json`, `invited_conferences.json`, `invited_presentations.json` to Data Management
- Added `publication_statistics.json`, `invited_metrics.json` to Automated Data Files
- Added `add_non_ads_publication.py` script documentation
- Updated Directory Structure with missing data files, scripts, and `Alterman-CV.pdf`
- Updated Data Flow Architecture with non-ADS publications and CV integration flow

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
