# Documentation Index

> **Central Hub for All Project Documentation**
>
> This page provides a comprehensive map of all documentation resources for the B. L. Alterman academic portfolio website.

---

## 📍 Quick Navigation

| Document | Location | Purpose | Audience |
|----------|----------|---------|----------|
| **[README.md](../README.md)** | Root | Project overview, GitHub homepage | End users, first-time visitors |
| **[CLAUDE.md](../CLAUDE.md)** | Root | AI assistant quick reference | AI assistants (startup) |
| **[ARCHITECTURE.md](../ARCHITECTURE.md)** | Root | Complete technical reference | Developers, AI assistants |
| **[AGENTS.md](./AGENTS.md)** | docs/ | AI behavior protocols | AI assistants, developers |
| **[NVM_SETUP.md](./NVM_SETUP.md)** | docs/ | Node version management | Developers (one-time setup) |
| **[blueprint.md](./archive/blueprint.md)** | docs/archive/ | Historical design doc (Jekyll era) | Historical reference |

---

## 🗺️ Visual Documentation Map

```
┌─────────────────────────────────────────────────────────────┐
│                    REPOSITORY ROOT                          │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼─────┐      ┌──────▼──────┐    ┌──────▼──────┐
   │ README   │      │  CLAUDE.md  │    │ARCHITECTURE │
   │   .md    │      │             │    │    .md      │
   └──────────┘      └──────┬──────┘    └──────┬──────┘

   GitHub          AI Assistant         Technical
   Homepage        Startup Guide        Reference

   [Users]         [AI Tools]          [Developers]

                        │
        ┌───────────────┴───────────────┐
        │                               │
   ┌────▼─────────┐              ┌──────▼──────┐
   │  docs/       │              │   plans/    │
   │  INDEX.md    │              │   (Separate)│
   │  (This file) │              └─────────────┘
   └────┬─────────┘
        │
        │  Documentation Hub
        │
        ├──→ AGENTS.md         [AI Protocols]
        ├──→ NVM_SETUP.md      [Setup Guide]
        └──→ archive/
             └─→ blueprint.md  [Historical]


┌─────────────────────────────────────────────────────────────┐
│                   CROSS-REFERENCE MAP                       │
└─────────────────────────────────────────────────────────────┘

   CLAUDE.md ──────────┬──────→ ARCHITECTURE.md
       │               │
       └───────────────┼──────→ docs/AGENTS.md
                       │
   ARCHITECTURE.md ────┼──────→ docs/AGENTS.md
       │               │
       └───────────────┴──────→ docs/NVM_SETUP.md

   docs/INDEX.md ──────────────→ All Documentation Files
```

---

## 📚 Documentation By Purpose

### For First-Time Visitors

**Start Here:** [README.md](../README.md)
- Project overview
- What this site does
- Key features
- Quick links

---

### For AI Assistants

**Startup:** [CLAUDE.md](../CLAUDE.md)
- Quick reference guide
- Essential commands
- Protocol awareness
- Architecture summaries

**Protocols:** [AGENTS.md](./AGENTS.md)
- Prompt improvement framework
- Development conventions
- Prompting guidelines
- Agent use cases

**Deep Dive:** [ARCHITECTURE.md](../ARCHITECTURE.md)
- Complete technical reference
- Data flow diagrams
- Component architecture
- Troubleshooting guides

---

### For Developers

**Quick Start:** [CLAUDE.md](../CLAUDE.md)
- Development commands
- Build configuration
- Common workflows

**Technical Reference:** [ARCHITECTURE.md](../ARCHITECTURE.md)
- Technology stack (Next.js 15, TypeScript 5, Tailwind CSS)
- Directory structure
- GitHub Actions workflows
- Python scripts documentation
- Dynamic route system
- Data management
- Configuration files
- Deployment process

**Setup:** [NVM_SETUP.md](./NVM_SETUP.md)
- Node version management
- Environment setup
- One-time configuration

---

## 🎯 Documentation By Task

### Adding Content

| Task | Primary Doc | Section |
|------|------------|---------|
| Add research page | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Common Tasks |
| Add publication | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Common Tasks |
| Add figure | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Common Tasks |
| Update bio/experience | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Common Tasks |

### Development

| Task | Primary Doc | Section |
|------|------------|---------|
| Local development | [CLAUDE.md](../CLAUDE.md) | § Quick Start Commands |
| Build for production | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Development Workflow |
| Deploy to GitHub Pages | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Deployment Process |
| Debug build issues | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Troubleshooting |

### Understanding Architecture

| Topic | Primary Doc | Section |
|-------|------------|---------|
| Dynamic route system | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Dynamic Route System |
| Data pipeline | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Data Flow Architecture |
| GitHub Actions | [ARCHITECTURE.md](../ARCHITECTURE.md) | § GitHub Actions Workflows |
| Component structure | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Component Architecture |
| Python scripts | [ARCHITECTURE.md](../ARCHITECTURE.md) | § Python Scripts |

### AI Development

| Topic | Primary Doc | Section |
|-------|------------|---------|
| Prompt improvement | [AGENTS.md](./AGENTS.md) | § Prompt Improvement Protocol |
| Development conventions | [AGENTS.md](./AGENTS.md) | § Development Conventions |
| Prompting best practices | [AGENTS.md](./AGENTS.md) | § Prompting Guidelines |
| Agent use cases | [AGENTS.md](./AGENTS.md) | § Agent Use Cases |

