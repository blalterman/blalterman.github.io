<!--
Spent-When: MARKED(<self>)
Supersedes: none
-->
# Fix the flat tail on the Cumulative Citations plot

## Context

The "Cumulative Citations" plot on the publications page looks stalled for 2026: the line rises to ~1085 at 2026, then runs flat to a new final point at 2027.

Diagnosis (verified against origin/main, the 2026-09-28 CI log, and the live site):

- The data pipeline is healthy. The 2026-08-04 fix (ee25813, derive from `ads_metrics.json` instead of the mtime-cached per-bibcode fetch) is holding. The 2026 count has risen every Monday: 208 → 214 → 217 → 219 → 221 → 237 → 242 → 247 → 253. Total is 1099, and deploy and audit both passed on 2026-09-28.
- On 2026-09-28, the ADS citation histogram started returning a `2027` bin: `refereed to refereed: {"2027": 2}`. I infer these are citing papers already assigned to 2027 journal volumes (forward-dated bibcodes), because the bin appears in the ADS histogram before 2027 has started. I have not inspected the two papers. The fix does not depend on the cause.
- `scripts/derive_citations_by_year.py` keeps every year with a nonzero count, so `citations_by_year.json` now ends at 2027 (`refereed: [..., 256, 253, 2]`).
- `scripts/generate_citations_timeline.py` plots the cumulative sum at each year, so the final segment is 2026 (cum ≈1083) → 2027 (cum ≈1085). That near-flat tail is the stall you see. It will persist until 2027 citations accumulate next year.

The earlier fix addressed a different failure (frozen data). This is a new presentation bug triggered by ADS data that did not exist until last week.

## Approach

Fix the plotting layer only. Fold any year later than the current calendar year into the current year before accumulating. `citations_by_year.json` stays a faithful reshaping of ADS, so these remain valid without modification:
- `derive_counts()` and its total reconciliation (1099 == 1099)
- `audit_deployed_data.py`, which recomputes `derive_counts()` from deployed metrics and compares
- `verify_citations_derivation.py`, which uses the 2025 fixture
- `generate_publication_statistics.py` totals

Changes in `scripts/generate_citations_timeline.py`:
1. Add a small helper, e.g. `fold_future_years(years, ref, nonref, current_year)`. It sums every entry with `int(year) > current_year` into the `current_year` entry and creates that entry if it is absent. With `current_year = datetime.now(timezone.utc).year`, the output is `2018..2026` with 2026 = 255 refereed (253 + 2). The cumulative endpoint stays 1099, so no citations are dropped.
2. Print a one-line notice when folding happens (e.g. "Folded 2 citations dated 2027 into 2026") so the CI log shows it.
3. Call the helper right after loading the data and before `itertools.accumulate`. Nothing else in the plotting code changes.

Optional, same commit:
4. `src/components/publication-statistics.tsx:21`: the alt text hardcodes "from 2018-2026" and will go stale in January. Drop the year range, e.g. "Cumulative refereed and non-refereed citations by year".

`publication_statistics.json` → `citations_by_year.total_by_year` also contains 2027 now, but nothing in `src/` reads it (verified with git grep), so it needs no change.

Out of scope, noted for a check: `publications_timeline` could hit the same forward-dated-year issue when a 2027-volume paper appears. It is not affected today.

## Verification

1. `git pull --rebase` first. Local `main` has diverged (ahead 1, behind 3): the local JSON predates the 2027 bin, and the local session-stub commit `07ff5e5` has not been pushed.
2. `python scripts/generate_citations_timeline.py`, then confirm in the log: the fold notice, time span 2018-2026, total 1099.
3. View `public/plots/citations_by_year.png` and `_dark.png`. The line should end at 2026 with no flat tail.
4. `python scripts/verify_citations_derivation.py` and `python scripts/audit_deployed_data.py` still pass, since the JSON is untouched.
5. Commit (no push without your OK). The next Monday CI run regenerates the plot. Check the deployed PNG afterward.

---

## Empirical Findings (2026-10-02 trial run)

### End-state metrics

- Plotted span 2018-2027 (10 years) became 2018-2026 (9 years); 2026 refereed 253 became 255 after folding 2 citations dated 2027.
- Cumulative endpoint 1099 before and after (1086 refereed, 13 non-refereed), matching the plan's prediction.
- Commits predicted: 1 (fix plus optional alt text in the same commit). Landed: 1.

### Acceptance Criteria

| AC | Status | Evidence |
|---|---|---|
| Rebase onto origin/main before regenerating | PASS | `git pull --rebase`: "Successfully rebased and updated refs/heads/main"; stub commit rewritten to `3a2421b` |
| Generator logs fold, span 2018-2026, total 1099 | PASS | Output: "Folded 2 citation(s) dated 2027 into 2026", "Total citations: 1099", "Time span: 2018-2026 (9 years)" |
| Plot ends at 2026 with no flat tail | PASS | `public/plots/citations_by_year.png` viewed after regeneration; final point at 2026, about 1086 |
| verify_citations_derivation.py passes | PASS | "PASS: derivation reproduces the previous method on all 8 years." |
| audit_deployed_data.py passes | PASS | "PASS: the deployed site matches the repository and is internally consistent." |
| Fix reaches the live site | PASS | Deploy run 37026825558 concluded `success` on `414bd2c`; live `plots/citations_by_year.svg` last-modified 2026-10-02 15:26:26 GMT, 0 occurrences of "2027" (positive control: the pre-fix live PNG showed a 2027 tick) |

### Deviations from plan

- The plan left deployment to the next Monday CI run. The author asked for an immediate deploy; deploy.yaml has no push trigger, so it was dispatched manually with `gh workflow run deploy.yaml --ref main`.

### Commits

- `414bd2c` fix(plots): fold forward-dated citation years into the current year

## Spent-Mark: executed, findings recorded
