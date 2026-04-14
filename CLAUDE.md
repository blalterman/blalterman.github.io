# CLAUDE.md

> **AI Assistant Quick Reference**
>
> This file provides essential guidance for Claude Code and other AI assistants working with this repository.
>
> **📘 For detailed architecture:** [ARCHITECTURE.md](./ARCHITECTURE.md)
> **📘 For AI behavior protocols:** [AGENTS.md](./docs/AGENTS.md)

---

## Project Overview

**Type:** Academic portfolio website (Next.js + TypeScript + Tailwind CSS)

**Owner:** B. L. Alterman, Research Astrophysicist at NASA Goddard Space Flight Center

**Key Features:**
- Statically generated site deployed to GitHub Pages
- Automated data pipeline fetching publications and citations from NASA ADS
- Dynamic route system: single template generates all research pages from JSON data
- Zero-maintenance content updates via JSON files
- CV PDF auto-compiled and hosted via cross-repo GitHub Action from private CV repo

**Tech Stack:** Next.js 15 (App Router), TypeScript 5, Tailwind CSS, Shadcn/ui, Python automation

📘 **See [ARCHITECTURE.md § Technology Stack](./ARCHITECTURE.md#technology-stack) for complete dependencies**

**💡 Navigation Tips for ARCHITECTURE.md:**
- Use [Reading Paths by Role](./ARCHITECTURE.md#how-to-use-this-document) to jump to relevant sections for your task
- Use [Quick Reference](./docs/architecture-quick-reference.md) to find specific topics quickly

---

## Quick Start Commands

```bash
# Development (runs on port 9002 with Turbopack)
npm run dev

# Build for production (static export)
npm run build

# Type checking
npm run typecheck

# Linting
npm run lint

# Python scripts (requires dependencies)
pip install -r scripts/requirements.txt
python scripts/create_research_page.py
```

---

## AI Assistant Protocols

**This repository has specific guidelines for AI behavior and prompting.**

### Key Protocols

1. **Prompt Improvement** - For moderate-to-complex tasks, proactively analyze prompts before execution for:
   - Clarity & specificity
   - Missing context or constraints
   - Efficiency optimization opportunities
   - Agent selection recommendations

2. **Human Review Required** - All AI-generated code must be reviewed by human developer

3. **Follow Project Conventions** - Use Next.js patterns, semantic HTML in React components, maintain type safety

### When to Apply Prompt Analysis

**Analyze for moderate/complex tasks:**
- Multi-step workflows (2-4+ steps)
- Planning, implementation, or architectural changes
- Ambiguous scope requiring interpretation
- Tasks needing agent coordination or debugging

**Skip for simple tasks:**
- Single file reads or documentation lookups
- Direct git/bash commands
- Clear, specific, single-step requests

📘 **See [AGENTS.md](./docs/AGENTS.md) for complete protocols:**
- [Prompt Improvement Protocol](./docs/AGENTS.md#prompt-improvement-protocol) - Full framework with presentation format
- [Development Conventions](./docs/AGENTS.md#development-conventions) - Complete code standards
- [Prompting Guidelines](./docs/AGENTS.md#prompting-guidelines) - Best practices for users
- [Agent Use Cases](./docs/AGENTS.md#agent-use-cases) - Task categories and examples

---

## Critical Architecture Concepts

### 1. Data-Driven Architecture

**All content lives in JSON files** at `/public/data/` - no hardcoded content in React components.

**Automated Data** (updated weekly by GitHub Actions):
- `ads_publications.json`, `ads_metrics.json`, `citations_by_year.json`
- `research-figures-with-captions.json`
- `publication_statistics.json`, `invited_metrics.json` (aggregated from multiple sources)

**Manual Data** (curated):
- **Research:** `research-projects.json`, `page-figure-mappings.json`, `research-paragraphs.json`
- **Ben Page:** `ben-page.json`
- **Publications:** `publications-categories.json`, `non_ads_publications.json`, `invited_conferences.json`, `invited_presentations.json`, `invited_public.json`
- **Professional:** `education.json`, `positions.json`, `skills.json`
- **Page Overviews:** `research-page.json`, `publications-page.json`, `experience-page.json`, `biography-homepage.json`

**Important:** `ads_publications.json` contains only ADS-indexed publications (overwritten weekly). Non-ADS entries (conferences without bibcodes, Zenodo white papers) live in `non_ads_publications.json` to survive weekly updates. Both are merged at load time via `loadAllPublications()` in `data-loader.ts`.

📘 **See [ARCHITECTURE.md § Data Management](./ARCHITECTURE.md#data-management) for complete data structure documentation**

### 2. Dynamic Route System ⚡ **Most Important!**

**Single React component generates multiple static pages from JSON data** - this pattern is used across Research, Ben, and Publications pages.

**Research Pages:**
- File: `/src/app/research/[slug]/page.tsx`
- `generateStaticParams()` reads `research-projects.json`
- **Research Overview:** Cards displayed in random order (shuffled at build time)
- **Adding new:** `python scripts/create_research_page.py` OR update 3 JSON files

**Ben Pages:**
- Overview: `/src/app/ben/page.tsx` - card grid linking to subpages
- Subpages: `/src/app/ben/[slug]/page.tsx` - individual topic pages
- `generateStaticParams()` reads `ben-page.json`
- **Adding new:** Edit `ben-page.json` (add section with slug, excerpt, paragraphs)

**Publications Pages:**
- Overview: `/src/app/publications/page.tsx` - metrics + category cards
- Subpages: `/src/app/publications/[category]/page.tsx` - publication tables
- `generateStaticParams()` reads `publications-categories.json`
- **Adding new:** Edit `publications-categories.json` (rarely needed)

**Key Pattern:** All pages use **card-based overview** + **dynamic subpages** for consistent navigation.

**Published Field:** All pages default to published (`true`). To create draft pages visible only in development:
- Add `"published": false` to respective JSON file
- Pages remain accessible at `npm run dev` but won't build in production
- See ARCHITECTURE.md § Common Tasks for complete guide

📘 **See [ARCHITECTURE.md § Dynamic Route System](./ARCHITECTURE.md#dynamic-route-system) for detailed explanation**

### 3. GitHub Actions Automation

**6 workflows** handle data updates and deployment:
- Publications, metrics, citations (weekly Mon updates)
- Timeline plots (triggers after data updates complete)
- PDF→SVG conversion (on upload)
- Figure data generation (on data changes)

**Cross-repo:** The private CV repo (`CV-v3`) has a GitHub Action that compiles the LaTeX CV and pushes `Alterman-CV.pdf` to this repo's `public/` directory every Monday (after ADS data updates).

📘 **See [ARCHITECTURE.md § GitHub Actions Workflows](./ARCHITECTURE.md#github-actions-workflows) for complete workflow documentation**

### 4. Component Structure

- **Pages:** `/src/app/` (App Router)
- **Components:** `/src/components/` (custom) + `/src/components/ui/` (Shadcn/ui)
- **Utils:** `/src/lib/` (data loading, publication utils, math rendering)
- **Path Aliases:** `@/*` maps to `./src/*`

📘 **See [ARCHITECTURE.md § Component Architecture](./ARCHITECTURE.md#component-architecture) for detailed structure**

---

## AI Assistant Guidelines

### When Working with This Codebase

**Key Patterns:**
1. **Use path aliases** - Import with `@/*` (maps to `./src/*`)
2. **Data files** - Always in `/public/data/` (never create duplicate `data/` directory)
3. **Research pages** - Edit JSON only, never create React files
4. **Scripts** - Use `utils.py` helpers for consistent paths

**Adding Content Workflows:**

| Task | Method |
|------|--------|
| New research page | `python scripts/create_research_page.py` OR update 3 JSON files |
| New figure | Upload PDF to `/public/paper-figures/pdfs/` → auto-converts to SVG |
| Update publications | Automatic weekly OR run fetch scripts manually |
| Add non-ADS publication | `python scripts/add_non_ads_publication.py` (writes to `non_ads_publications.json`) |
| Update professional info | Edit `education.json`, `positions.json`, `skills.json` |

**Build Configuration:**
- `output: 'export'` in `next.config.ts` (required for GitHub Pages)
- TypeScript/ESLint errors ignored during builds (CI/CD compatibility)
- Images unoptimized (required for static export)
- Port 9002 for development

📘 **See [ARCHITECTURE.md § Development Workflow](./ARCHITECTURE.md#development-workflow) for complete guide**
📘 **See [ARCHITECTURE.md § Common Tasks](./ARCHITECTURE.md#common-tasks) for task-specific instructions**

---

## Python Scripts

All scripts in `/scripts/` use shared `utils.py` for consistent path management:

**Key Scripts:**
- `create_research_page.py` - Interactive CLI for adding research pages (supports `--dry-run`)
- `add_non_ads_publication.py` - Add non-ADS publications to `non_ads_publications.json`
- `fetch_ads_*.py` - NASA ADS API integration (publications, metrics, citations)
- `generate_figure_data.py` - Combines figure metadata with publications
- `generate_publication_statistics.py` - Aggregates stats from all publication sources
- `merge_invited_conferences.py` - Enriches publications with invited talk flags
- `utils.py` - Shared utilities: `get_repo_root()`, `get_public_data_dir()`, `get_public_plots_dir()`

📘 **See [ARCHITECTURE.md § Python Scripts](./ARCHITECTURE.md#python-scripts) for detailed documentation**

---

## Data Flow

```
NASA ADS API → Python Scripts → JSON Files → Next.js Build → GitHub Pages
                                    ↑                              ↑
                    non_ads_publications.json              Alterman-CV.pdf
                    invited_*.json (manual)          (from private CV repo)
```

Weekly automation updates publications and metrics every Monday automatically. The private CV repo also rebuilds and pushes `Alterman-CV.pdf` after data updates.

📘 **See [ARCHITECTURE.md § Data Flow Architecture](./ARCHITECTURE.md#data-flow-architecture) for complete flow diagram**

---

## Troubleshooting Quick Reference

| Issue | Check |
|-------|-------|
| Publications not updating | GitHub Actions logs, verify `ADS_DEV_KEY`/`ADS_ORCID` secrets |
| Research page missing | Verify slug in all 3 JSON files, rebuild site |
| Figure not displaying | Check file exists in `/public/paper-figures/svg/`, verify paths |
| Build failing | Validate JSON syntax, check TypeScript, clear `.next` cache |

📘 **See [ARCHITECTURE.md § Troubleshooting](./ARCHITECTURE.md#troubleshooting) for comprehensive guide**

---

## Important Notes

- **Static Site Generation:** Next.js with `output: 'export'` for GitHub Pages
- **Data-Driven:** All content in JSON files, no hardcoded content
- **Automated Updates:** Publications and metrics update weekly via GitHub Actions
- **Path Management:** Scripts work from any directory using `utils.py`
- **Single Data Directory:** Scripts only write to `/public/data/` (no duplicate `data/`)
- **CV Integration:** Private CV repo generates BibTeX from website JSON data; compiled PDF pushed here automatically

---

## Resources

- **Detailed Architecture:** [ARCHITECTURE.md](./ARCHITECTURE.md)
- **AI Behavior Protocols:** [AGENTS.md](./docs/AGENTS.md)
- **Project README:** [README.md](./README.md)
- **Node Setup:** [NVM_SETUP.md](./docs/NVM_SETUP.md)

---

## Summary for AI Assistants

This is a **data-driven static site** where:

✅ Content lives in JSON files, not React components
✅ Research pages auto-generate from JSON (dynamic routes)
✅ Data updates automatically via GitHub Actions
✅ Adding pages = editing JSON only (no code changes)
✅ Python scripts handle automation with shared utilities

**When you need details, always refer to [ARCHITECTURE.md](./ARCHITECTURE.md)**
**For prompting and behavior protocols, refer to [AGENTS.md](./docs/AGENTS.md)**
- CLAUDE.md