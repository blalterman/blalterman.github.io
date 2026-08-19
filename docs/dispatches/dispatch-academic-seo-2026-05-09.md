# Dispatch: Academic site SEO — Highwire citation tags + ScholarlyArticle JSON-LD + per-paper pages

**Generated:** 2026-05-09
**Branch:** main
**Work type:** software

## Scope

Extend `/Users/blalterman/observatories/code/blalterman.github.io` to emit Google Scholar-indexable metadata for the site's publication corpus. Three integration patterns are viable; the first task in the executing session is to resolve which pattern to implement (see § Open Items). After pattern selection, ship the matching subset of:

1. New static route at `src/app/publications/paper/[bibcode]/page.tsx` (relative to repo root) rendering one page per publication, with the abstract visible as page content (Pattern A or D).
2. Highwire Press citation tags emitted via Next.js Metadata API on per-paper pages (Pattern A or D).
3. `ScholarlyArticle` JSON-LD blocks on per-paper pages (Pattern A or D) or per-publication entries on `/Users/blalterman/observatories/code/blalterman.github.io/src/app/publications/[category]/page.tsx` (Pattern C).
4. Augmentation of `/Users/blalterman/observatories/code/blalterman.github.io/scripts/fetch_ads_publications_to_data_dir.py` to fetch `abstract`, `volume`, `issue`, `page` fields from ADS (Pattern A or D).
5. Extension of the `Publication` interface at `/Users/blalterman/observatories/code/blalterman.github.io/src/types/publication.ts` to include the new fields as optional (Pattern A or D).

## Motivation

The site is the public-facing portfolio for B. L. Alterman, research astrophysicist. Career-relevant search traffic for an academic portfolio flows through Google Scholar (paper discovery, citation lookups, ORCID resolution) at least as much as through Google's main index. Verified via grep on 2026-05-09: zero `citation_*` tags ship anywhere in the site (`grep -r "citation_" /Users/blalterman/observatories/code/blalterman.github.io/src/ /Users/blalterman/observatories/code/blalterman.github.io/public/data/` returned empty), zero per-paper pages exist, and zero per-page JSON-LD ships beyond the `Person` block at `/Users/blalterman/observatories/code/blalterman.github.io/src/app/layout.tsx:99`.

