# Figure Summary Workflow for Future Papers

This document provides a complete workflow for writing figure summaries targeting scientifically literate public audiences. It synthesizes lessons from revising 35+ figure summaries across 10 papers (2018-2025), capturing patterns that achieve Science News/Scientific American accessibility without sacrificing scientific precision.

---

## Quick Start Checklist

Copy this checklist for each new figure:

```markdown
## Figure Summary Checklist

### Before Drafting
- [ ] Identified figure type (comparison, time series, multi-panel, statistical)
- [ ] Selected appropriate template from Common Patterns section
- [ ] Listed 3-5 key visual elements for what_we_see
- [ ] Identified the single most important finding for the_finding
- [ ] Prepared the front-loaded verdict for why_it_matters

### After Drafting
- [ ] what_we_see: 150-200 words, max 2 nesting levels
- [ ] the_finding: 200-250 words, max 3 nesting levels
- [ ] why_it_matters: 200-250 words, verdict in first 10 words
- [ ] Total: 500-700 words (target 600)
- [ ] No sentence exceeds 60 words (target 25-40)
- [ ] Max 1 parenthetical per sentence
- [ ] All sentences pass Skim Test (skeleton = core meaning)
- [ ] Fractal used for comparisons only, not enumerations
- [ ] No paragraph exceeds 250 words
```

---

## Step 1: Identify Figure Type

Before drafting, classify the figure to select the appropriate template.

### Type A: Comparison Figures
**Characteristics:** Two or more populations, conditions, or categories shown side-by-side
**Examples:** Fast vs. slow wind, protons vs. alphas, before vs. after threshold
**Structure:** Use fractal for the comparison; keep description simple

### Type B: Time Series Figures
**Characteristics:** Temporal evolution over solar cycles, missions, or events
**Examples:** 45-year helium evolution, solar cycle correlations
**Structure:** Front-load the temporal pattern; use enumeration for periods

### Type C: Multi-Panel Figures
**Characteristics:** 2-6 panels showing related views of the same phenomenon
**Examples:** Different energy channels, viewing angles, species
**Structure:** Brief panel-by-panel description; unified finding across panels

### Type D: Statistical/Distribution Figures
**Characteristics:** Histograms, scatter plots, correlations, fits
**Examples:** Power-law behavior, Gaussian decomposition, R-squared comparisons
**Structure:** Focus on the pattern, not the statistics; explain what numbers mean

### Type E: Schematic/Conceptual Figures
**Characteristics:** Illustrative diagrams explaining physical processes
**Examples:** Solar source regions, wave propagation, fractionation mechanisms
**Structure:** Map visual elements to physical concepts; minimal numbers

---

## Step 2: Draft Three Paragraphs

Each summary follows the same three-paragraph structure. Use these templates as starting points.

### Template: what_we_see (150-200 words, max 2 nesting levels)

**Purpose:** Describe what the reader sees in the figure. No interpretation yet.

**Template:**
```
[1-2 sentences]: Basic figure structure (panels, axes, data type)
[1-2 sentences]: Key visual elements (colors, markers, regions)
[1-2 sentences]: Data source or context (instrument, time period, species)
```

**Example (Paper 5 Figure 2):**
> This two-panel figure shows spectral index measurements across solar wind speeds. Panel (a) plots carbon-oxygen spectral index against speed, with individual measurements as gray points and running medians as a thick blue line. Panel (b) shows the same for iron-oxygen. Both panels span speeds from 300 to 700 km/s, covering 17 years of ACE spacecraft data.

**Anti-pattern to avoid:**
> This four-panel figure shows measurements from the Wind spacecraft's Faraday cup instrument viewing the solar wind from four different angles relative to the magnetic field---118, 139, 156, and 170---each panel plotting charge flux (vertical axis, in picoamperes on a logarithmic scale) versus energy-per-charge (horizontal axis, 0-4 kilovolts), revealing three distinct peaks...

The anti-pattern packs 12+ concepts into two sentences with 4+ nesting levels.

---

### Template: the_finding (200-250 words, max 3 nesting levels)

**Purpose:** Explain what patterns or results emerge from the visualization.

**Template:**
```
[1-2 sentences]: Primary observation (the main pattern)
[1-2 sentences]: Supporting details (quantitative values, comparisons)
[1-2 sentences]: Secondary pattern or contrast (if applicable)
[1-2 sentences]: What makes this finding notable
```

