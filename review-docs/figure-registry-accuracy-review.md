# Figure Registry: Accuracy-Sensitive Review Items

**Generated:** 2026-04-14
**Source:** `public/data/figure-registry.json` (94 figures, 282 text blocks)
**Method:** Option B+ text quality review (6 recalibrated propositions + 2 gap checks)

Items below may affect scientific meaning if edited. Each needs domain expert review before any changes are applied.

---

## Category: S4 Hedging — Double Hedges

These sentences contain two uncertainty markers. Both hedges may be intentionally calibrated to the actual level of certainty. Only simplify if both hedges express identical uncertainty.

### aa51550-24/fig_8 / the_finding
- **Original:** "This unexpected result suggests the unknown fractionation mechanism may couple to an element's electrical charge rather than its weight."
- **Pattern:** "suggests...may" — two hedges on the same claim
- **Proposed:** "This unexpected result suggests the unknown fractionation mechanism couples to an element's electrical charge rather than its weight." OR "The unknown fractionation mechanism may couple to an element's electrical charge rather than its weight."
- **Risk:** The double hedge may be deliberate — "suggests" hedges the evidence quality while "may" hedges the mechanism itself. Removing either changes epistemic strength.

### s11207-021-01801-9/fig_4 / the_finding
- **Original:** "Cycle 22 is the sole exception, showing a systematic drift toward earlier dates with larger windows, which suggests its true shutoff may have occurred somewhat earlier than the baseline 250-day estimate captures."
- **Pattern:** "suggests...may have occurred" — two hedges on the same claim
- **Proposed:** "...which suggests its true shutoff occurred somewhat earlier..." OR "...its true shutoff may have occurred somewhat earlier..."
- **Risk:** "Suggests" hedges the inference from data; "may have" hedges the conclusion. Both may be appropriate given Cycle 22's anomalous behavior.

### Alterman_2019_ApJL_879_L6/fig_2a / why_it_matters
- **Original:** "Previous studies found that the helium-sunspot connection weakened and nearly disappeared in faster wind, suggesting it might be a purely slow-wind phenomenon."
- **Pattern:** "suggesting...might" — two hedges on the same inference
- **Proposed:** "...suggesting it is a purely slow-wind phenomenon." OR "...which might make it a purely slow-wind phenomenon."
- **Risk:** The double hedge is reporting what *previous studies* suggested — this is historical context being appropriately distanced, not the author's own claim. Simplifying may make it sound like the author endorses the conclusion more strongly than intended.

---

## Category: S2 Progressive Explanation — Terms Requiring Domain Expertise

These technical terms appear in `why_it_matters` blocks without plain-language explanations. Adding definitions requires domain knowledge to ensure accuracy.

### "cross helicity" (3 blocks)
- **Alterman_2025_ApJL_982_L40/fig_11:** "helium abundance and cross helicity, without requiring a mass spectrometer"
- **Alterman_2026_ApJL_996_L12/fig_2:** "compressive density fluctuations that the cross helicity alone cannot capture"
- **Alterman_2026_ApJL_996_L12/fig_22:** "hydrogen compressibility and normalized cross helicity are complementary measures"
- **Suggested definition (needs verification):** "(a measure of how wave-like the solar wind fluctuations are)"
- **Risk:** Cross helicity (sigma_c) measures alignment between velocity and magnetic field fluctuations. A simplified definition may lose the directionality or the connection to Alfven wave content.

### "Alfvenic slow wind" (2 blocks)
- **Alterman_2025_ApJL_982_L40/fig_4:** "wave activity alone cannot classify the solar wind: some slow wind has high wave activity (the Alfvenic slow wind)"
- **Alterman_2025_ApJL_982_L40/fig_5:** "the key evidence for explaining the Alfvenic slow wind"
- **Note:** fig_4 already provides inline context ("some slow wind has high wave activity"). fig_5 assumes the reader knows what Alfvenic slow wind is. Could add: "(slow wind with wave-like properties typically associated with fast wind)"

### "ponderomotive force" (1 block)
- **aa51550-24/fig_6:** "including ponderomotive-force-driven FIP (first ionization potential) fractionation"
- **Note:** Highly technical term. Could add "(a wave-driven force)" but this is a significant simplification.

---

## Category: P2 Topic Sentences — Meta-Referential Openers

