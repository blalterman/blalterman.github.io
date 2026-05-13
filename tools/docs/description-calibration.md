# Description Calibration Spec

**Authoritative voice and grounding guide for unified per-page descriptions across the site.**

This document calibrates the single `description` parameter that `src/lib/metadata.ts` passes to Next.js Metadata API for every page. It is the load-bearing reference for both manual authoring and parallel agent fan-out.

## Scope

Every page on the site emits three description-shaped meta tags:

- `<meta name="description">` — search engines (Google SERP snippets)
- `<meta property="og:description">` — Open Graph consumers (LinkedIn, Slack, Discord, iMessage, Facebook)
- `<meta name="twitter:description">` — Twitter/X cards

The metadata helper accepts a single `description` parameter and emits the same string to all three meta tags. This unified-image approach is supported by empirical evidence (see § Empirical Background) and reduces the editorial maintenance burden from 3N strings to N strings without measurable loss of channel-render quality.

## Empirical Background

Sampled 16 professional sites on 2026-05-09 for channel-tuning practice:

- Institutional: NASA Sun, NASA Parker Solar Probe, IOPscience (ApJ paper landing), NASA ADS
- Science communicators: Bill Nye, Phil Plait (Bad Astronomy newsletter), Sabine Hossenfelder, Katie Mack
- Public intellectuals: Stephen Wolfram, Tyler Cowen (Marginal Revolution), Maria Popova (The Marginalian), Steven Pinker, Sam Harris
- Boutique editorial: Nautilus

Across the 12 sites that exposed usable meta tags, **100% use single-source descriptions** — the same string across `meta`, `og`, and `twitter`. Channel-tuning is not observed practice even at Stephen Wolfram (notoriously careful about presentation) or Nautilus (boutique editorial that competes for clicks without institutional gravity).

This site follows the universal pattern: one carefully-authored description per page, replicated across all three meta tags.

## Voice per Page Type

Each page type has a voice established in existing site copy. Lift from there; do not invent.

### Homepage and static pages (`/`, `/research`, `/publications`, `/experience`)

- Voice: third-person factual, declarative, with specifics (NASA Goddard, helium abundance, etc.)
- Length: 100–200 chars typical
- Existing reference: layout.tsx homepage description (145 chars): "Research astrophysicist studying solar wind physics, heliophysics, and space weather. Explore publications, projects, and academic collaborations."

### Ben overview (`/ben`)

- Title invariant (DECIDED): og:title is exactly `B. L. Alterman` — bare, no suffix. Warm welcoming title preserved across canonical/og:title/twitter:title.
- Description voice: short invitation, first-person or third-person warm
- Length: 60–100 chars
- Existing reference (67 chars): "Learn about Ben's research vision and team-building philosophy."

### Ben subpages (`/ben/[slug]`)

- Voice: first-person narrative, philosophical; central conviction in one sentence
- Length: 130–220 chars
- Existing reference: section.excerpt fields in ben-page.json (147 chars typical)
- Paper-writer skill applicability: NONE. Voice mismatch with scientific-prose propositions.

### Research topic pages (`/research/[slug]`)