**Example (Paper 5 Figure 2):**
> The most striking pattern is what doesn't happen: spectral indices remain remarkably stable across all solar wind speeds. Carbon-oxygen ratios hover near -1.0 regardless of whether the wind is slow (350 km/s) or fast (650 km/s). Iron-oxygen shows slightly more scatter but the same fundamental stability.

> This constancy contradicts expectations. If fractionation occurred primarily in the corona, we might expect fast wind (from coronal holes) and slow wind (from active regions) to show different compositional fingerprints. Instead, the uniformity suggests fractionation happens earlier---during the initial ionization and collection process in the chromosphere.

---

### Template: why_it_matters (200-250 words, verdict in first 10 words)

**Purpose:** Connect findings to broader scientific significance. VERDICT FIRST.

**Template:**
```
[Sentence 1]: THE VERDICT - Main implication in first 10 words
[2-3 sentences]: What this means for our understanding
[1-2 sentences]: Practical applications or predictions
[1-2 sentences]: Connection to broader questions (optional)
```

**Example (Paper 5 Figure 2):**
> This stability rules out speed-dependent fractionation mechanisms. The Sun's compositional processing apparently occurs before the wind accelerates, during the initial plasma release from the chromosphere. Fast and slow wind inherit the same elemental fingerprint from this common origin, then diverge only in speed.

> For space weather forecasting, this means we cannot use composition to distinguish solar source regions based on speed alone. However, the finding opens a new diagnostic window: any compositional variations we do observe must trace genuine source differences, not acceleration effects.

**Anti-pattern (verdict buried):**
> By examining the correlation between spectral index and solar wind speed, accounting for measurement uncertainties, considering seasonal variations, and comparing results from multiple solar cycles, this figure demonstrates that compositional fractionation does not depend on wind speed.

The anti-pattern buries the verdict at position 40+.

---

## Step 3: Apply the 7 Guidelines

After drafting, verify each guideline. The most common revision needs are Guidelines 2 (sentence length) and 7 (paragraph length).

### Guideline Quick Reference

| # | Guideline | Target | Hard Limit | Quick Check |
|---|-----------|--------|------------|-------------|
| 1 | Fractal Depth | 2 levels (what_we_see), 3 levels (analytical) | --- | Count nested clauses, parentheticals, em-dashes |
| 2 | Sentence Length | 25-40 words | 60 words | Word count per sentence |
| 3 | Parenthetical Budget | 0-1 per sentence | 1 (parallel quantitative values = 1) | Count parentheses, em-dashes |
| 4 | Skim Test | Skeleton conveys meaning | --- | Delete parentheticals, read what remains |
| 5 | Fractal vs. Enumeration | Fractal for comparisons | --- | Lists should be simple sentences |
| 6 | Front-Load Verdicts | Verdict in first 10 words | --- | Check first sentence of why_it_matters |
| 7 | Paragraph Length | 150-250 words | 250 words | Word count per section |

### Most Common Violations (by frequency from 35+ revisions)

1. **Sentence length (Guideline 2):** 40% of revisions
2. **Paragraph length (Guideline 7):** 35% of revisions
3. **Enumeration bloat (Guideline 5):** 25% of revisions
4. **Buried verdict (Guideline 6):** 20% of revisions
5. **Excessive parentheticals (Guideline 3):** 15% of revisions

---

## Step 4: Self-Review Checklist

Before finalizing, run this validation pass:

### Pass 1: Structure Check
- [ ] Three sections present: what_we_see, the_finding, why_it_matters
- [ ] Word counts within targets (500-700 total)
- [ ] Each section under 250 words

### Pass 2: Sentence Audit
Count words in every sentence. Flag any exceeding 60 words.
- [ ] No sentence exceeds 60 words
- [ ] Average sentence length 25-40 words
- [ ] Longest sentence identified and reviewed

### Pass 3: Nesting Check
For each sentence, count nesting levels (parentheticals + em-dashes + subordinate clauses).
- [ ] what_we_see: max 2 levels
- [ ] the_finding: max 3 levels
- [ ] why_it_matters: max 3 levels

### Pass 4: Skim Test
Read the summary aloud, skipping all parenthetical content.
- [ ] Core meaning survives
- [ ] No critical information lost

### Pass 5: Verdict Position
- [ ] First sentence of why_it_matters contains the main implication
- [ ] Implication appears in first 10 words

---

## Common Patterns and Templates

### Pattern A: Comparison Figures (Fast vs. Slow Wind)

