# AGENTS.md

## Purpose

This file documents how AI development assistants (e.g., GitHub Copilot, OpenAI Codex, ChatGPT) are used in building and maintaining this personal research website. These agents support the human developer by accelerating repetitive tasks, suggesting design patterns, and assisting with content generation—while all major decisions and final edits remain human-reviewed.
The website is built using the Jekyll framework.

---

## Agent Use Cases

The following tasks are commonly supported by AI agents:

### 🧱 Layout & Design

- Generate semantic, accessible HTML5 structure
- Propose clean, responsive CSS for layout and typography
- Assist in creating new pages or sections (e.g., publications, teaching, blog)

### ✍️ Content Writing

- Draft academic bios, section intros, or project descriptions
- Summarize papers for the publications section
- Generate placeholder or boilerplate text

### 🧑‍💻 Code Generation

- Write or refactor HTML, CSS, or JS components
- Convert content into Markdown or JSON if needed
- Provide templates or skeletons for site features

### 🧪 QA & Review

- Check semantic structure (e.g., heading hierarchy)
- Suggest accessibility or usability improvements
- Review for broken links or structural inconsistencies

---

## Prompting Guidelines

To ensure useful and reproducible outputs:

- **Be specific**: Include exact elements (e.g., "create a 2-column layout using Flexbox").
- **State intent**: Clarify the user goal (e.g., “make the header mobile-friendly”).
- **Use incremental prompts**: Ask for small, verifiable changes instead of sweeping rewrites.

Example prompt:

> “Add a ‘Contact’ section at the bottom of `index.html`. Include name, email, and institution in a simple 2-column layout using Flexbox.”

---

## Development Conventions

When working with agents on this project:

1. **All AI-generated code is subject to human review and edit.**
2. **Do not disable HTML validation, accessibility, or linter rules unless justified.**
3. **Use semantic HTML whenever possible (e.g., `<section>`, `<article>`, `<nav>`, `<footer>`).**
4. **Favor maintainable, minimal CSS over heavy frameworks unless necessary.**
5. **Document all AI-assisted commits with a message prefix:**
