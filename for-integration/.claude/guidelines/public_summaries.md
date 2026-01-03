# Figure Summaries for Scientifically Literate Public Audiences

## Purpose

This document provides guidelines for writing figure summaries targeting **scientifically literate public** audiences—readers of Science News or Scientific American. These readers have college-level STEM education or science journalism backgrounds, but lack domain expertise in heliophysics.

**Target audience:**
- Science journalists with technical training
- Scientists from adjacent fields (astrophysics, plasma physics, atmospheric science)
- Grant reviewers outside the immediate specialty
- Educated public with active STEM interest

**NOT for:**
- General public (high school level)—too technical
- Domain specialists (Physics Today, AGU journals)—too simplified

**Use cases:** Science journalism pitches, grant broader impacts sections, conference summaries for interdisciplinary audiences, outreach materials for science-engaged public.

### Summary Structure

Each figure summary follows a three-paragraph structure:

1. **what_we_see:** Describe what the figure visually presents (axes, colors, panels, data)
2. **the_finding:** Explain what patterns or results emerge from the visualization
3. **why_it_matters:** Connect findings to broader scientific significance

**Length targets:** Total 500-700 words (target 600), with each section contributing roughly equal weight.

---

## The 7 Guidelines

### Guideline 1: Fractal Depth Ceiling

**Rule:** Limit nesting depth based on section type.

- **Descriptive sections (what_we_see):** Maximum 2 nesting levels
- **Analytical sections (the_finding, why_it_matters):** Maximum 3 nesting levels

**Test:** Apply the Golden Rule—does each nesting level add NEW information, or just rephrase? If removing a level loses information, keep it. If it only loses pattern, remove it.

**BEFORE (3 levels in descriptive section):**
> "This four-panel figure shows measurements from the Wind spacecraft's Faraday cup instrument (which detects charged particles by measuring current induced as particles pass through a series of grids—essentially a sophisticated particle counter) viewing the solar wind from four different angles."

**AFTER (2 levels):**
> "This four-panel figure shows solar wind measurements from Wind spacecraft. A Faraday cup instrument captures particles arriving at four different angles relative to the magnetic field."

---

### Guideline 2: Sentence Length Cap

**Rule:** Keep sentences within cognitive load limits.

- **Target:** 25-40 words per sentence
- **Hard limit:** 60 words maximum
- **Check:** If a sentence exceeds 60 words, split at em-dash, colon, or natural clause boundary

**BEFORE (72 words):**
> "The horizontal axis shows energy-per-charge in kilovolts, ranging from zero to four, while the vertical axis displays charge flux in picoamperes on a logarithmic scale—this logarithmic presentation being necessary because particle fluxes span several orders of magnitude, from background noise levels near one picoampere to peak signal strengths exceeding one thousand picoamperes at the main peaks."

**AFTER (two sentences, 32 and 28 words):**
> "The horizontal axis shows energy-per-charge (0-4 kilovolts); the vertical axis displays charge flux on a logarithmic scale. This logarithmic presentation captures particle fluxes spanning several orders of magnitude, from background noise to peak signals."

---

### Guideline 3: Parenthetical Budget

**Rule:** Maximum one parenthetical or aside per sentence.

**Exception:** Parallel quantitative values count as ONE use. For example: "slow wind (355 km/s) and fast wind (622 km/s)" is acceptable because the parentheticals serve identical grammatical functions.

**Rationale:** Readers lose the main thread after the first interruption. Multiple asides force working memory to track multiple suspended contexts.

**BEFORE (3 parentheticals):**
> "The correlation (measured using Spearman's rank method—preferred over Pearson's because it captures monotonic relationships even when non-linear) between helium abundance (A_He, the ratio of helium to hydrogen by number) and solar wind speed shows distinct regimes."

**AFTER (1 parenthetical):**
> "The correlation between helium abundance and solar wind speed shows distinct regimes. This analysis uses Spearman's rank method (which captures monotonic relationships even when non-linear) rather than standard linear correlation."

---

### Guideline 4: The "Skim Test"

**Rule:** Every sentence must convey its core meaning when parenthetical content is skipped.

**Procedure:**
1. Read the sentence mentally deleting ALL content in parentheses, em-dashes, or subordinate clauses
2. Does the remaining "skeleton" sentence make sense on its own?
3. **Pass:** Skeleton conveys main point
4. **Fail:** Critical information buried in nested content

**PASSES:**
> "The plot shows solar wind speed peaks around 355 km/s (slow wind) and 622 km/s (fast wind), revealing the bimodal nature of the solar wind."

Skeleton: "The plot shows solar wind speed peaks around 355 km/s and 622 km/s, revealing the bimodal nature of the solar wind." Core meaning intact.