Use this template when the figure contrasts two populations.

**Structure:**
```
what_we_see:
- Basic figure structure (1-2 sentences)
- Visual distinction between populations (1-2 sentences)
- Data context (1 sentence)

the_finding:
- Main contrast stated (1 sentence)
- Population 1 characteristics (2-3 sentences)
- Population 2 characteristics (2-3 sentences)
- Boundary or transition (1-2 sentences)

why_it_matters:
- VERDICT: What the contrast means (1 sentence)
- Source implications (2-3 sentences)
- Practical applications (1-2 sentences)
```

**Example structure (from Paper 8 Figure 1):**
> **what_we_see:** Two-panel figure showing helium abundance vs. time. Top panel covers 1998-2024, bottom shows solar activity indicator. Fast wind shown in red, slow wind in blue.

> **the_finding:** Fast and slow wind show opposite relationships to solar activity. Fast wind helium peaks near solar maximum, then declines. Slow wind helium stays relatively constant throughout the cycle.

> **why_it_matters:** This divergence reveals fundamentally different source regions. Fast wind responds to coronal hole evolution. Slow wind samples a more uniform reservoir.

---

### Pattern B: Time Series Figures (Solar Cycle Evolution)

Use this template when the figure shows evolution over time.

**Structure:**
```
what_we_see:
- Axes and time span (1-2 sentences)
- Key features or annotations (1-2 sentences)
- Data source (1 sentence)

the_finding:
- Long-term trend (1-2 sentences)
- Cycle-to-cycle patterns (2-3 sentences)
- Notable anomalies (1-2 sentences)

why_it_matters:
- VERDICT: What the evolution reveals (1 sentence)
- Historical context (1-2 sentences)
- Predictive implications (1-2 sentences)
```

---

### Pattern C: Multi-Panel Figures

Use this template for 2-6 panels showing related views.

**Structure:**
```
what_we_see:
- Overall layout (1 sentence)
- Panel-by-panel brief description (1 sentence per panel, simple enumeration)
- Common elements (1 sentence)

the_finding:
- Unifying pattern across panels (2-3 sentences)
- Key panel-to-panel differences (2-3 sentences)
- Synthesis (1-2 sentences)

why_it_matters:
- VERDICT: What the multi-panel view reveals (1 sentence)
- Why multiple views were necessary (1-2 sentences)
- Implications (1-2 sentences)
```

**Anti-pattern to avoid (enumeration bloat from Paper 1 Figure 1):**
> This four-panel figure shows measurements from the Wind spacecraft's Faraday cup instrument viewing the solar wind from four different angles relative to the magnetic field---118, 139, 156, and 170. Each panel plots charge flux (vertical axis, in picoamperes on a logarithmic scale) versus energy-per-charge (horizontal axis, 0-4 kilovolts), revealing three distinct peaks in different colors: a dominant red peak for core protons (the main hydrogen component making up >90% of the solar wind), a secondary blue peak for beam protons...

**Correct approach:**
> This four-panel figure shows solar wind measurements from the Wind spacecraft. The Faraday cup instrument captures particles arriving at four angles (118, 139, 156, and 170 degrees). Each panel plots charge flux versus energy-per-charge. Three distinct peaks appear: red for core protons, blue for beam protons, and purple for alpha particles.

---

### Pattern D: Statistical/Distribution Figures

Use this template for histograms, scatter plots, and correlations.