~25 `why_it_matters` blocks open with "This figure/panel provides/reveals/demonstrates X" rather than leading with X directly. These contain specific content but use meta-framing. Rewriting to lead with content would strengthen the opening but risks changing emphasis.

**Pattern examples (not exhaustive):**

| Figure | Current Opening | Content-Leading Alternative |
|--------|----------------|---------------------------|
| 2026_L12/fig_4 | "This figure introduces the paper's central innovation: hydrogen compressibility as a third classification variable." | "Hydrogen compressibility serves as a third classification variable..." |
| 2026_L12/fig_7 | "This figure provides the first visual evidence for the paper's central claim: the unexpectedly high helium..." | "The unexpectedly high helium in some fast wind is associated with..." |
| 2026_L12/fig_12 | "This figure provides the clearest quantitative evidence that compressible fluctuations cause anomalous helium behavior..." | "Compressible fluctuations cause anomalous helium behavior in fast wind..." |
| 2025_L40/fig_4 | "This figure reveals why wave activity alone cannot classify the solar wind..." | "Wave activity alone cannot classify the solar wind..." |
| 2025_984/fig_2 | "This figure bridges the observational gap between the inner heliosphere and Earth's orbit." | "The observational gap between the inner heliosphere and Earth's orbit is bridged..." |
| aa51550-24/fig_5 | "This figure serves as a critical consistency check for the entire analysis." | "The bilinear fitting framework passes a critical consistency check..." |
| aa51550-24/fig_8 | "This figure provides the strongest observational clue about what drives the mysterious fast-wind fractionation." | "The strongest observational clue about fast-wind fractionation comes from..." |

**Decision needed:** Is the "This figure" framing appropriate for web content (where the figure IS the context), or should these be rewritten to be more content-forward?

---

## Category: S5 Sentence Length — Remaining Long Sentences

11 sentences >40 words were left as-is during step 3e. These are either visual enumerations in `what_we_see` (7) or single causal chains where splitting would break the argument (4).

**Visual enumerations (leave as-is unless you prefer split):**
- [59w] `2025_L40/fig_9/what_we_see` — 5 speed range descriptions
- [56w] `2025_984/fig_1/what_we_see` — 4 color band descriptions
- [48w] `aa51550-24/fig_3/what_we_see` — element curve enumeration
- [43w] `2019_L6/fig_3a/what_we_see` — data point description
- [42w] `2025_L40/fig_8/what_we_see` — speed range segments
- [41w] `2023_952/fig_8/what_we_see` — solar cycle marker enumeration
- [41w] `2026_L12/fig_13/what_we_see` — panel description

**Argumentative sentences (splitting risks losing causal thread):**
- [45w] `aa51550-24/fig_6/the_finding` — triple rule-out: "cannot be explained by X, by Y, or by Z"
- [43w] `2023_952/fig_9/why_it_matters` — single claim with CIR/SEP expansion
- [43w] `2025_L40/fig_10b/why_it_matters` — causal chain with "because...independently of"
- [42w] `2025_984/fig_1/the_finding` — Alfven wave definition via em-dash appositive

---

## Category: what_we_see Cross-References

7 `what_we_see` blocks still contain cross-references to other figures (e.g., "from Figure 5", "from the previous figure"). These were outside the scope of step 3a (which fixed `alt` fields only) but affect standalone readability of the summary text.

| Figure | Cross-Reference in what_we_see |
|--------|-------------------------------|
| 2023_952/fig_8 | "from quiet-time abundance variability fits" (FIXED in alt, but what_we_see may still reference previous figures contextually) |
| 2026_L12/fig_8 | "zooms into the helium-speed saturation region" (FIXED) |

**Note:** Steps 3a already fixed the `what_we_see` opening sentences for all 9 cross-referencing entries. This item is for awareness — verify the remaining text within those blocks doesn't introduce new cross-references further into the paragraph.

---

## Summary

| Category | Count | Action Needed |
|----------|-------|--------------|
| S4 Double hedges | 3 | Review each: keep both, simplify to one, or remove |
| S2 Technical terms | 3 terms (6 instances) | Provide or verify plain-language definitions |
| P2 Meta-referential openers | ~25 blocks | Decide: rewrite to content-forward, or keep as-is for web |
| S5 Remaining long sentences | 11 | Review: split if desired, or accept for this content type |
| what_we_see cross-refs | 0 remaining (all fixed in 3a) | Verify |