- Voice: third-person science prose; lead with the phenomenon or finding; concrete numbers when available
- Length: 200–400 chars
- Existing reference: topic.description fields in research-topics/*.json
- Paper-writer skill applicability: FULL — invoke per § Paper-writer Integration

### Figure detail pages (`/research/figure/[paper_id]/[figure_id]`)

- Voice: declarative finding, technical, single-sentence punch
- Length: 150–250 chars
- Existing reference: entry.summary_short fields in figure-registry.json
- Paper-writer skill applicability: FULL

### Publications category pages (`/publications/[category]`)

- Voice: short taxonomic label or brief framing
- Length: 20–80 chars typical; up to ~150 chars when describing aggregated content
- Existing reference: category.description fields
- Paper-writer skill applicability: PARTIAL — only hedging calibration

## Length Guidance

**No character limit per Google Search Central** (verified 2026-04-20): "There's no limit on how long a meta description can be, but the snippet is truncated in Google Search results as needed, typically to fit the device width."

Open Graph protocol (ogp.me) does NOT specify a length. Twitter Cards documentation specifies no hard limit either.

**Empirical range across the 16-site sample:** 35–305 chars. No clustering at any folklore number. Per-page-type ranges in this spec are descriptive (where existing site copy falls), not prescriptive.

Write what fits the content. Do NOT pad or trim to hit a target.

## Claim Grounding

All claims in descriptions must be supported by the published corpus — the topic JSON, figure-registry summaries, paper abstracts (under `research-corpus/papers/<paper_id>/paper.md`), and the research papers themselves. The user's clearer phrasings of corpus-supported claims are allowed and encouraged; agents are not required to mirror the corpus's exact wording.

Two distinct lines agents must hold:

1. **Phrasing freedom** — When the user has worded a corpus-supported claim more clearly than the corpus does, prefer the user's wording. The A_He / σ_c diagnostic-split framing is an example: the framing is supported by Alterman & D'Amicis 2025 (ApJL 982 L40), Alterman & D'Amicis 2026 (ApJL 996 L12), Alterman 2025 (ApJL), and Alterman et al. 2025a (A&A) even though those papers do not word it as a "diagnostic split."

2. **Claim discipline** — Agents must NOT make claims the corpus doesn't support. If a description would benefit from a claim beyond the corpus, the agent must flag it in `voice_grounding_source` rather than ship.

When in doubt: read the relevant paper abstracts in `research-corpus/papers/<paper_id>/paper.md` and the figure-registry summaries. If a claim cannot be traced to those, it cannot ship.

## Worked Example 1 — Research Topic: helium-abundance

Source data:
- `topic.title`: "Helium Abundance"
- `topic.subtitle`: "Tracing solar wind origins through composition"
- Paper abstracts: Alterman & D'Amicis 2025 (ApJL 982 L40), Alterman & D'Amicis 2026 (ApJL 996 L12) under `research-corpus/papers/`

**Unified description (270 chars) — APPROVED 2026-05-13:**

> Helium saturates near 4.19% above 433 km/s. Set in the chromosphere, helium fingerprints the source region. Set at the Sun-heliosphere interface, the cross helicity fingerprints the coupling process where the solar wind is born from coronal plasma.

**Annotations:**

- Three-sentence structure: observation, helium's role, cross helicity's role
- Parallel "Set in/at X, fingerprints Y" for both diagnostics — diagnostic-split framing in compressed form
- Corpus-grounded: 4.19% / 433 km/s observation (Paper I, fig 3); chromospheric origin and Sun-heliosphere interface heights (Paper I, fig 2); "coupling process" framing supported by but reworded from Papers I + II
- No AI tics; no rhetorical opener; concrete numbers lead

## Worked Example 2 — Ben Subpage: research-vision

Source data:
- `section.title`: "Research Vision"
- `section.excerpt` (147 chars): "The question of what it means to be on this planet, orbiting our Sun, drives everything I do—my research, my teams, and the systems I build."
- `section.paragraphs[0]`: long first-person narrative

**Unified description (200 chars) — APPROVED 2026-05-13:**

> What does it mean to be on this planet, orbiting our Sun? Answering this question drives my research on the solar wind, the teams I build, and the systems I orchestrate to make breakthroughs inevitable.

**Annotations:**

- Question-answer structure: page's central conviction IS a question, so leading with the question is leading with the content
- First-person throughout — voice-consistency rule for ben pages overrides the general "no rhetorical opener" rule
- Concrete verbs: drives, build, orchestrate (no generic "shape", "guide")
- Closes with verbatim user concept from `paragraphs[0]`: "make breakthrough insights inevitable rather than accidental" compressed to "make breakthroughs inevitable"
- Voice grounding: section.excerpt + paragraphs[0]; user-confirmed phrasings

## Paper-writer Integration

`/paper-writer:propositions-sentence` provides 6 propositions calibrated for scientific paper sentences. Three transfer to description-length copy:

| Proposition | Applies? | Why |
|---|---|---|
| Science-forward citations (≥80%) | NO | Descriptions don't cite |
| Progressive explanation | YES | Descriptions should advance reader understanding |
| Justification patterns | NO | No room at this length |
| Hedging calibration | YES | Catches AI hedge tics |
| Sentence length (24–35 words) | NO | Descriptions often ~25 words entire |
| Quantitative emphasis | YES (where applicable) | Concrete numbers lead in science-prose pages |

### Per-page-type application

- **Ben subpages**: do NOT invoke. Voice mismatch.
- **Static pages and Ben overview**: invoke only for hedging calibration.
- **Research topic pages**: invoke fully (3 transferable propositions).
- **Figure detail pages**: invoke fully (3 transferable propositions).
- **Publications category pages**: invoke only for hedging calibration (other propositions don't fit taxonomic labels).

Agents should treat paper-writer output as advisory. If a flagged proposition cannot be addressed without distorting content at description length, agents document the override in `voice_grounding_source` and ship.

## Anti-Patterns

### AI hedging tics — FORBIDDEN

- "Additionally", "Furthermore", "Moreover", "It's worth noting"
- "delve into", "navigate the landscape", "in today's world", "robust", "leverages"
- "could potentially", "may help to", "tends to"
- "fascinating", "exciting", "remarkable" (generic enthusiasm without specifics)
- "explores", "discusses", "examines" as the primary verb without naming what specifically

### Word weight — every word must do work

Description character budgets are unforgiving. Generic verbs, filler connectors, and rhetorical scaffolding waste characters that could carry information. Cut on sight:

- **Generic verbs**: "tells you", "answers", "reveals", "diagnoses" when used as the main verb without semantic load. Replace with concrete verbs that name the action ("fingerprints", "regulates", "shifts", "saturates").
- **Rhetorical openers in factual contexts**: "How can you tell...", "Did you know..." burn 30+ chars on setup. Lead with the claim. Exception: ben subpages where the page's central conviction is itself a question.
- **Em-dash explanatory inserts that hedge**: "— a powerful diagnostic for —" is filler around an unspecified noun.
- **Redundant context**: if the topic title carries the context (e.g., "Helium Abundance" page), do not repeat "solar wind helium" — say "helium."
- **Hedge adjectives**: "powerful", "key", "novel", "important", "fascinating" — generic enthusiasm without specifics.

Audit test: read each word and ask "what does this contribute?" If the answer is "nothing," cut it.

### Voice violations

- Do NOT shift ben subpage descriptions to third-person. Voice consistency rule.
- Do NOT strip first-person voice from ben pages when condensing.

### Length violations

- Do NOT pad to hit a folklore length target (155 chars, 200 chars, etc.).
- Do NOT trim a description below the natural length of its content.

## Batch Design — Paper-Coherent Assignments

Figure descriptions are partitioned by paper into 6 thematically-coherent batches. Other categories are single agents:

| Batch | Pages | Theme | Subagent type |
|---|---|---|---|
| Ben | 7 (overview + 6 subpages) | Ben pages (single source file: `public/data/ben-page.json`) | `ben-page-writer` |
| Research_Topics | 12 | Research topic pages (`public/data/research-topics/*.json`) | `general-purpose` |
| Publications_Categories | 7 | Publications categories (`public/data/publications-categories.json`) | `general-purpose` |
| F1 | 30 | Compressibility regulator (Alterman_2026_ApJL_996_L12) | `general-purpose` |
| F2 | 21 | Saturation framework (Alterman_2025_ApJL_982_L40) + heavy-ion application (aa51550-24) | `general-purpose` |
| F3 | 15 | Solar cycle composition: Alterman_2019_ApJL_879_L6 + s11207-021-01801-9 + aa54299-25 | `general-purpose` |
| F4 | 15 | Suprathermal heavy ions: Alterman_2023_ApJ_952_42 + Alterman_2024_ApJL_964_L31 | `general-purpose` |
| F5 | 9 | Proton beams / differential flow: Alterman_2018_ApJ_864_112 | `general-purpose` |
| F6 | 4 | Solar wind acceleration via Alfvén wave forcing: Alterman_2025_ApJL_984_L64 | `general-purpose` |

**Total: 9 parallel agents, 120 newly-authored strings.**

Static pages (homepage + 4 page-level metadata exports) are authored inline by the parent session with the user in the loop. Not delegated.

## Tmp-File Handoff Protocol

Agents do NOT modify source JSON files directly. They write structured tmp files that a separate review session applies to source files.

### Tmp file location

`tools/tmp/seo-descriptions/` (relative to project root, on branch `feat/seo-descriptions`).

| Filename | Batch |
|---|---|
| `ben.json` | Ben pages |
| `research-topics.json` | Research topic pages |
| `publications-categories.json` | Publications categories |
| `figures-F1.json` | Compressibility regulator (Alterman_2026_ApJL_996_L12) |
| `figures-F2.json` | Saturation framework + heavy-ion application |
| `figures-F3.json` | Solar cycle composition cluster |
| `figures-F4.json` | Suprathermal heavy ions |
| `figures-F5.json` | Proton beams / differential flow |
| `figures-F6.json` | Solar wind acceleration |

### Tmp file structure

```json
{
  "batch": "F1",
  "label": "Compressibility regulator (Alterman_2026_ApJL_996_L12)",
  "papers": ["Alterman_2026_ApJL_996_L12"],
  "authored_at": "2026-05-13T...",
  "calibration_spec": "tools/docs/description-calibration.md",
  "patches": [
    {
      "target_file": "public/data/figure-registry.json",
      "target_key": "Alterman_2026_ApJL_996_L12/fig_1",
      "description": "...",
      "voice_grounding_source": "summary_short field; paper abstract sentence 1-2; calibration spec figure-detail voice"
    }
  ]
}
```

### Apply protocol (review session)

For each batch:
1. Read the tmp file
2. Sample 3-5 descriptions for voice/anti-pattern compliance
3. If acceptable: apply each `patches[i].description` to `patches[i].target_file` at `patches[i].target_key`
4. Add a description field at that key in the source JSON
5. Remove the tmp file
6. Commit with subject `feat(seo): apply unified descriptions for <category>`
7. Repeat for next batch

## Authoring Workflow (for agents)

Each agent receives:

1. The path to this calibration spec (read at start)
2. The tmp file path for its batch
3. Its category's source data paths
4. Paper abstract path(s) under `research-corpus/papers/<paper_id>/paper.md`
5. The list of pages it owns

Per-agent steps:

1. Read this calibration spec fully — voice rules, anti-patterns, worked examples
2. Read source data for each page in the batch
3. Read paper abstract(s) for science grounding (figure batches)
4. Draft one unified description per page
5. For science-prose batches: optionally invoke `/paper-writer:propositions-sentence` on a draft and revise per transferable propositions only (progressive explanation, hedging calibration, quantitative emphasis)
6. Write the structured JSON patch to the tmp file path
7. Return a brief status message ONLY:

```json
{
  "status": "complete",
  "batch": "<batch_label>",
  "tmp_file": "<full path>",
  "page_count": <N>,
  "first_description_sample": "<first 100 chars of any one description>"
}
```

**CRITICAL: agents must NOT include description content in their final message beyond the 100-char sample. Descriptions live only in the tmp file. Parent session does not ingest the patches.**

## Revision History

- 2026-05-13: Initial authoring (channel-tuned worked examples).
- 2026-05-13: Worked Example 1 approved (channel-tuned variant). Added Claim Grounding section and Word-weight anti-pattern.
- 2026-05-13: Rewritten for Option A unified-description approach after empirical-evidence re-evaluation. Worked Examples 1 and 2 collapsed to single unified strings. Channel × Page-Type Matrix and Voice per Channel sections removed (no longer needed). Added Batch Design and Tmp-File Handoff Protocol sections. Authoring Workflow updated for tmp file pattern.
- Pending: agent fan-out + per-batch review + apply commits + verification + merge to main.