---

## 🔍 Finding Information

### By File Size

| Document | Lines | Depth | Use Case |
|----------|-------|-------|----------|
| CLAUDE.md | ~245 | Quick | AI startup, essential commands |
| AGENTS.md | ~148 | Moderate | AI protocols, prompting |
| README.md | ~120 | Quick | Project overview |
| NVM_SETUP.md | ~90 | Quick | One-time setup |
| ARCHITECTURE.md | ~2200 | Deep | Complete technical reference |

### By Update Frequency

| Document | Updates | Reason |
|----------|---------|--------|
| **README.md** | Rarely | Stable project overview |
| **CLAUDE.md** | Occasionally | As new patterns emerge |
| **ARCHITECTURE.md** | Regularly | As features are added |
| **AGENTS.md** | Occasionally | As AI protocols evolve |
| **NVM_SETUP.md** | Rarely | Stable setup process |

---

## 📖 Documentation Standards

### File Naming

- **Root docs:** `UPPERCASE.md` (README, CLAUDE, ARCHITECTURE, AGENTS)
- **Supplementary docs:** `Title_Case.md` (NVM_SETUP)
- **Historical docs:** `lowercase.md` in `archive/` (blueprint)

### Cross-Referencing

All documentation uses **relative markdown links**:
- Root to root: `[CLAUDE.md](./CLAUDE.md)`
- Root to docs/: `[AGENTS.md](./docs/AGENTS.md)`
- docs/ to root: `[README.md](../README.md)`
- docs/ to docs/: `[AGENTS.md](./AGENTS.md)`

### Link Format

Use this format for cross-references:
```markdown
📘 **See [FILENAME](./path) for [topic]**
📘 **See [FILENAME § Section](#section-anchor)** for details
```

---

## 🚀 Getting Started Paths

### Path 1: End User

```
README.md
    ↓
Visit deployed site
    ↓
Explore research pages
```

### Path 2: Developer

```
README.md
    ↓
CLAUDE.md (Quick start commands)
    ↓
NVM_SETUP.md (Environment setup)
    ↓
npm run dev (Start development)
    ↓
ARCHITECTURE.md (Deep dive as needed)
```

### Path 3: AI Assistant

```
CLAUDE.md (Startup + protocol awareness)
    ↓
AGENTS.md (Prompt improvement protocols)
    ↓
ARCHITECTURE.md (Technical details as needed)
    ↓
Work on tasks following protocols
```

### Path 4: Contributing

```
README.md (Project overview)
    ↓
ARCHITECTURE.md (Understand architecture)
    ↓
AGENTS.md (AI development standards)
    ↓
Make changes following conventions
    ↓
Submit pull request
```

---

## 📋 Document Maintenance

### Updating Documentation

When making changes:

1. **Update content** in the appropriate file
2. **Update cross-references** if file moves or sections change
3. **Update this INDEX.md** if adding/removing documents
4. **Update "Last Updated" date** in document headers
5. **Commit with descriptive message** explaining changes

### Adding New Documentation

New documentation should be placed:

- **Root:** Only essential docs (README, CLAUDE, ARCHITECTURE)
- **docs/:** Supplementary guides, protocols, setup docs
- **docs/archive/:** Historical documents no longer actively used
- **plans/:** Planning documents, implementation plans

---

## 🔗 External Resources

### Next.js Documentation
- **Official Docs:** https://nextjs.org/docs
- **App Router:** https://nextjs.org/docs/app
- **Static Export:** https://nextjs.org/docs/app/building-your-application/deploying/static-exports

### GitHub Pages
- **Documentation:** https://docs.github.com/en/pages
- **Custom Domains:** https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

### NASA ADS / SciX API
- **API Documentation:** https://scixplorer.org/help/api/
- **Search Query Syntax:** https://scixplorer.org/help/search/

---

## 📞 Help & Support

### Documentation Issues

If you find issues with documentation:

1. **Check related docs** - Information might be in a different file
2. **Search for keywords** - Use GitHub's search or grep
3. **Check changelog** - See ARCHITECTURE.md § Changelog for recent changes
4. **Open an issue** - Report documentation gaps or errors on GitHub

### Common Questions

**Q: Which doc should I read first?**
A: Start with README.md for overview, then CLAUDE.md for quick reference, then ARCHITECTURE.md for deep dives.

**Q: Where do I find information about adding content?**
A: ARCHITECTURE.md § Common Tasks has step-by-step guides for all content additions.

**Q: How do I set up my development environment?**
A: Follow NVM_SETUP.md for Node setup, then use commands from CLAUDE.md § Quick Start Commands.

**Q: Where are AI development guidelines?**
A: AGENTS.md contains all AI protocols, prompting guidelines, and development conventions.

**Q: How do I troubleshoot build errors?**
A: ARCHITECTURE.md § Troubleshooting has a comprehensive troubleshooting guide.

---

## 🗂️ Archive

Historical documents preserved for reference:

- **[blueprint.md](./archive/blueprint.md)** - Original Jekyll-era design document (pre-2024)

These files are kept for historical context but do not reflect the current architecture.

---

**Last Updated:** 2025-12-29

**Maintained By:** B. L. Alterman

**For questions or contributions, please open an issue on GitHub.**
