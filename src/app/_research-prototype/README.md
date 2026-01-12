# Research Prototype Pages (Disabled)

This folder contains prototype research topic pages with rich figure summaries and cross-topic navigation.

## Why the Underscore Prefix?

The `_` prefix tells Next.js App Router to **ignore this folder for routing**. This means:
- Code remains version-controlled and reviewable
- No routes are generated during build
- Production builds succeed even with all topics set to `published: false`

## Current Status

All 9 research topics have `published: false` in their JSON files at `/public/data/research-topics/`. The prototype pages are not ready for production.

## To Re-Enable

1. Rename this folder from `_research-prototype` to `research-prototype`
2. Set at least one topic to `published: true` in its JSON file
3. Rebuild and deploy

## Topics Included

- Sources of the Solar Wind
- Helium Abundance
- Solar Activity
- Heavy Ion Composition
- Solar Wind Compressibility
- Space Weather
- Suprathermal Ions
- Alfven Waves
- Coulomb Collisions

## Technical Notes

- Dynamic route at `[slug]/page.tsx` uses `generateStaticParams()` for static export
- `filterPublishedProjects()` controls which topics appear in production vs development
- Set `dynamicParams = false` to prevent 404s for unpublished slugs
