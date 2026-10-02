# Architecture Quick Reference

> **Fast lookup index for ARCHITECTURE.md**
>
> Can't remember where something is? Use this index to jump directly to the relevant section.

## By Topic

### Data Files
- **Where are data files?** → `/public/data/` ([Directory Structure](../ARCHITECTURE.md#directory-structure))
- **Publications data format** → [ads_publications.json](../ARCHITECTURE.md#ads_publicationsjson-3600-lines)
- **Research projects format** → [research-projects.json](../ARCHITECTURE.md#research-projectsjson-65-lines)
- **Ben page data format** → [ben-page.json](../ARCHITECTURE.md#ben-pagejson-40-lines)
- **All data schemas** → [Data Management](../ARCHITECTURE.md#data-management)

### Components
- **Where are components?** → `/src/components/` ([Component Architecture](../ARCHITECTURE.md#component-architecture))
- **Dynamic routes** → [Dynamic Route System](../ARCHITECTURE.md#dynamic-route-system)
- **Page structure** → [Component Architecture](../ARCHITECTURE.md#component-architecture)
- **Utility functions** → [Utility Functions](../ARCHITECTURE.md#utility-functions)

### Automation
- **How do publications update?** → [Update Site Data](../ARCHITECTURE.md#1-update-site-data)
- **How do metrics update?** → [Update Site Data](../ARCHITECTURE.md#1-update-site-data)
- **How do figures convert?** → [Convert PDFs to SVG](../ARCHITECTURE.md#4-convert-pdfs-to-svg)
- **All workflows** → [GitHub Actions Workflows](../ARCHITECTURE.md#github-actions-workflows)

### Configuration
- **next.config.ts** → [Next.js Configuration](../ARCHITECTURE.md#nextconfigts)
- **tsconfig.json** → [TypeScript Configuration](../ARCHITECTURE.md#tsconfigjson)
- **tailwind.config.ts** → [Tailwind Configuration](../ARCHITECTURE.md#tailwindconfigts)
- **All configs** → [Configuration Files](../ARCHITECTURE.md#configuration-files)

### Tasks
- **Add research page** → [Add New Research Page](../ARCHITECTURE.md#add-a-new-research-page)
- **Add figure** → [Add New Figure](../ARCHITECTURE.md#add-a-new-figure)
- **Add Ben section** → [Add Section to Ben Page](../ARCHITECTURE.md#task-add-a-new-section-to-the-ben-page)
- **Update professional info** → [Update Professional Information](../ARCHITECTURE.md#update-professional-information)
- **All tasks** → [Common Tasks](../ARCHITECTURE.md#common-tasks)

### Troubleshooting
- **Publications not updating** → [Troubleshooting: Publications](../ARCHITECTURE.md#issue-publications-not-updating)
- **Research page missing** → [Troubleshooting: Research Pages](../ARCHITECTURE.md#issue-research-page-not-appearing)
- **Figure not showing** → [Troubleshooting: Figures](../ARCHITECTURE.md#issue-figure-not-displaying)
- **Build failing** → [Troubleshooting: Build](../ARCHITECTURE.md#issue-build-failing)
- **All issues** → [Troubleshooting](../ARCHITECTURE.md#troubleshooting)

## By File Type

### React/TypeScript
- **src/app/** → [Component Architecture](../ARCHITECTURE.md#component-architecture)
- **src/components/** → [Key Components](../ARCHITECTURE.md#key-components)
- **src/lib/** → [Utility Functions](../ARCHITECTURE.md#utility-functions)

### Python
- **scripts/** → [Python Scripts](../ARCHITECTURE.md#python-scripts)
- **utils.py** → [Shared Utilities](../ARCHITECTURE.md#shared-utilities-utilspy)
- **create_research_page.py** → [Research Page Creator](../ARCHITECTURE.md#5-create_research_pagepy)

### Data Files
- **public/data/** → [Data Management](../ARCHITECTURE.md#data-management)
- **Automated files** → [Automated Data](../ARCHITECTURE.md#automated-data-files)
- **Manual files** → [Manual Data](../ARCHITECTURE.md#manual-data-files)

### Configuration
- **package.json** → [Package Configuration](../ARCHITECTURE.md#packagejson)
- **next.config.ts** → [Next.js Configuration](../ARCHITECTURE.md#nextconfigts)
- **tsconfig.json** → [TypeScript Configuration](../ARCHITECTURE.md#tsconfigjson)
- **tailwind.config.ts** → [Tailwind Configuration](../ARCHITECTURE.md#tailwindconfigts)

## By Task Frequency

### Daily Tasks
- **Start dev server** → [Local Development](../ARCHITECTURE.md#local-development)
- **Add content** → [Adding Content](../ARCHITECTURE.md#adding-content)
- **Test changes** → [Testing Python Scripts](../ARCHITECTURE.md#testing-python-scripts)

### Weekly Tasks
- **Review automated updates** → [Automated Deployment](../ARCHITECTURE.md#automated-deployment)
- **Check GitHub Actions** → [GitHub Actions Workflows](../ARCHITECTURE.md#github-actions-workflows)

### Occasional Tasks
- **Add research page** → [Add New Research Page](../ARCHITECTURE.md#add-a-new-research-page)
- **Add figure** → [Add New Figure](../ARCHITECTURE.md#add-a-new-figure)
- **Update deps** → [Local Development](../ARCHITECTURE.md#local-development)

### Rare Tasks
- **Change theme** → [Change Theme Colors](../ARCHITECTURE.md#task-change-theme-colors)
- **Update metadata** → [Update Site Metadata](../ARCHITECTURE.md#task-update-site-metadata-seo)
- **Deploy manually** → [Manual Deployment](../ARCHITECTURE.md#manual-deployment)

## By Error Message

### Build Errors
- "Invalid JSON" → [Troubleshooting: Build Failing](../ARCHITECTURE.md#issue-build-failing)
- "Module not found" → [Troubleshooting: Build Failing](../ARCHITECTURE.md#issue-build-failing)
- "Type error" → [Debug Build Issues](../ARCHITECTURE.md#task-debug-build-issues)

### Runtime Errors
- "Figure not displaying" → [Troubleshooting: Figures](../ARCHITECTURE.md#issue-figure-not-displaying)
- "Page not found" → [Troubleshooting: Research Pages](../ARCHITECTURE.md#issue-research-page-not-appearing)

### GitHub Actions Errors
- "Workflow failed" → [Troubleshooting: GitHub Actions](../ARCHITECTURE.md#issue-github-actions-failing)
- "Publications not updating" → [Troubleshooting: Publications](../ARCHITECTURE.md#issue-publications-not-updating)

---

**💡 Tip:** Bookmark this page for quick access to specific sections of ARCHITECTURE.md