The Google Scholar inclusion guidelines (https://scholar.google.com/intl/en/scholar/inclusion.html, verified 2026-05-09) state three required tags for any document — `citation_title`, `citation_author`, `citation_publication_date` — plus a critical caveat that the abstract must be visible as page content, not just in `<meta>` tags. No tags currently meet this requirement on this site.

This dispatch is the academic-SEO follow-up to the SEO metadata helper work (seo-metadata-helper-2026-05-08, swept 2026-08-05; in git history), which fixes per-page canonical/og:title/twitter:title via a metadata helper at the relative path `src/lib/metadata.ts`. That dispatch must ship first (verified by § Prerequisites).

## Prerequisites

Run before drafting an implementation plan. Each must PASS.

```bash
# The metadata helper from the prior dispatch must be in place.
HELPER=/Users/blalterman/observatories/code/blalterman.github.io/src/lib/metadata.ts
test -f "$HELPER" \
  && grep -q "buildPageMetadata" "$HELPER" \
  && echo "OK helper present" \
  || echo "FAIL helper absent — the SEO metadata helper dispatch has not shipped"
```

```bash
# Project prerequisite checks (working dir, branch, sync, tree, Playwright MCP, port 9002, ADS data files).
bash -c 'set -e
test -f /Users/blalterman/observatories/code/blalterman.github.io/package.json
test -f /Users/blalterman/observatories/code/blalterman.github.io/CLAUDE.md
echo "OK working dir"
cd /Users/blalterman/observatories/code/blalterman.github.io
b=$(git branch --show-current); echo "branch: $b"
git fetch origin main --quiet
counts=$(git rev-list --left-right --count main...origin/main)
ahead=$(echo "$counts" | awk "{print \$1}")
behind=$(echo "$counts" | awk "{print \$2}")
[ "$behind" -eq 0 ] && echo "OK sync ahead=$ahead behind=0" || { echo "FAIL behind=$behind"; exit 1; }
[ -z "$(git status --porcelain | head -1)" ] && echo "OK tree clean" || echo "DIRTY"
claude mcp list 2>&1 | grep -q "playwright.*Connected" && echo "OK playwright" || echo "FAIL playwright"
P=$(lsof -i :9002 -t 2>/dev/null | head -1); [ -z "$P" ] && echo "OK port 9002" || echo "OCCUPIED PID=$P"
test -f public/data/ads_publications.json && echo "OK ADS data" || echo "FAIL ADS data"'
```

## Read First

1. seo-metadata-helper-2026-05-08 (swept 2026-08-05; `git log --diff-filter=D --all -- '*seo-metadata-helper*'`) — The prior SEO dispatch this one builds on. Read its § Acceptance Criteria and § Out of Scope to understand the existing metadata helper boundary; the academic-SEO work must not modify the helper.
2. `/Users/blalterman/observatories/code/blalterman.github.io/src/types/publication.ts` — The `Publication` interface lines 1–53. Current fields and which would need to be added.
3. `/Users/blalterman/observatories/code/blalterman.github.io/src/app/layout.tsx` lines 56–94 — Existing `Person` JSON-LD block injected via `dangerouslySetInnerHTML`. The `ScholarlyArticle` JSON-LD pattern, if used, mirrors this approach.
4. `/Users/blalterman/observatories/code/blalterman.github.io/src/app/publications/[category]/page.tsx` — Existing publications category route. Pattern C embeds JSON-LD here; Pattern A/D adds a sibling route at `paper/[bibcode]/`.
5. `/Users/blalterman/observatories/code/blalterman.github.io/scripts/fetch_ads_publications_to_data_dir.py` — Current ADS fetch script. Pattern A/D requires augmenting this to fetch `abstract`, `volume`, `issue`, `page`.
6. `/Users/blalterman/observatories/code/blalterman.github.io/public/data/ads_publications.json` — Sample one entry to confirm current field shape before changing it.
7. The metadata helper file at the path verified in § Prerequisites — Read-only reference; do NOT modify per § Anti-Patterns.

## Decisions

**DECIDED (user-confirmed in authoring session 2026-05-09):**

- This dispatch is its own scoped unit, separate from the metadata-helper dispatch. The metadata-helper dispatch ships first; this one runs after.
- The metadata helper produced by the prior dispatch is not modified by this dispatch. New helpers (e.g., a `src/lib/scholarly-metadata.ts`) are siblings.
- Description-channel-tuning (single vs three description fields per page) is NOT in scope here — that decision belongs in a separate content dispatch.

**DECIDED (2026-05-19):**

- **Pattern C only.** Patterns A and D rejected. Site architecture treats publications as inputs to thematic synthesis on research subpages, not as standalone destinations; per-publication landing pages would compete with the thematic layer. See project memory `project_publications-are-inputs-not-destinations.md`. This resolves Open Item 1 and renders Open Items 2 (abstract hosting), 3 (build-time cost), and 4 (coverage scope) moot — all three only apply under Pattern A or D.
- **Open Item 5 (`og:type: article` extensions for ben + research subpages) is descoped from this dispatch.** Scope misalignment: OI-5 targets social-share previews on non-publication pages, not Google Scholar indexability for publications. If pursued later, author a separate dispatch.

**PROPOSED (Claude's implementation hypothesis — receiving session must validate before building):**

- File for any new helper: `src/lib/scholarly-metadata.ts` (relative to repo root). Mirrors the prior dispatch's helper location and style.
- Per-paper route path (Pattern A/D): `/publications/paper/[bibcode]/`, slotting under the existing `/publications/[category]` namespace.
- JSON-LD emission technique: `<script type="application/ld+json" dangerouslySetInnerHTML={{...}}>` injected from the page component, matching the `layout.tsx:99` pattern.
- Highwire tag emission technique: Next.js `Metadata.other` field, where each `citation_*` key maps to a string or string-array per the spec.

## Open Items (RESOLVE BEFORE IMPLEMENTATION)

Surface each to the user before writing code. None has a default; each is a real choice.

1. **Architectural pattern: A vs C vs D.**
   - Pattern A — Per-paper landing pages. Creates `/publications/paper/[bibcode]/` (one page per publication, ~150 routes). Page renders title, authors, journal/year, visible abstract, DOI link, citations count. `generateMetadata()` emits `citation_*` tags via `Metadata.other`. Pre-work: augment fetch script to pull abstract/volume/issue/page; re-fetch all publications; extend `Publication` type.
   - Pattern C — JSON-LD only, no new routes. Embeds `ScholarlyArticle` JSON-LD blocks on existing `/publications/[category]/` pages, one per publication, each with `mainEntityOfPage` pointing to the journal URL (not the portfolio). No new routes, no schema changes, no abstract fetching.
   - Pattern D — A + C combined. Per-paper landing pages emit `citation_*` tags AND `ScholarlyArticle` JSON-LD with `sameAs`/`mainEntityOfPage` linking to the journal/ADS.

2. **Abstract hosting permission (Pattern A or D only).** Hosting paper abstracts as visible page content on `/publications/paper/[bibcode]/` is required for Google Scholar inclusion per the verified guidelines. Most journal publication agreements permit author-hosted abstracts; this is per-publisher. Verify with the user that hosting is permitted for the corpus before committing to abstract fetching and storage.

3. **Build-time cost (Pattern A or D only).** ~150 new static routes, plus an ADS API call per publication during the fetch phase, plus JSON file growth (current `ads_publications.json` is 150 entries; abstracts add ~1–2 KB each = ~200–300 KB). Confirm with user that the build-time and JSON-size cost is acceptable.

4. **Coverage scope.** The 150 ADS publications mix `publication_type: article` (refereed), conference proceedings, datasets, white papers. Decide: per-paper pages for all of them, or refereed articles only? Scholar's guidelines cover articles, theses, and conference papers — so refereed-only would still cover the bulk of citation-relevant content.

## Acceptance Criteria

Receiving session selects exactly one set based on Open Item 1's resolution.

### Pattern A or D selected

- [ ] File at relative path `src/app/publications/paper/[bibcode]/page.tsx` exists, exports `generateStaticParams`, `generateMetadata`, and a default page component.
- [ ] `generateStaticParams` returns one entry per publication in `public/data/ads_publications.json` (or one per refereed-article entry, per Open Item 4 resolution).
- [ ] `/Users/blalterman/observatories/code/blalterman.github.io/src/types/publication.ts` includes `abstract?: string`, `volume?: string`, `issue?: string`, `page?: string` (or equivalent named fields aligned with ADS API field names).
- [ ] `/Users/blalterman/observatories/code/blalterman.github.io/scripts/fetch_ads_publications_to_data_dir.py` requests the new fields from the ADS API and writes them into `public/data/ads_publications.json`.
- [ ] After re-fetch, `python3 -c "import json; d=json.load(open('public/data/ads_publications.json')); print(sum(1 for p in d if 'abstract' in p))"` reports a count greater than 0.
- [ ] Against dev server on port 9002, on route `/publications/paper/2025ApJ...982L..40A` (sample Alterman first-author paper), `document.querySelectorAll('meta[name^="citation_"]').length >= 4` (citation_title, ≥1 citation_author, citation_publication_date, citation_doi).
- [ ] Same route: `document.querySelectorAll('script[type="application/ld+json"]').length >= 2` (one inherited from layout's Person, one ScholarlyArticle from the page).
- [ ] Same route: the abstract text from the source JSON entry is present in `document.body.innerText` (visible page content, per Scholar requirement).
- [ ] `npm run typecheck` exits 0.
- [ ] `npm run build` exits 0; build summary shows the new dynamic route and a path count matching Acceptance Criterion item 2.
- [ ] All commits use conventional-commits subjects. Example subjects: `feat(scripts): fetch abstract, volume, issue, page from ADS`, `feat(seo): add per-paper pages with Highwire citation tags and ScholarlyArticle JSON-LD`.

### Pattern C selected

- [ ] `/Users/blalterman/observatories/code/blalterman.github.io/src/app/publications/[category]/page.tsx` (or a sibling component it renders) emits one `<script type="application/ld+json">` block per publication shown on the category page.
- [ ] Each emitted block parses as valid JSON and contains `"@type": "ScholarlyArticle"`, `"headline"` matching the publication title, `"author"` with one entry per author, `"datePublished"` in ISO format, `"mainEntityOfPage"` set to the publication's `url` field (the journal/DOI URL, not a portfolio URL).
- [ ] Against dev server on port 9002, on route `/publications/refereed`, `Array.from(document.querySelectorAll('script[type="application/ld+json"]')).filter(s => JSON.parse(s.textContent)['@type'] === 'ScholarlyArticle').length` equals the number of refereed publications shown on that page.
- [ ] No new routes added under `src/app/`.
- [ ] No fields added to `Publication` interface in `src/types/publication.ts`.
- [ ] No changes to `scripts/fetch_ads_publications_to_data_dir.py`.
- [ ] `npm run typecheck` exits 0; `npm run build` exits 0.
- [ ] Commit subject example: `feat(seo): add ScholarlyArticle JSON-LD on publication category pages`.

### Regardless of pattern

- [ ] `npm run lint 2>&1 | grep -E "src/(app|lib)/" | grep -v -E "(contact\.tsx|publication-filters\.tsx|publication-statistics\.tsx|use-toast\.ts)"` produces no output (no new lint errors in `src/app/` or `src/lib/`).
- [ ] No modifications to the metadata helper file produced by the prior dispatch (path verified in § Prerequisites).
- [ ] No modifications to `/Users/blalterman/observatories/code/blalterman.github.io/src/app/layout.tsx`.
- [ ] No push to `origin/main` without explicit user approval (auto-mode classifier soft-blocks this regardless).

## Anti-Patterns

- **Do NOT modify the metadata helper file produced by the prior dispatch (path verified in § Prerequisites).** It is the prior dispatch's deliverable and is owned by that scope. New helpers added by this dispatch live in sibling files (e.g., `src/lib/scholarly-metadata.ts`). Reason: scope-bleeding between dispatches makes "what was authorized when" ambiguous and corrupts the closing protocol's empirical-findings record.
- **Do NOT modify `/Users/blalterman/observatories/code/blalterman.github.io/src/app/layout.tsx`.** Its existing JSON-LD `Person` block is correct for the site-level identity claim; per-paper additions are local to per-paper pages. Reason: layout-level fields serve site-wide purposes and changing layout risks scope creep.
- **Do NOT inline 150 abstracts into `public/data/ads_publications.json` until § Open Items item 2 (abstract hosting permission) is resolved.** Reason: paper abstracts are subject to publisher copyright. Hosting permission is per-publisher.
- **Do NOT bundle the description-channel-tuning question into this dispatch.** Single vs three description fields per page is a separate decision that belongs in a content dispatch. Reason: prior session 2026-05-09 explicitly DECIDED this scope split.
- **Do NOT push `git push origin main` without explicit user approval.** The auto-mode classifier soft-blocks main pushes regardless; the user must run `! git push origin main` themselves from their prompt. Reason: documented in user's `~/.claude/CLAUDE.md`.
- **Do NOT add `ResearchProject`, `Dataset`, or other Schema.org types beyond `ScholarlyArticle` in this dispatch.** Reason: per § Out of Scope.

## Out of Scope

- Channel-tuned `og:description` / `twitter:description` per page. Owned by a future content dispatch.
- `ResearchProject` or `Dataset` JSON-LD types. Separate concern.
- ORCID badges, DOI badges, or other UI elements visible on the page beyond what § Acceptance Criteria requires.
- Sitemap improvements (`sitemap.xml`, `robots.txt` tuning).
- Modifications to ADS data-update GitHub Actions workflows. The fetch script can be augmented; the workflow that invokes it does not need to change unless the new fetch fields require a longer timeout.

## Verification

Run from working directory `/Users/blalterman/observatories/code/blalterman.github.io`.

```bash
git log --oneline -5
```
**Expected:** the top of `git log` shows the SEO metadata helper commit (subject `fix(seo): set per-page canonical, og:title, and twitter:title via metadata helper`) within the last few commits. If the metadata-helper dispatch has not shipped, this dispatch's prerequisites fail.

```bash
npm run typecheck && echo "PASS typecheck"
```
**Expected:** Exit 0; final line `PASS typecheck`.

```bash
npm run lint 2>&1 | grep -E "src/(app|lib)/" | grep -v -E "(contact\.tsx|publication-filters\.tsx|publication-statistics\.tsx|use-toast\.ts)"
```
**Expected:** No output.

```bash
npm run build 2>&1 | tail -10
```
**Expected:** Exit 0. For Pattern A or D, build summary shows path count for `/publications/paper/[bibcode]` matching the publication count selected by Open Item 4.

For Pattern A or D — Highwire tag verification on a sample paper page:

```bash
npm run dev &
DEV_PID=$!
until curl -sf -o /dev/null http://localhost:9002/; do sleep 1; done
echo "ready"
```

Use `mcp__playwright__browser_navigate` to load `http://localhost:9002/publications/paper/2025ApJ...982L..40A`, then `mcp__playwright__browser_evaluate` to extract:

```js
({
  citationTags: Array.from(document.querySelectorAll('meta[name^="citation_"]')).map(m => ({name: m.name, content: m.content})),
  jsonLdCount: document.querySelectorAll('script[type="application/ld+json"]').length,
  abstractVisible: document.body.innerText.includes(/* expected abstract substring */)
})
```

**Expected:** `citationTags.length >= 4` with at minimum `citation_title`, `citation_author`, `citation_publication_date`, `citation_doi`. `jsonLdCount === 2`. `abstractVisible === true`.

For Pattern C — JSON-LD verification on a category page:

Use `mcp__playwright__browser_navigate` to `http://localhost:9002/publications/refereed`, then evaluate:

```js
Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
  .map(s => JSON.parse(s.textContent))
  .filter(o => o['@type'] === 'ScholarlyArticle')
  .length
```

**Expected:** count equals the number of refereed publications listed on the page.

After verification:

```bash
kill $DEV_PID
```

Stage commits with conventional-commits subjects (see § Acceptance Criteria for examples). Wait for explicit user approval before push.

## Operational Constraints

- **Working directory:** `/Users/blalterman/observatories/code/blalterman.github.io`. All paths in this dispatch are absolute except where explicitly noted as relative-to-repo-root.
- **Dev server port:** 9002 (per `package.json` script `dev`: `next dev --turbopack -p 9002`).
- **Playwright MCP:** registered in `~/.claude.json` under this project's entry. Tools (`mcp__playwright__browser_navigate`, `mcp__playwright__browser_evaluate`, etc.) auto-load when starting a session in this repo.
- **Conventional commits:** required (per repo history pattern). Multiple commits acceptable for this dispatch (script change + page/JSON-LD change can be separate logical commits).
- **Push policy:** never push to `origin/main` without explicit user approval. The auto-mode classifier soft-blocks direct main pushes regardless; the user must run `! git push origin main` themselves from their prompt.
- **Deploy policy:** the `Deploy Static Site to GitHub Pages` workflow at `.github/workflows/deploy.yaml` does NOT trigger on push events. After push, trigger deploy explicitly: `gh workflow run deploy.yaml --ref main`. Do not run that command without user approval.
- **Static export:** `output: 'export'` in `next.config.ts` is required for GitHub Pages deploy. Do not introduce server-side rendering features (SSR, ISR, runtime API routes) — they will break the build.
- **ADS API key:** `ADS_DEV_KEY` and `ADS_ORCID` environment variables required by the fetch script. Receiving session should verify these are set before running the augmented fetch.

## Closing Protocol

After § Verification passes, follow `~/.claude/rules/handoff-protocol.md` § "Closing Protocol":

1. `/empirical-findings /Users/blalterman/.claude/dispatches/dispatch-academic-seo-2026-05-09.md`
2. `/tombstone-launch /Users/blalterman/.claude/dispatches/launch-academic-seo-2026-05-09.md` then `/purge-tombstoned /Users/blalterman/.claude/dispatches/launch-academic-seo-2026-05-09.md`
3. `bash ~/.claude/tools/lint-ai-clean.sh /Users/blalterman/.claude/dispatches/dispatch-academic-seo-2026-05-09.md`

---

## Empirical Findings (2026-05-19 trial run)

### End-state metrics

- Commits predicted: 1. Commits landed: 1. Match.
- Files changed: 2 (1 new, 1 modified). Insertions: 43. Deletions: 1.
- ScholarlyArticle blocks on `/publications/refereed`: 40. Refereed publication count: 40. Match.
- ACs: 12 PASS, 0 FAIL, 0 DEFERRED.

### Acceptance Criteria

| AC | Status | Evidence |
|---|---|---|
| `[category]/page.tsx` emits one JSON-LD block per publication | PASS | 40 blocks on `/publications/refereed` (Playwright eval) |
| Each block: valid JSON, `@type: ScholarlyArticle`, `headline`, `author` array, `datePublished` ISO, `mainEntityOfPage` = DOI URL | PASS | Playwright sample: `datePublished: "2026-04"`, `mainEntityOfPage: "https://dx.doi.org/10.1029/2026JA035166"` |
| Playwright count on `/publications/refereed` equals refereed count | PASS | 40 = 40 |
| No new routes under `src/app/` | PASS | `npm run build` summary; no `publications/paper` entry |
| No fields added to `Publication` interface | PASS | `src/types/publication.ts` unmodified (git diff) |
| No changes to fetch script | PASS | `fetch_ads_publications_to_data_dir.py` unmodified (git diff) |
| `npm run typecheck` exits 0 | PASS | stdout: `PASS typecheck` |
| `npm run build` exits 0 | PASS | exit 0; SSG routes unchanged |
| Commit subject matches example | PASS | `406100f feat(seo): add ScholarlyArticle JSON-LD on publication category pages` |
| No modifications to `src/lib/metadata.ts` | PASS | git diff — untouched |
| No modifications to `src/app/layout.tsx` | PASS | git diff — untouched |
| No push to `origin/main` without user approval | PASS | not pushed; user runs `! git push origin main` |

### Open Item dispositions

| Open Item | Disposition |
|---|---|
| OI-1: Architectural pattern A vs C vs D | RESOLVED — Pattern C selected (DECIDED 2026-05-19 before execution) |
| OI-2: Abstract hosting permission | SUPERSEDED — Pattern C does not host abstracts; moot |
| OI-3: Build-time cost | SUPERSEDED — Pattern C adds no new routes and no ADS re-fetch; moot |
| OI-4: Coverage scope | SUPERSEDED — Pattern C applies JSON-LD to all category pages via the existing `publications` array; no per-paper scope decision needed |
| OI-5: `og:type: article` extensions for ben + research subpages | DEFERRED — descoped from this dispatch per DECIDED 2026-05-19; belongs in a separate content dispatch |

### Commits

- `406100f` feat(seo): add ScholarlyArticle JSON-LD on publication category pages
