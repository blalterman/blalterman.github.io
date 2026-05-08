# Launch Prerequisites

Project-specific environment checks for `/launch-prompt`. Each section below has a fenced bash block (the verification command) and a `Format:` line specifying how the result is rendered into the launch prompt's "Prerequisites verified" section.

If any check fails, the launch prompt prepends a BLOCKING banner naming the failing prerequisite.

---

## Working Directory

```bash
test -f /Users/blalterman/observatories/code/blalterman.github.io/package.json \
  && test -f /Users/blalterman/observatories/code/blalterman.github.io/CLAUDE.md \
  && echo "OK" || echo "FAIL — package.json or CLAUDE.md missing at expected location"
```
Format: `- [ ] Working directory: {OK / FAIL — package.json or CLAUDE.md missing at expected location}`

## Branch

```bash
cd /Users/blalterman/observatories/code/blalterman.github.io && git branch --show-current
```
Format: `- [ ] Branch: {branch_name — flag for receiver review if not main}`

## Sync With Origin

PASS when local main is even with `origin/main` or ahead of it. FAIL when behind (would conflict on push). Multiple-cycle local development is the normal pattern; ahead is expected.

```bash
cd /Users/blalterman/observatories/code/blalterman.github.io \
  && git fetch origin main --quiet \
  && counts=$(git rev-list --left-right --count main...origin/main) \
  && ahead=$(echo "$counts" | awk '{print $1}') \
  && behind=$(echo "$counts" | awk '{print $2}') \
  && if [ "$behind" -eq 0 ]; then echo "OK ahead=$ahead behind=0"; else echo "FAIL ahead=$ahead behind=$behind — pull from origin/main before working"; fi
```
Format: `- [ ] Sync: {OK ahead=<N> behind=0 / FAIL ahead=<N> behind=<M> — pull from origin/main before working}`

## Working Tree

```bash
cd /Users/blalterman/observatories/code/blalterman.github.io && git status --porcelain | head -10
```
Format: `- [ ] Working tree: {clean / dirty: <N> files — receiver decides whether to stash, commit, or proceed}`

## Playwright MCP

```bash
claude mcp list 2>&1 | grep -E "playwright.*Connected" >/dev/null && echo "OK" || echo "NOT_CONNECTED — register via 'claude mcp add playwright -- npx -y @playwright/mcp@latest'"
```
Format: `- [ ] Playwright MCP: {OK / NOT_CONNECTED — register via 'claude mcp add playwright -- npx -y @playwright/mcp@latest'}`

## Port 9002

Dev server (`npm run dev`) listens on port 9002 per `package.json`. A zombie `next-server` from a prior session blocks startup. The `kill <PID>` instruction in the failure message resolves it.

```bash
PID=$(lsof -i :9002 -t 2>/dev/null | head -1) && [ -z "$PID" ] && echo "FREE" || echo "OCCUPIED by PID $PID — kill with 'kill $PID'"
```
Format: `- [ ] Port 9002: {FREE / OCCUPIED by PID <N> — kill with 'kill <N>'}`

## Required Data Files

Files auto-fetched weekly via GitHub Actions workflows (`update-ads-publications.yml`, `update-ads-metrics.yml`, `update_annual_citations.yml`). Manual refresh via `python3 scripts/fetch_ads_publications.py` and siblings if missing.

```bash
test -f /Users/blalterman/observatories/code/blalterman.github.io/public/data/ads_publications.json \
  && test -f /Users/blalterman/observatories/code/blalterman.github.io/public/data/ads_metrics.json \
  && test -f /Users/blalterman/observatories/code/blalterman.github.io/public/data/citations_by_year.json \
  && echo "OK" || echo "FAIL — one or more ADS data files missing; run scripts/fetch_ads_publications.py and siblings, or trigger update-ads-publications workflow"
```
Format: `- [ ] Data files: {OK / FAIL — one or more ADS data files missing; run scripts/fetch_ads_publications.py and siblings, or trigger update-ads-publications workflow}`