**FAILS:**
> "The plot is divided into vertical columns by speed, with each column's color intensity normalized to its own maximum—meaning bright yellow indicates most common helium value for that speed."

Skeleton: "The plot is divided into vertical columns by speed, with each column's color intensity normalized to its own maximum." Reader cannot understand WHY normalization matters without the em-dash content.

**Fix:** Promote critical information: "Each column's color intensity is normalized to its own maximum. Bright yellow therefore indicates the most common helium value for that particular speed—not the global maximum across all speeds."

---

### Guideline 5: Fractal vs. Enumeration

**Rule:** Apply fractal structure for comparisons; avoid it for enumerations.

**Use fractal for:**
- Contrasts (slow vs. fast wind, below vs. above threshold)
- Cause-effect chains
- Analytical progressions (observation → interpretation → implication)

**Avoid fractal for:**
- Figure element lists (axes, panels, colors)
- Technical specifications (instruments, units, scales)
- Sequential descriptions (first panel, second panel, third panel)

**Why:** Lists don't benefit from nested self-similar structure. Fractal organization works when each level DEVELOPS an idea; enumeration simply INVENTORIES elements.

**BEFORE (fractal applied to enumeration):**
> "The figure presents four panels, each containing distinct information—the first showing raw measurements (with protons appearing as the dominant peak at roughly one kilovolt), while the second reveals alpha particles (identifiable by their characteristic double-charge signature at approximately two kilovolts), and the third..."

**AFTER (simple enumeration):**
> "The figure presents four panels. The first shows raw measurements with a dominant proton peak near 1 kV. The second reveals alpha particles at approximately 2 kV. The third and fourth panels display processed data after background subtraction."

---

### Guideline 6: Front-Load Verdicts

**Rule:** State the main finding in the first 10 words of why_it_matters.

**Good pattern:** "This proves X. [Details and implications follow.]"

**Anti-pattern:** "By analyzing Y through Z, considering A and B, we conclude X."

**Rationale:** Readers of Science News expect conclusions first, supporting details second. Burying the verdict forces readers to hold the entire analysis in memory before learning why they should care.

**BEFORE (verdict at position 42):**
> "By examining the correlation between helium abundance and solar wind speed, accounting for measurement time delays, and considering instrument uncertainties, this figure demonstrates that helium abundance tracks solar activity over the eleven-year cycle."

**AFTER (verdict at position 1):**
> "Helium abundance tracks solar activity. This figure demonstrates the correlation survives rigorous tests: accounting for measurement delays, correcting for instrument uncertainties, and comparing multiple solar cycles."

---

### Guideline 7: Paragraph Length Limits

**Rule:** Keep paragraphs digestible.

| Section | Word limit | Notes |
|---------|------------|-------|
| what_we_see | 150-200 words | Single paragraph acceptable |
| the_finding | 200-250 words | Break if exceeds 250 |
| why_it_matters | 200-250 words | Break if exceeds 250 |
| **Total** | **500-700 words** | **Target 600** |

**Rationale:** Online readers scan. Dense paragraphs exceeding 250 words signal "skip this"—exactly the opposite of what outreach material should communicate.

---

## Evaluation Checklist

Copy this checklist when reviewing figure summaries:

```markdown
## Figure Summary Checklist (Scientifically Literate Public)

Before finalizing any figure summary, verify:

□ No sentence exceeds 60 words
□ Fractal depth ≤2 (what_we_see) or ≤3 (the_finding/why_it_matters)
□ Max 1 parenthetical per sentence (exceptions noted)
□ All sentences pass "Skim Test" (skeleton = core meaning)
□ Fractal used for comparisons, NOT enumerations
□ "Why_it_matters" verdict in first 10 words
□ No single paragraph >250 words
□ Total summary: 500-700 words (target 600)
□ Reading level: Science News / Scientific American
```

---

## Common Pitfalls and Fixes

### Pitfall 1: Enumeration Bloat

**Problem:** Listing many elements in nested parentheticals mid-sentence.

**Example pattern:** Describing "four angles (118 deg, 139 deg, 156 deg, 170 deg)" followed by peaks, colors, and species—all nested within a single sentence structure.

**Fix:** Separate figure mechanics into their own sentences or use a brief list. Technical specifications (angles, units, scales) don't need fractal development.

---

### Pitfall 2: Meta-Level Abstractions

**Problem:** Discussing methodology trade-offs using nested structure.

**Example pattern:** "The most physically complete formula isn't always the most useful one... because dynamic pressure creates a chicken-and-egg problem AND higher moments have larger error bars."

**Fix:** State the conclusion first, explain the trade-off second in a separate sentence. "We use the simpler formula despite its approximations. The complete formula introduces circular dependencies and amplifies measurement uncertainties."

---

### Pitfall 3: Accumulating Qualifications

