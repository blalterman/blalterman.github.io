# Progress Log (blalterman.github.io)

Reverse-chronological session log. Newest entry on top. Written by /session:close (or a project /close), read by /session:start.

---

## 2026-07-15
- Done: Shipped self-hosted per-publication PDF downloads. Added `public/data/publication-pdfs.json` (53-entry registry keyed by bibcode), joined in `loadAllPublications` (`src/lib/data-loader.ts`) with a build-time orphan-key positive control; added `pdfPath`/`pdfVersion` to `src/types/publication.ts`; added a version-labeled ("PDF"/"Preprint") Download button, centered in the links cell, in `src/components/publication-filters.tsx`. Copied 53 license-verified PDFs into `public/papers/pdfs/` at native resolution. Backfilled full author lists into `non_ads_publications.json` from Zenodo; removed the dead USRA link from the Brandt entry. Commits: `9e787f4`, `fbf1daa`, `cd469b5`, `7a254ab`, `6b6d0b8`, `962563e` (Decadal commit rebased onto the weekly automation commits). Deployed live via `workflow_dispatch` of `deploy.yaml` (run 29434958713, success). Coverage: refereed 39, white papers 13, thesis 1.
- Decisions (DECIDED): host all refereed + thesis + white papers at native resolution (no downsampling, no Git LFS — Pages does not serve LFS objects); label white-paper downloads "PDF" not "White Paper"; version-of-record hosted where CC-licensed (31), arXiv preprint where the VoR is publisher-copyright (8: 2 arXiv-CC + 6 author-right basis), thesis (1), white papers (13: 7 Zenodo CC-BY/CC0 + 6 BAAS Decadal CC-BY 4.0); PDF registry lives OUTSIDE the weekly-overwritten `ads_publications.json` and is joined by bibcode (validated under a real weekly ADS overwrite this session — zero orphans).
- Open threads: Brandt Helio2050 white paper (`NOADS-Helio2050ISP`) is the only unhosted white paper — no reachable source (USRA link dead 404, not on Zenodo/BAAS); awaiting a user-supplied PDF copy. AAS/BAAS/MDPI block `urllib`/WebFetch (403/Cloudflare); the working technique is fetching via the real Chrome browser (`mcp__claude-in-chrome` fetch-in-page).
- Next action: When the user provides the Brandt PDF, copy it to `public/papers/pdfs/NOADS_Helio2050ISP.pdf`, add its `publication-pdfs.json` entry (`version: whitepaper`), backfill its ~91-author list, build, commit, push, then re-trigger `deploy.yaml` (`gh workflow run deploy.yaml --ref main`).
- Active LP: none
- Active handoff: none
