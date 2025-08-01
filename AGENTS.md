# AGENTS.md

## Purpose

This file documents how AI development assistants (e.g., GitHub Copilot, OpenAI Codex, ChatGPT) are used in building and maintaining this personal research website. These agents support the human developer by accelerating repetitive tasks, suggesting design patterns, and assisting with content generation—while all major decisions and final edits remain human-reviewed.
The website is built using the Next.js framework.

---

## Agent Use Cases

The following tasks are commonly supported by AI agents in this Next.js project:

### 🧱 Layout & Design

- Generate semantic, accessible HTML structure within React components
- Propose clean, responsive CSS or Tailwind CSS classes for layout and typography
- Assist in creating new pages or sections using Next.js page routing

### ✍️ Content Writing

- Draft academic bios, section intros, or project descriptions
- Summarize papers for the publications section
- Generate placeholder or boilerplate text

### 🧑‍💻 Code Generation

- Write or refactor React components, TypeScript code, or API routes
- Convert content into JSON or other data formats if needed
- Provide templates or skeletons for site features
- Assist with implementing data fetching strategies (e.g., static generation, server-side rendering)

### 🧪 QA & Review

- Check semantic structure and accessibility within React components
- Suggest accessibility or usability improvements
- Review for broken links or structural inconsistencies
- Help with debugging Next.js-specific issues

---

## Prompting Guidelines

To ensure useful and reproducible outputs:

- **Be specific**: Include exact elements and desired outcomes (e.g., "create a responsive header component using React and Tailwind CSS").
- **State intent**: Clarify the user goal (e.g., “implement static generation for the publications page”).
- **Use incremental prompts**: Ask for small, verifiable changes instead of sweeping rewrites.
- **Provide context**: Include relevant code snippets or file structures when asking for modifications.

Example prompt:

> “Create a new page at `/about` using Next.js App Router. Include a section for a short bio and a profile picture.”

---

## Development Conventions

When working with agents on this project:

1. **All AI-generated code is subject to human review and edit.**
2. **Do not disable linting or type-checking rules unless justified.**
3. **Use semantic HTML within React components whenever possible (e.g., `<section>`, `<article>`, `<nav>`, `<footer>`).**
4. **Favor maintainable, modular React components and well-organized CSS or Tailwind classes.**
5. **Document all AI-assisted commits with a message prefix (e.g., `AI:` or `Co-authored-by:`).**
6. **Adhere to Next.js conventions for file-based routing, data fetching, and API routes.**