**Problem:** Main point followed by caveat, then speculation, then alternative interpretation—all in one sentence.

**Example pattern:** "Visual proof... not artifact BUT physical process... timing dominant BUT other factors—perhaps variations OR uncertainties."

**Fix:** One idea per sentence. Separate caveats into their own statement. "This provides visual proof of the physical process. Alternative explanations—instrumental artifacts or timing effects—were tested and ruled out."

---

### Pitfall 4: Long-Distance Dependencies

**Problem:** Sentences exceeding 70 words with subject and verb separated by multiple nested clauses.

**Example pattern:** 85-word sentences with 5 nesting levels, including parentheticals within em-dash elaborations.

**Fix:** Split at natural boundaries (em-dashes, colons). Each resulting sentence should maintain parallel structure with its siblings.

---

## The Updated Golden Rule

**Original Golden Rule** (from synthesis/fractal_calibration.md):
> "Fractal adds NEW information at each level (not just rephrasing)."

**Updated for Public Writing:**
> "Fractal should add NEW information at each level (not just rephrasing) AND stay within cognitive load limits (2-3 levels maximum, 60 words/sentence maximum, 1 parenthetical/sentence maximum)."

**Why the update:** Analysis shows that 95% of current summaries pass the original Golden Rule—each nesting level genuinely adds new information. Yet these summaries still hinder accessibility. The issue is cumulative cognitive load: individually justified nested structures compound to exceed working memory capacity. The update adds explicit cognitive load constraints.

---

## Before/After Gallery

### Example 1: Enumeration Bloat to Separated Sentences

**BEFORE:**
> "This four-panel figure shows measurements from the Wind spacecraft's Faraday cup instrument viewing the solar wind from four different angles relative to the magnetic field—118 deg, 139 deg, 156 deg, and 170 deg. Each panel plots charge flux (vertical axis, in picoamperes on a logarithmic scale) versus energy-per-charge (horizontal axis, 0-4 kilovolts), revealing three distinct particle populations through their characteristic peaks."

Issues: 4+ nesting levels, 12+ concepts compressed before the reader finishes two sentences.

**AFTER:**
> "This four-panel figure shows solar wind measurements from the Wind spacecraft. The Faraday cup instrument captures particles arriving at four angles (118 deg, 139 deg, 156 deg, and 170 deg). Each panel plots charge flux versus energy-per-charge. Three distinct particle populations appear as separate peaks."

Improvements: Reduced to 2 nesting levels, technical details (scales, units) simplified, one idea per sentence.

---

### Example 2: Long Sentence Split at Em-Dash

**BEFORE:**
> "The visualization reveals that helium abundance—expressed as the ratio of doubly-ionized helium to protons in the solar wind, a quantity that reflects coronal conditions at the Sun rather than in-situ processes during transit—varies systematically with solar wind speed, exhibiting higher values in fast wind streams (which originate from coronal holes) compared to slow wind (which emerges from the streamer belt and active region boundaries)."

Issues: 85 words, 5 nesting levels, buried main point.

**AFTER:**
> "The visualization reveals that helium abundance varies systematically with solar wind speed. Helium abundance—the ratio of doubly-ionized helium to protons—reflects conditions in the Sun's corona rather than changes during transit to Earth. Fast wind from coronal holes shows higher helium abundance than slow wind from the streamer belt."

Improvements: Three sentences averaging 30 words each, parallel structure, verdict front-loaded.

---

### Example 3: Buried Verdict to Front-Loaded

**BEFORE:**
> "By examining the correlation between X and Y, accounting for time delays introduced by solar wind transit times, considering measurement uncertainties from both instruments, and comparing results across three complete solar cycles spanning 33 years, this figure demonstrates that helium abundance in the solar wind tracks solar activity with remarkable fidelity."

Issues: 52 words before the verdict, methodology front-loaded over conclusion.

**AFTER:**
> "Helium abundance tracks solar activity with remarkable fidelity. This figure demonstrates the correlation holds across 33 years and three complete solar cycles, surviving rigorous tests for time delays and measurement uncertainties."

Improvements: Verdict in first 5 words, supporting details follow naturally.

---

## Cross-References

- **Fractal calibration principles:** See `synthesis/fractal_calibration.md` for the original Golden Rule and context-aware fractal guidance
- **Sentence patterns:** See `sentence_patterns.md` for science-forward citation restructuring
- **Paragraph templates:** See `paragraph_templates.md` for development arc patterns
- **Anti-patterns:** See `anti_patterns.md` for additional pitfalls in technical writing

---

**Document Status:** v1.0 - Style guide for scientifically literate public figure summaries
**Primary Application:** Figure summary writing and revision
**Audience Level:** Science News / Scientific American readers (college STEM education, science journalism)