**Structure:**
```
what_we_see:
- Plot type and axes (1-2 sentences)
- Key statistical features (1-2 sentences)
- Sample size and context (1 sentence)

the_finding:
- Primary statistical result (1-2 sentences)
- What the numbers mean physically (2-3 sentences)
- Comparison to expectations or other datasets (1-2 sentences)

why_it_matters:
- VERDICT: What the statistics prove (1 sentence)
- Physical interpretation (2-3 sentences)
- Predictive or diagnostic value (1-2 sentences)
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: The 85-Word Monster Sentence

From Paper 7 Figure 10 (pre-revision):
> Traditional one-dimensional classification using speed alone (e.g., 'fast = v > 500 km/s') misclassifies a substantial fraction of solar wind: panel (a) shows regions with mean speed 420-480 km/s (yellow) that span |sigma_c| from 0.3 to 0.9, indicating these intermediate speeds sample fundamentally different source regions depending on Alfvenicity and composition---the low-|sigma_c|, low-A_He portion is closed-field slow wind that happens to be unusually fast (perhaps from active region boundaries), while the high-|sigma_c|, mid-A_He portion is open-field fast wind that happens to be unusually slow (perhaps from small or equatorial coronal holes with weak expansion).

**Problems:** 85 words, 5 nesting levels, parentheticals within em-dash elaborations.

**Fix (4 sentences, 2 levels each):**
> Traditional speed-only classification misclassifies a substantial fraction of solar wind. Panel (a) shows regions with mean speed 420-480 km/s spanning cross helicity from 0.3 to 0.9. The low-Alfvenicity, low-helium portion at these speeds represents closed-field slow wind that happens to be unusually fast. The high-Alfvenicity, mid-helium portion represents open-field fast wind that happens to be unusually slow.

---

### Anti-Pattern 2: Enumeration Bloat

From Paper 1 Figure 1 (pre-revision):
> Three distinct peaks appear in different colors: a dominant red peak for core protons (the main hydrogen component making up >90% of the solar wind), a secondary blue peak for beam protons (a faster-moving subset of hydrogen), and a smaller purple peak for alpha particles (fully ionized helium atoms).

**Problem:** 4 nesting levels, each parenthetical contains additional context.

**Fix:**
> Three distinct peaks appear: red for core protons (the main hydrogen component), blue for beam protons (a faster-moving subset), and purple for alpha particles (fully ionized helium).

---

### Anti-Pattern 3: Buried Verdict

From Paper 1 Figure 8 (pre-revision):
> This figure reveals a critical tension in solar wind analysis: the most physically complete formula isn't always the most useful one. In principle, the full anisotropic Alfven speed including dynamic pressure should give the best representation, but in practice, it introduces more measurement uncertainty than physical correction.

**Problem:** Verdict buried after meta-commentary.

**Fix:**
> The most physically complete formula is not always the most useful one. In principle, the full anisotropic Alfven speed should give the best representation. In practice, it introduces more measurement uncertainty than physical correction.

---

### Anti-Pattern 4: Qualification Accumulation

**Problem pattern:** Main point followed by caveat, then speculation, then alternative interpretation---all in one sentence.

**Example:**
> Visual proof... not artifact BUT physical process... timing dominant BUT other factors---perhaps variations OR uncertainties.

**Fix:** One idea per sentence.
> This provides visual proof of the physical process. Alternative explanations---instrumental artifacts and timing effects---were tested and ruled out.

---

## Word Count Targets

| Section | Target | Hard Limit | Notes |
|---------|--------|------------|-------|
| what_we_see | 150-180 words | 200 words | Single paragraph acceptable |
| the_finding | 180-220 words | 250 words | 2-3 paragraphs recommended |
| why_it_matters | 180-220 words | 250 words | 2-4 paragraphs recommended |
| **Total** | **500-620 words** | **700 words** | Target 600 |

### Aggregate Statistics from Revision Project

| Metric | Before Revision | After Revision | Reduction |
|--------|-----------------|----------------|-----------|
| Average word count | 993 words | 517 words | 48% |
| Average nesting depth | 4-5 levels | 2-3 levels | 50% |
| Paragraphs per summary | 3 | 7 | +133% |
| Sentences exceeding 60 words | 2-3 per summary | 0 | 100% |

---

## Before/After Gallery

### Example 1: Enumeration Bloat to Separated Sentences

**Paper 1 Figure 1 (what_we_see)**

BEFORE (4 nesting levels, 669 total words):
> This four-panel figure shows measurements from the Wind spacecraft's Faraday cup instrument viewing the solar wind from four different angles relative to the magnetic field---118, 139, 156, and 170. Each panel plots charge flux (vertical axis, in picoamperes on a logarithmic scale) versus energy-per-charge (horizontal axis, 0-4 kilovolts). Three distinct peaks appear in different colors: a dominant red peak for core protons (the main hydrogen component making up >90% of the solar wind), a secondary blue peak for beam protons (a faster-moving subset of hydrogen), and a smaller purple peak for alpha particles (fully ionized helium atoms).

AFTER (2 nesting levels, 580 total words):
> This four-panel figure shows solar wind measurements from the Wind spacecraft. The Faraday cup instrument captures particles arriving at four angles relative to the magnetic field (118, 139, 156, and 170 degrees). Each panel plots charge flux versus energy-per-charge on a logarithmic scale spanning 0-4 kilovolts. Three distinct peaks appear in different colors: red for core protons (the main hydrogen component), blue for beam protons (a faster-moving subset), and purple for alpha particles (fully ionized helium).

**Changes:** Split first sentence, moved angles to parenthetical, collapsed peak descriptions.

---

### Example 2: 85-Word Monster to 4 Clean Sentences

**Paper 7 Figure 10 (why_it_matters)**

BEFORE (85 words, 5 levels):
> Traditional one-dimensional classification using speed alone (e.g., 'fast = v > 500 km/s') misclassifies a substantial fraction of solar wind: panel (a) shows regions with mean speed 420-480 km/s (yellow) that span |sigma_c| from 0.3 to 0.9, indicating these intermediate speeds sample fundamentally different source regions depending on Alfvenicity and composition---the low-|sigma_c|, low-A_He portion is closed-field slow wind that happens to be unusually fast (perhaps from active region boundaries), while the high-|sigma_c|, mid-A_He portion is open-field fast wind that happens to be unusually slow (perhaps from small or equatorial coronal holes with weak expansion).

AFTER (4 sentences, ~25 words each):
> Traditional speed-only classification misclassifies a substantial fraction of solar wind. Panel (a) shows regions with mean speed 420-480 km/s spanning cross helicity from 0.3 to 0.9. The low-Alfvenicity, low-helium portion at these speeds represents closed-field slow wind that happens to be unusually fast. The high-Alfvenicity, mid-helium portion represents open-field fast wind that happens to be unusually slow.

---

### Example 3: Paper 10 Figure 6-10 Aggregate Transformation

**Before revision (average):**
- 1090 words per summary
- 3 paragraphs (one per section)
- 5-6 nesting levels
- Multiple sentences exceeding 60 words

**After revision (average):**
- 537 words per summary (48% reduction)
- 7-8 paragraphs
- 2-3 nesting levels
- No sentences exceeding 60 words

---

### Example 4: Good Example (Paper 5 Figure 2)

This summary passed all guidelines and serves as a template:

**what_we_see (~150 words):**
> This two-panel figure compares spectral indices across solar wind speeds for two element pairs. Panel (a) shows the carbon-oxygen spectral index plotted against bulk solar wind speed, with individual hourly measurements shown as gray points and running medians as a blue line. Panel (b) presents the same analysis for iron-oxygen. Both panels span speeds from approximately 300 to 700 km/s, covering 17 years of ACE spacecraft observations.

**the_finding (~180 words):**
> The most newsworthy discovery here is what doesn't happen: despite spanning nearly the full range of solar wind conditions, spectral indices show remarkable stability. Carbon-oxygen ratios hover consistently near -1.0, whether the wind crawls at 350 km/s or races at 650 km/s. Iron-oxygen shows modestly more variability but follows the same fundamental pattern of constancy.

> This uniformity directly constrains where fractionation can occur. If compositional processing happened primarily during acceleration in the corona, we would expect fast wind from coronal holes and slow wind from active regions to carry distinct signatures. Instead, both wind types inherit nearly identical elemental fingerprints.

**why_it_matters (~190 words):**
> This stability rules out speed-dependent fractionation mechanisms. The compositional processing that enriches heavy elements relative to their photospheric abundances must occur before the wind accelerates, during initial plasma release from the chromosphere.

> For heliophysics, this finding locates the critical fractionation zone with new precision. The chromosphere-corona transition region, not the extended corona, hosts the key physics that determines solar wind composition.

> For space weather applications, the finding means we cannot use composition alone to identify fast versus slow wind sources. However, any compositional variations we do observe must trace genuine source differences rather than acceleration effects---a cleaner diagnostic signal than previously assumed.

**Highlight technique:** Front-loads the verdict ("This stability rules out..."), uses negative framing to highlight surprising stability, maintains parallel structure between panels.

---

## Cross-References

- **Core guidelines:** `style-guide/public_summaries.md` (the 7 guidelines with examples)
- **Fractal calibration:** `synthesis/fractal_calibration.md` (Golden Rule for when to use fractal)
- **Sentence patterns:** `style-guide/sentence_patterns.md` (science-forward citation restructuring)
- **Anti-patterns:** `style-guide/anti_patterns.md` (additional technical writing pitfalls)

---

**Document Status:** v1.0 - Workflow guide for figure summaries in future papers (Papers 11+)
**Source:** Lessons extracted from revising 35+ figure summaries across 10 papers (2018-2025)
**Primary Application:** Drafting and revising figure summaries for scientifically literate public audiences
