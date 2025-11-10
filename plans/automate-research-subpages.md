# Automation Plan for Research Subpage Generation

## Current Manual Process
1. Add entry to `research-projects.json` (page metadata)
2. Add entry to `page-figure-mappings.json` (figure assignment)
3. Add entry to `research-paragraphs.json` (content)
4. **Manually create** `/src/app/research/[slug]/page.tsx` file

## Recommended Solution: Dynamic Route with Static Generation

**Replace all individual page files with a single dynamic route:**

Create `/src/app/research/[slug]/page.tsx`:
```typescript
import { loadJSONData } from '@/lib/data-loader';
import { ResearchFigure } from '@/components/research-figure';

export async function generateStaticParams() {
  const projects = loadJSONData<any[]>('research-projects.json');
  return projects.map((project) => ({
    slug: project.slug,
  }));
}

export default function ResearchPage({ params }: { params: { slug: string } }) {
  const { slug } = params;

  const projects = loadJSONData<any[]>('research-projects.json');
  const project = projects.find((p: any) => p.slug === slug);
  const paragraphs = loadJSONData<Record<string, string>>('research-paragraphs.json');
  const figuresData = loadJSONData<any[]>('research-figures-with-captions.json');

  const pageData = figuresData.find((p: any) => p.slug === slug);
  const introductoryParagraph = paragraphs[slug];
  const figure = pageData?.figure;

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24">
      <h1 className="font-headline">{project?.title}</h1>
      <p className="text-lg text-muted-foreground mt-4">
        {introductoryParagraph}
      </p>
      {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
    </main>
  );
}
```

## How It Works with Static Export

1. **Build Time**: `generateStaticParams()` reads `research-projects.json`
2. **Page Generation**: Creates static HTML for each slug: `/research/proton-beams.html`, etc.
3. **Deployment**: Fully static files served by GitHub Pages

## Benefits After Implementation

**Adding a new research page becomes:**
1. Add to `research-projects.json` ✅
2. Add to `page-figure-mappings.json` ✅
3. Add to `research-paragraphs.json` ✅
4. **Push changes** → Page automatically exists! ✅

**No more manual React file creation needed.**

## Implementation Steps

1. **Create dynamic route file** with the code above
2. **Delete 8 individual page files**:
   - `/src/app/research/proton-beams/page.tsx`
   - `/src/app/research/helium-abundance/page.tsx`
   - `/src/app/research/sources-of-the-solar-wind/page.tsx`
   - `/src/app/research/heavy-ion-composition/page.tsx`
   - `/src/app/research/coulomb-collisions/page.tsx`
   - `/src/app/research/suprathermal-ions/page.tsx`
   - `/src/app/research/space-weather/page.tsx`
   - `/src/app/research/turbulence/page.tsx`
3. **Test build** to ensure all pages generate correctly
4. **Deploy** and verify all URLs work

## Why This Works for Static Sites

**Build Process:**
```
1. Read research-projects.json
2. Find slugs: [proton-beams, helium-abundance, ...]
3. For each slug:
   - Run ResearchPage component
   - Generate static HTML
   - Save as /research/[slug].html
4. Deploy static files to GitHub Pages
```

**Key Insight**: Dynamic routes in Next.js App Router with `generateStaticParams()` are designed specifically for static generation. They don't create dynamic server-side pages - they generate static HTML files at build time based on your data.

## Files That Would Change

### New File
- `/src/app/research/[slug]/page.tsx` - Single dynamic route template

### Deleted Files (8 total)
- All individual research page files in `/src/app/research/*/page.tsx`

### No Changes Needed
- Data files remain the same
- Components remain the same
- Build process remains the same
- GitHub Actions remain the same

## Result

This would make the website truly data-driven where new research topics can be added by simply updating JSON files, with no TypeScript/React development required.

The automation eliminates Step 4 (manual React file creation) while maintaining all current functionality and preserving the static site generation requirement.