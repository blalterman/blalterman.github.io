# AGENTS.md

## Purpose

This file documents how AI development assistants (e.g., GitHub Copilot, OpenAI Codex, ChatGPT) are used in building and maintaining this personal research website. These agents support the human developer by accelerating repetitive tasks, suggesting design patterns, and assisting with content generation—while all major decisions and final edits remain human-reviewed.
The website is built using the Next.js framework.

---
## Prompt Improvement Protocol

### When to Analyze Prompts
Provide proactive improvement suggestions for **moderate and complex tasks**:

**Moderate Complexity (2-4 steps):**
- Multi-step workflows with some ambiguity
- Tasks requiring sequential tool use
- Requests that could benefit from more specificity

**Complex Complexity (strategic/multi-domain):**
- Planning, implementation, or architectural tasks
- Multi-phase or multi-module work
- Ambiguous scope requiring interpretation
- Tasks needing agent coordination
- Physics/scientific validation requirements
- Debugging requiring root cause analysis

**Exclude simple tasks:**
- Single file reads or documentation lookups
- Direct git/bash commands (status, log, etc.)
- Single glob/grep operations
- Clear, specific, single-step requests

### Improvement Focus Areas
Analyze prompts for opportunities in all areas:

1. **Clarity & Specificity**
   - Remove ambiguities and undefined scope
   - Add missing requirements or success criteria
   - Specify integration points and module targets

2. **Context & Constraints**
   - Add relevant domain context
   - Specify constraints (backward compatibility, performance)
   - Include data format expectations

3. **SolarWindPy Integration**
   - Suggest appropriate agent selection
   - Reference hooks, workflows, and automation

4. **Efficiency Optimization**
   - Suggest parallel operations where applicable
   - Recommend context-saving approaches
   - Identify opportunities for batch operations

### Improvement Presentation Format
Use structured format for suggestions:

```
📝 Prompt Improvement Suggestion

Original Intent: [Confirm understanding of request]

Suggested Improvements:
- [Specific addition/clarification 1]
- [Specific addition/clarification 2]
- [Agent or workflow suggestion]
- [Missing constraint or context]

Enhanced Prompt Example:
"[Concrete example of improved version]"

Expected Benefits:
- [How improvement enhances execution quality]
- [Reduced ambiguity or better agent selection]
- [Efficiency or context preservation gains]

Proceed with:
[A] Original prompt as-is
[B] Enhanced version
[C] Custom modification (please specify)
```

### Integration with Workflow
- Prompt analysis occurs **before** task execution
- Works naturally with plan mode workflow
- User approves original or enhanced version before proceeding
- Builds better prompting patterns over time

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
