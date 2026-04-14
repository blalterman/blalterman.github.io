# Ben & Publications Page Restructuring Plan

**Date:** 2025-10-29
**Status:** In Progress
**Goal:** Transform Ben and Publications pages from single-page layouts to card-based overview pages with dynamic subpages

---

## Table of Contents
1. [Overview](#overview)
2. [Current Structure](#current-structure)
3. [Proposed Structure](#proposed-structure)
4. [Implementation Plan](#implementation-plan)
5. [Data Structure Changes](#data-structure-changes)
6. [Documentation Updates](#documentation-updates)
7. [Testing Checklist](#testing-checklist)
8. [Verification Results](#verification-results)

---

## Overview

### Goals
- **Consistency:** All major pages (Research, Ben, Publications) use card-based navigation
- **UX:** Reduce scrolling, clearer hierarchy, faster navigation to specific content
- **Maintainability:** Dynamic routes reduce code duplication
- **Data-Driven:** Follow existing architecture patterns (JSON-based content)

### User Preferences
- URL structure: `/ben/[slug]` pattern (follows Research pattern)
- Routing: Dynamic routes for both Ben and Publications
- Card design: Text-only cards (no images)
- Static export: 100% compatible with GitHub Pages

---

## Current Structure

### Ben Page (`/ben`)
**File:** `/src/app/ben/page.tsx`
**Layout:** Single page with 3 cards stacked vertically
**Data:** `/public/data/ben-page.json`

**Current Cards:**
1. **Research Vision** (Telescope icon) - 2 paragraphs
2. **Team Ethos** (Compass icon) - 3 paragraphs
3. **Mentorship Philosophy** (HeartHandshake icon) - 3 paragraphs

**Current JSON Schema:**
```json
{
  "heading": "About Ben",
  "tagline": "How I ask big questions and who I ask them with.",
  "sections": [
    {
      "heading": "Research Vision",
      "icon": "Telescope",
      "paragraphs": ["...", "..."]
    }
  ]
}
```

### Publications Page (`/publications`)
**File:** `/src/app/publications/page.tsx`
**Layout:** Single page with metrics + 7 conditional tables
**Data:** `ads_publications.json`, `ads_metrics.json`

**Current Tables:**
1. PhD Thesis (conditional, `phdthesis` type)
2. Refereed Publications (`article` type)
3. Datasets (conditional, `dataset` type)
4. Conference Proceedings (conditional, `inproceedings` type)
5. Conference Presentations (conditional, `abstract` type)
6. White Papers (conditional, `techreport` type)
7. Pre-Prints (conditional, `eprint` type)

---

## Proposed Structure

### Ben Page

#### Overview Page (`/ben`)
**File:** `/src/app/ben/page.tsx`
**Layout:** Card grid (responsive: 1 col mobile, 2 cols tablet, 3 cols desktop)
**Content:** Heading, tagline, 3 clickable cards

**Card Contents:**
- Icon (from Lucide React)
- Title
- Excerpt (first ~100 chars or custom short description)
- "Details" button with arrow icon → links to subpage

#### Dynamic Subpages (`/ben/[slug]`)
**File:** `/src/app/ben/[slug]/page.tsx`
**Pattern:** Single template generates 3 static pages via `generateStaticParams()`

**Generated Routes:**
- `/ben/research-vision`
- `/ben/team-ethos`
- `/ben/mentorship-philosophy`

**Page Contents:**
- Breadcrumb navigation (Home > Ben > [Current Topic])
- Title with icon
- Full paragraph content
- Optional: related links or navigation

#### New JSON Schema
```json
{
  "heading": "About Ben",
  "tagline": "How I ask big questions and who I ask them with.",
  "sections": [
    {
      "title": "Research Vision",
      "slug": "research-vision",
      "icon": "Telescope",
      "excerpt": "My approach to asking fundamental questions about the solar corona and heliosphere.",
      "paragraphs": ["...", "..."],
      "published": true
    },
    {
      "title": "Team Ethos",
      "slug": "team-ethos",
      "icon": "Compass",
      "excerpt": "How I build collaborative teams and foster inclusive research environments.",
      "paragraphs": ["...", "...", "..."],
      "published": true
    },
    {
      "title": "Mentorship Philosophy",
      "slug": "mentorship-philosophy",
      "icon": "HeartHandshake",
      "excerpt": "My commitment to supporting the next generation of scientists.",
      "paragraphs": ["...", "...", "..."],
      "published": true
    }
  ]
}
```

---

### Publications Page

#### Overview Page (`/publications`)
**File:** `/src/app/publications/page.tsx`
**Layout:** Metrics display at top, then card grid for categories

**Card Contents:**
- Icon (from Lucide React)
- Category title
- Count badge (number of publications)
- Short description
- "View" button → links to category subpage

**Conditional Rendering:** Only show cards for categories with publications

#### Dynamic Subpages (`/publications/[category]`)
**File:** `/src/app/publications/[category]/page.tsx`
**Pattern:** Single template generates up to 7 static pages via `generateStaticParams()`

**Generated Routes:**
- `/publications/phd-thesis`
- `/publications/refereed`
- `/publications/datasets`
- `/publications/proceedings`
- `/publications/presentations`
- `/publications/white-papers`
- `/publications/preprints`

**Page Contents:**
- Breadcrumb navigation (Home > Publications > [Category])
- Category title with icon
- Full publication table (existing table implementation)
- Link back to overview

#### New Data File: `publications-categories.json`
```json
{
  "heading": "Publications",
  "tagline": "Peer-reviewed research, datasets, and conference contributions",
  "categories": [
    {
      "title": "PhD Thesis",
      "slug": "phd-thesis",
      "icon": "GraduationCap",
      "description": "Doctoral dissertation",
      "publicationType": "phdthesis",
      "showCitations": false
    },
    {
      "title": "Refereed Publications",
      "slug": "refereed",
      "icon": "BookOpen",
      "description": "Peer-reviewed journal articles",
      "publicationType": "article",
      "showCitations": true
    },
    {
      "title": "Datasets",
      "slug": "datasets",
      "icon": "Database",
      "description": "Published research datasets",
      "publicationType": "dataset",
      "showCitations": false
    },
    {
      "title": "Conference Proceedings",
      "slug": "proceedings",
      "icon": "FileText",
      "description": "Published conference papers",
      "publicationType": "inproceedings",
      "showCitations": false
    },
    {
      "title": "Conference Presentations",
      "slug": "presentations",
      "icon": "Presentation",
      "description": "Conference talks and poster presentations",
      "publicationType": "abstract",
      "showCitations": false
    },
    {
      "title": "White Papers",
      "slug": "white-papers",
      "icon": "FileText",
      "description": "Technical reports and white papers",
      "publicationType": "techreport",
      "showCitations": false
    },
    {
      "title": "Pre-Prints",
      "slug": "preprints",
      "icon": "ScrollText",
      "description": "Manuscripts submitted for publication",
      "publicationType": "eprint",
      "showCitations": false
    }
  ]
}
```

---

## Implementation Plan

### Phase 1: Ben Page Restructuring

#### Task 1.1: Update `ben-page.json`
**File:** `/public/data/ben-page.json`
**Changes:**
- Rename `heading` field to `title` in sections
- Add `slug` field to each section
- Add `excerpt` field to each section
- Add `published` field (default true)

#### Task 1.2: Rewrite Ben Overview Page
**File:** `/src/app/ben/page.tsx`

**Implementation:**
- Import Card components from shadcn/ui
- Load `ben-page.json`
- Filter published sections (dev shows all, production filters)
- Render card grid layout (responsive)
- Each card links to `/ben/[slug]`
- Include icon mapping for Lucide React icons

**Pattern to follow:** `/src/components/featured-research.tsx`

#### Task 1.3: Create Ben Dynamic Subpages
**File:** `/src/app/ben/[slug]/page.tsx`

**Implementation:**
- `generateStaticParams()` - reads `ben-page.json`, returns slugs
- Filter published sections in production
- Find section by slug
- Render page with title, icon, paragraphs
- Add breadcrumb navigation
- Handle 404 for invalid slugs (redirect to `/ben`)

**Pattern to follow:** `/src/app/research/[slug]/page.tsx`

#### Task 1.4: Test Ben Pages
- Verify `/ben` loads overview
- Verify `/ben/research-vision` loads correctly
- Verify `/ben/team-ethos` loads correctly
- Verify `/ben/mentorship-philosophy` loads correctly
- Test navigation from cards
- Test breadcrumb navigation

---

### Phase 2: Publications Page Restructuring

#### Task 2.1: Create `publications-categories.json`
**File:** `/public/data/publications-categories.json`

**Content:** See "New Data File" section above

#### Task 2.2: Rewrite Publications Overview Page
**File:** `/src/app/publications/page.tsx`

**Implementation:**
- Keep metrics display at top (unchanged)
- Load `publications-categories.json`
- Load `ads_publications.json`
- For each category, count publications with `getPublicationsByType()`
- Render card grid (conditional - only if count > 0)
- Each card shows icon, title, count, description
- Each card links to `/publications/[category]`

#### Task 2.3: Create Publications Dynamic Subpages
**File:** `/src/app/publications/[category]/page.tsx`

**Implementation:**
- `generateStaticParams()` - reads `publications-categories.json`, returns slugs
- Filter categories with publications > 0
- Find category by slug
- Load publications with `getPublicationsByType()`
- Render table (reuse existing table component logic)
- Add breadcrumb navigation
- Handle 404 for invalid categories (redirect to `/publications`)

#### Task 2.4: Test Publications Pages
- Verify `/publications` loads overview with metrics + cards
- Verify each category subpage loads correctly
- Verify conditional rendering (empty categories hidden)
- Test table rendering on subpages
- Test navigation from cards
- Test breadcrumb navigation

---

### Phase 3: Documentation Updates

#### Task 3.1: Update ARCHITECTURE.md § Component Architecture
**File:** `ARCHITECTURE.md`
**Lines:** 790-814

**Changes:**
- Update Ben page section to show overview + dynamic routes pattern
- Update Publications page section to show overview + dynamic routes pattern
- Document new file structure

**Before (Ben):**
```markdown
├── ben/
│   ├── page.tsx               # Personal philosophy page (/ben)
│   │   ├── Loads ben-page.json (heading, tagline, sections array)
│   │   ├── Dynamic card generation from sections array
│   │   ├── Icon mapping with Lucide React (Telescope, Compass)
│   │   └── Shadcn/ui Card components for each section
```

**After (Ben):**
```markdown
├── ben/
│   ├── page.tsx               # Ben overview page (/ben) - card grid
│   │   ├── Loads ben-page.json (heading, tagline, sections array)
│   │   ├── Filters published sections (environment-aware)
│   │   ├── Card grid layout (responsive 1/2/3 columns)
│   │   ├── Icon mapping with Lucide React
│   │   └── Links to /ben/[slug] subpages
│   │
│   ├── [slug]/
│   │   └── page.tsx           # Dynamic Ben subpages
│   │       ├── generateStaticParams() from ben-page.json
│   │       ├── Finds section by slug
│   │       ├── Renders title, icon, full paragraphs
│   │       └── Breadcrumb navigation
```

**Similar changes for Publications section**

#### Task 3.2: Update ARCHITECTURE.md § Dynamic Route System
**File:** `ARCHITECTURE.md`
**Lines:** 633-760

**Changes:**
- Add subsection: "Ben Pages Dynamic Routes"
- Add subsection: "Publications Pages Dynamic Routes"
- Document `generateStaticParams()` implementation for each
- Show code examples

**Structure:**
```markdown
## Dynamic Route System

### Overview
[existing intro]

### Research Pages (Existing Pattern)
[existing content]

### Ben Pages
- Overview page at /ben
- Dynamic routes at /ben/[slug]
- generateStaticParams() implementation
- Data loading pattern
- Environment-aware publishing

### Publications Pages
- Overview page at /publications
- Dynamic routes at /publications/[category]
- generateStaticParams() implementation
- Category filtering logic
- Conditional rendering
```

#### Task 3.3: Update ARCHITECTURE.md § Data Management
**File:** `ARCHITECTURE.md`
**Lines:** 1164-1345

**Changes:**
- Add section for `ben-page.json` (after skills.json around line 1345)
- Add section for `publications-categories.json`
- Document schema for each
- Show examples

**Template:**
```markdown
#### `ben-page.json`
**Purpose:** Defines Ben page overview structure and subpage content
**Type:** Manual (curated)
**Used by:** `/src/app/ben/page.tsx`, `/src/app/ben/[slug]/page.tsx`
**Location:** `/public/data/ben-page.json`

**Structure:**
[schema and examples]
```

#### Task 3.4: Update ARCHITECTURE.md § Directory Structure
**File:** `ARCHITECTURE.md`
**Lines:** 76-186

**Changes:**
- Add `ben-page.json` to data files list
- Add `publications-categories.json` to data files list
- Add `publications-page.json` if it exists
- Mark each as MANUAL

#### Task 3.5: Update ARCHITECTURE.md § Common Tasks
**File:** `ARCHITECTURE.md`
**Lines:** 2017-2163

**Changes:**
- Rewrite "Add a New Section to the Ben Page" task
  - Update to reflect subpage pattern
  - Show new JSON schema
  - Document slug generation
  - Add workflow steps

**Add new task:** "Add a New Ben Subpage"
```markdown
## Task: Add a New Ben Subpage

### Goal
Add a new section to the Ben page with its own dedicated subpage.

### Steps
1. Edit `/public/data/ben-page.json`
2. Add new object to sections array with required fields
3. Rebuild site: `npm run build`
4. New page appears at `/ben/[slug]`

### Example
[JSON example with slug, title, excerpt, paragraphs, published]

### Notes
- Slug becomes the URL path
- Published defaults to true
- Set published: false for drafts (visible in dev only)
```

**Add new task:** "Add a New Publications Category" (rarely needed)

#### Task 3.6: Update CLAUDE.md § Data-Driven Architecture
**File:** `CLAUDE.md`
**Lines:** 91-103

**Changes:**
Update manual data file list:
```markdown
**Manual Data** (curated):
- **Research:** `research-projects.json`, `page-figure-mappings.json`, `research-paragraphs.json`
- **Ben Page:** `ben-page.json`
- **Publications:** `publications-categories.json`
- **Professional:** `education.json`, `positions.json`, `skills.json`
- **Page Overviews:** `research-page.json`, `experience-page.json`, `publications-page.json`, `biography-homepage.json`
```

#### Task 3.7: Update CLAUDE.md § Dynamic Route System
**File:** `CLAUDE.md`
**Lines:** 105-131

**Changes:**
Add after existing dynamic route content:
```markdown
**Other Dynamic Pages:** The same pattern is used for:
- **Ben page:** `/ben` (overview) + `/ben/[slug]` (subpages for each topic)
- **Publications page:** `/publications` (overview) + `/publications/[category]` (subpages for each publication type)

All pages are statically generated at build time using `generateStaticParams()`.

📘 **See [ARCHITECTURE.md § Dynamic Route System](./ARCHITECTURE.md#dynamic-route-system) for complete documentation**
```

---

### Phase 4: Testing & Verification

#### Task 4.1: Development Testing
```bash
npm run dev
```

**Test checklist:**
- [ ] `/ben` loads overview page with 3 cards
- [ ] `/ben/research-vision` loads subpage with full content
- [ ] `/ben/team-ethos` loads subpage with full content
- [ ] `/ben/mentorship-philosophy` loads subpage with full content
- [ ] `/publications` loads overview with metrics + category cards
- [ ] `/publications/refereed` loads table
- [ ] `/publications/datasets` loads table (if data exists)
- [ ] Other publication category pages load correctly
- [ ] Navigation links in header work
- [ ] Mobile navigation works
- [ ] Card links work
- [ ] Breadcrumb navigation works
- [ ] Invalid slugs redirect properly

#### Task 4.2: Build & Static Export
```bash
npm run build
```

**Verify:**
- [ ] Build completes without errors
- [ ] All Ben pages generated in `/out/ben/`
- [ ] All Publications pages generated in `/out/publications/`
- [ ] Check file structure matches expectations

**Expected output:**
```
out/
  ben/
    index.html
    research-vision/
      index.html
    team-ethos/
      index.html
    mentorship-philosophy/
      index.html
  publications/
    index.html
    refereed/
      index.html
    phd-thesis/
      index.html
    [other categories]/
      index.html
```

#### Task 4.3: Production Testing
```bash
# Serve the static build locally
npx serve out
```

**Test all routes again in production build**

---

## Data Structure Changes

### ben-page.json

**Before:**
```json
{
  "heading": "About Ben",
  "tagline": "How I ask big questions and who I ask them with.",
  "sections": [
    {
      "heading": "Research Vision",
      "icon": "Telescope",
      "paragraphs": [
        "I'm driven by big questions...",
        "My research focuses on..."
      ]
    }
  ]
}
```

**After:**
```json
{
  "heading": "About Ben",
  "tagline": "How I ask big questions and who I ask them with.",
  "sections": [
    {
      "title": "Research Vision",
      "slug": "research-vision",
      "icon": "Telescope",
      "excerpt": "My approach to asking fundamental questions about the solar corona and heliosphere.",
      "paragraphs": [
        "I'm driven by big questions...",
        "My research focuses on..."
      ],
      "published": true
    }
  ]
}
```

**Schema Changes:**
- Rename: `heading` → `title`
- Add: `slug` (string, URL-safe)
- Add: `excerpt` (string, ~100 chars for card preview)
- Add: `published` (boolean, optional, defaults to true)

### publications-categories.json (NEW)

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
- `heading` (string): Page heading
- `tagline` (string): Page subtitle
- `categories` (array):
  - `title` (string): Display name
  - `slug` (string): URL path segment
  - `icon` (string): Lucide React icon name
  - `description` (string): Short description for card
  - `publicationType` (string): Matches ADS publication type
  - `showCitations` (boolean): Whether to show citations column in table

---

## Documentation Updates

### Files to Update

**CRITICAL:**
1. `ARCHITECTURE.md` § Component Architecture (lines 790-814)
2. `ARCHITECTURE.md` § Dynamic Route System (lines 633-760) - add 2 subsections
3. `ARCHITECTURE.md` § Data Management (lines 1164-1345) - add 2 sections
4. `CLAUDE.md` § Dynamic Route System (lines 105-131)

**IMPORTANT:**
5. `ARCHITECTURE.md` § Directory Structure (lines 76-186)
6. `ARCHITECTURE.md` § Task: Add New Section to Ben Page (lines 2017-2163) - rewrite
7. `ARCHITECTURE.md` § Common Tasks (add 2 new tasks)
8. `CLAUDE.md` § Data-Driven Architecture (lines 91-103)

**OPTIONAL:**
9. `ARCHITECTURE.md` § Data Flow Architecture (lines 190-265) - add diagrams
10. `README.md` § Research Content Data (lines 40-56) - fix filename references

---

## Testing Checklist

### Navigation Links (All Should Continue Working)
- [ ] Header "Ben" link → `/ben`
- [ ] Header "Publications" link → `/publications`
- [ ] Mobile nav "Ben" link → `/ben`
- [ ] Mobile nav "Publications" link → `/publications`
- [ ] Homepage "Read my full story" link → `/ben`
- [ ] Research page "View All Publications" button → `/publications`

### Ben Page Routes
- [ ] `/ben` loads overview page
- [ ] Overview displays 3 cards in grid
- [ ] Each card has icon, title, excerpt, "Details" button
- [ ] Click "Research Vision" card → `/ben/research-vision`
- [ ] Click "Team Ethos" card → `/ben/team-ethos`
- [ ] Click "Mentorship Philosophy" card → `/ben/mentorship-philosophy`
- [ ] Each subpage displays full content
- [ ] Breadcrumb navigation works
- [ ] Invalid slug (e.g., `/ben/invalid`) redirects to `/ben`

### Publications Page Routes
- [ ] `/publications` loads overview page
- [ ] Metrics display at top (unchanged)
- [ ] Category cards display below metrics
- [ ] Only categories with publications show cards
- [ ] Each card shows icon, title, count, description
- [ ] Click "Refereed Publications" card → `/publications/refereed`
- [ ] Refereed page displays full table
- [ ] Click other category cards load correct tables
- [ ] Empty categories don't show cards on overview
- [ ] Empty categories don't generate routes
- [ ] Invalid slug redirects to `/publications`

### Build & Static Export
- [ ] `npm run build` completes without errors
- [ ] `/out/ben/index.html` exists
- [ ] `/out/ben/research-vision/index.html` exists
- [ ] `/out/ben/team-ethos/index.html` exists
- [ ] `/out/ben/mentorship-philosophy/index.html` exists
- [ ] `/out/publications/index.html` exists
- [ ] All publication category pages exist in `/out/publications/`
- [ ] Serve static build and test all routes

### Responsive Design
- [ ] Cards display 1 column on mobile
- [ ] Cards display 2 columns on tablet
- [ ] Cards display 3 columns on desktop
- [ ] Tables remain scrollable on mobile
- [ ] Navigation menus work on all screen sizes

---

## Verification Results

### Cross-Reference Analysis (Completed)

**All existing references to `/ben` and `/publications` verified as safe:**

1. **Navigation Components**
   - `/src/components/header.tsx` (lines 22, 24) - ✅ Safe
   - `/src/components/mobile-nav.tsx` (lines 37, 43) - ✅ Safe

2. **Content Components**
   - `/src/components/about.tsx` (lines 40-42) - ✅ Safe
   - `/src/components/featured-research.tsx` (lines 54-57) - ✅ Safe
   - `/src/components/research.tsx` (line 75) - ✅ Safe

3. **No References Found In**
   - Python scripts (`/scripts/`) - ✅ No conflicts
   - JSON data files (`/public/data/`) - ✅ No conflicts
   - GitHub workflows (`.github/workflows/`) - ✅ No conflicts

**Routing Compatibility:**
- Static routes (`/ben/page.tsx`) take precedence over dynamic routes
- Dynamic routes (`/ben/[slug]/page.tsx`) won't conflict
- Same pattern already proven working in Research pages

**Conclusion:** All existing links will continue working. No code changes required outside of the restructuring itself.

---

## Benefits Summary

### For Users
✅ **Clearer Navigation** - Card-based overview makes content easier to browse
✅ **Reduced Scrolling** - Content distributed across focused pages
✅ **Faster Access** - Direct links to specific topics or publication types
✅ **Consistent Experience** - All major pages follow same pattern

### For Developers
✅ **Less Code Duplication** - One template generates multiple pages
✅ **Easier Maintenance** - Update logic in one place
✅ **Data-Driven** - Add new pages by editing JSON, not code
✅ **Proven Pattern** - Already working successfully for Research pages

### For Content Management
✅ **Simple Workflow** - Edit JSON + rebuild = new page
✅ **Draft Support** - Environment-aware publishing (like Research)
✅ **No Code Changes** - Content updates don't require React knowledge
✅ **Scalable** - Easy to add new sections or categories

---

## Next Steps

1. ✅ Create this plan document
2. ⏳ Execute Phase 1: Ben Page restructuring
3. ⏳ Execute Phase 2: Publications Page restructuring
4. ⏳ Execute Phase 3: Documentation updates
5. ⏳ Execute Phase 4: Testing & verification
6. ⏳ Commit changes with descriptive message
7. ⏳ Deploy to GitHub Pages
8. ⏳ Verify production site

---

## Notes

- This restructuring is **fully backward compatible** - all existing links continue working
- Static site generation ensures **100% GitHub Pages compatibility**
- The pattern follows the **proven Research page implementation**
- All pages are **pre-rendered at build time** - no runtime server needed
- Adding new Ben subpages will be **as simple as editing JSON** and rebuilding

---

**End of Plan Document**
