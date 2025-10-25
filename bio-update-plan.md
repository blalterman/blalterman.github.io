# Ben Page Implementation Plan

**Date Created:** 2025-10-25
**Goal:** Create a new "Ben" page to house biographical content, shortening the homepage to just the first 2 paragraphs.

---

## 1. Design Decisions Summary

### 1.1 Content Split
- **Homepage:** First 2 paragraphs only (the "big question" hook)
- **Ben Page:** Remaining 5 paragraphs split into 2 sections
- **No content duplication** between pages

### 1.2 Data Architecture
- **Approach:** Separate JSON files (Option B)
- **Files:**
  - `biography-homepage.json` - Homepage content
  - `ben-page.json` - Ben page sections
- **Rationale:** Zero overlap eliminates duplication concerns, follows existing site pattern

### 1.3 Homepage Changes
- **CTA Type:** Option 3 - Inline sentence link
- **CTA Text:** "Want to learn more about my research vision and team philosophy? Read my full story."
- **Link destination:** `/ben`

### 1.4 Ben Page Design
- **Layout:** Option B - Card-based sections with icons
- **Page heading:** "Ben"
- **Tagline:** "How I ask big questions and who I ask them with"
- **Navigation placement:** `Home | Ben | Research | Publications | Experience | Contact`

### 1.5 Visual Design
- **Section 1:** "Research Vision" with Telescope icon
- **Section 2:** "How I Build Teams" with Compass icon
- **Pattern:** Follows Experience page card layout
- **Container:** Cards with shadow, icons in headers

---

## 2. Data Files to Create

### 2.1 Create `/public/data/biography-homepage.json`

```json
{
  "heading": "Academic. Researcher. Explorer.",
  "tagline": "Exploring the Solar Wind to Understand Our Place in the Cosmos",
  "paragraphs": [
    "Since humans first looked to the stars, we have asked, \"Are we alone?\"",
    "The closest exoplanet to Earth, Proxima Centauri b, is 4.2 light-years away. Riding the fastest spaceship humans have ever built, it would take us over 6600 years—over 200 generations—to travel there. With current technology, no expedition would survive that journey. So how can we know if there is other life in the universe? By studying how a star sustains life on the one planet we are certain it exists."
  ]
}
```

### 2.2 Create `/public/data/ben-page.json`

```json
{
  "sections": [
    {
      "heading": "Research Vision",
      "icon": "Telescope",
      "paragraphs": [
        "I do this by studying the Sun and solar wind, the stream of charged particles it continuously emits, on timescales from seconds to decades to discover what it means for a Sun to create a habitable zone and to power life on Earth. I blend deep curiosity, creativity, and discipline to ask novel questions that push us beyond the edge of our current understanding. This builds transformative insights that reshape how we live here and now.",
        "No single instrument or single person can accomplish this task alone. We need highly specialized instruments that can observe a range of phenomena over timescales that can exceed any single instrument's lifetime and one person's career. The questions we ask and the challenges we face demand that we work together to achieve our goals. Only cohesive teams can do this well."
      ]
    },
    {
      "heading": "How I Build Teams",
      "icon": "Compass",
      "paragraphs": [
        "I build high-trust teams where questions are celebrated and ownership is real, creating the psychological safety necessary to ask big questions and take the risks required to answer them. This requires a subtle combination of independence and interdependence. We must be able to work on our own while simultaneously leaning on and collaborating with each other. This combination gives us the freedom to be creative, effective, and impactful as we drive results and push the bounds of human knowledge. In such environments, conflict is inevitable. By taking an us-against-the-problem approach, we put the problem on the wall and argue evidence, not intention, so teams leverage conflict as a tool to push us all forward and build beyond our individual visions. This turns team culture into a performance system that drives achievement and delivery while simultaneously fostering safety, care, and overall well-being.",
        "Teams of this caliber require strong principles, values, and practices to succeed. My principles are integrity, transparency, empathy, curiosity, rigor, and gratitude. They show up as concrete habits: we cross-check evidence across missions so insights cohere; we write plainly and explain choices; we archive code and methods with each result; each milestone has a directly responsible individual; weekly check-ins keep momentum; monthly \"unlock\" milestones ensure near-term wins open the larger architecture. We take high-impact, disciplined risks when we envision a clear path to delivery, even when others don't. We learn in public, testing, extracting lessons, and adapting quickly. This cadence transforms research and exploration into outcomes that drive real-world change.",
        "Today, we are building a new understanding of how the solar wind's helium abundance varies with the solar cycle, providing deep and nuanced insight into how helium impacts the solar wind's birth. These results also redefine how we understand the solar cycle and forecast its effects by separating two previously coupled problems: timing and amplitude of the solar cycle. This result strengthens solar cycle forecasts, improving our ability to safeguard human life and technology on Earth and in space."
      ]
    }
  ]
}
```

---

## 3. New Page Component

### 3.1 Create `/src/app/ben/page.tsx`

```typescript
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Telescope, Compass } from "lucide-react";
import { loadJSONData } from "@/lib/data-loader";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Ben | B. L. Alterman",
    description: "Learn about Ben Alterman's research vision and team-building philosophy.",
};

interface BenSection {
    heading: string;
    icon: string;
    paragraphs: string[];
}

interface BenPageData {
    sections: BenSection[];
}

const iconMap = {
    Telescope: Telescope,
    Compass: Compass,
};

export default function BenPage() {
    const benData = loadJSONData<BenPageData>('ben-page.json');

    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <div className="text-center mb-12">
                <h1 className="font-headline">Ben</h1>
                <p className="text-lg text-muted-foreground mt-2">
                    How I ask big questions and who I ask them with
                </p>
            </div>

            <div className="max-w-4xl mx-auto space-y-8">
                {benData.sections.map((section) => {
                    const IconComponent = iconMap[section.icon as keyof typeof iconMap];

                    return (
                        <Card key={section.heading} className="shadow-lg">
                            <CardHeader>
                                <CardTitle className="flex items-center text-2xl">
                                    {IconComponent && <IconComponent className="mr-3 h-6 w-6 text-primary" />}
                                    {section.heading}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {section.paragraphs.map((paragraph, index) => (
                                    <p key={index} className="text-lg text-muted-foreground">
                                        {paragraph}
                                    </p>
                                ))}
                            </CardContent>
                        </Card>
                    );
                })}
            </div>
        </main>
    );
}
```

---

## 4. Component Modifications

### 4.1 Update `/src/app/page.tsx`

**Current code (lines 6-13):**
```typescript
interface BiographyData {
  heading: string;
  tagline: string;
  paragraphs: string[];
}

export default function Home() {
  const biographyData = loadJSONData<BiographyData>('biography.json');
```

**Change to:**
```typescript
interface BiographyData {
  heading: string;
  tagline: string;
  paragraphs: string[];
}

export default function Home() {
  const biographyData = loadJSONData<BiographyData>('biography-homepage.json');
```

**Action:** Change `'biography.json'` to `'biography-homepage.json'` on line 13.

---

### 4.2 Update `/src/components/about.tsx`

**Add import at top (after line 3):**
```typescript
import Link from 'next/link';
```

**Add CTA after paragraphs (after line 36, before closing div on line 37):**
```typescript
          <p className="text-lg text-muted-foreground mt-4">
            Want to learn more about my research vision and team philosophy?{' '}
            <Link href="/ben" className="text-primary hover:underline font-medium">
              Read my full story
            </Link>.
          </p>
```

**Complete modified section (lines 25-38):**
```typescript
        <div className="md:col-span-2 space-y-4">
          <h1 className="text-3xl md:text-5xl font-bold font-headline tracking-tighter">
            {biographyData.heading}
          </h1>
          <p className="text-xl md:text-2xl text-primary font-light">
            {biographyData.tagline}
          </p>
          {biographyData.paragraphs.map((paragraph, index) => (
            <p key={index} className="text-lg text-muted-foreground">
              {paragraph}
            </p>
          ))}
          <p className="text-lg text-muted-foreground mt-4">
            Want to learn more about my research vision and team philosophy?{' '}
            <Link href="/ben" className="text-primary hover:underline font-medium">
              Read my full story
            </Link>.
          </p>
        </div>
```

---

### 4.3 Update `/src/components/header.tsx`

**Add "Ben" link after "Home" (line 22, before Research link):**

**Current code (lines 21-26):**
```typescript
          <nav className="hidden items-center space-x-6 text-sm font-medium md:flex">
            <Link href="/research" className="transition-colors hover:text-foreground/80 text-foreground/60">Research</Link>
            <Link href="/publications" className="transition-colors hover:text-foreground/80 text-foreground/60">Publications</Link>
            <Link href="/experience" className="transition-colors hover:text-foreground/80 text-foreground/60">Experience</Link>
            <Link href="/#contact" className="transition-colors hover:text-foreground/80 text-foreground/60">Contact</Link>
          </nav>
```

**Change to:**
```typescript
          <nav className="hidden items-center space-x-6 text-sm font-medium md:flex">
            <Link href="/ben" className="transition-colors hover:text-foreground/80 text-foreground/60">Ben</Link>
            <Link href="/research" className="transition-colors hover:text-foreground/80 text-foreground/60">Research</Link>
            <Link href="/publications" className="transition-colors hover:text-foreground/80 text-foreground/60">Publications</Link>
            <Link href="/experience" className="transition-colors hover:text-foreground/80 text-foreground/60">Experience</Link>
            <Link href="/#contact" className="transition-colors hover:text-foreground/80 text-foreground/60">Contact</Link>
          </nav>
```

---

### 4.4 Update `/src/components/mobile-nav.tsx`

**Add "Ben" link in mobile menu (after line 36):**

**Current code (lines 36-48):**
```typescript
            <div className="grid gap-2 py-6">
              <Link href="/research" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Research
              </Link>
              <Link href="/publications" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Publications
              </Link>
              <Link href="/experience" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Experience
              </Link>
              <Link href="/#contact" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Contact
              </Link>
            </div>
```

**Change to:**
```typescript
            <div className="grid gap-2 py-6">
              <Link href="/ben" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Ben
              </Link>
              <Link href="/research" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Research
              </Link>
              <Link href="/publications" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Publications
              </Link>
              <Link href="/experience" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Experience
              </Link>
              <Link href="/#contact" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Contact
              </Link>
            </div>
```

---

## 5. File Cleanup

### 5.1 Archive or Delete `/public/data/biography.json`

**Action:** This file is no longer needed (replaced by `biography-homepage.json` and `ben-page.json`).

**Options:**
- Delete it entirely
- Move to `/public/data/archive/biography.json.backup`

**Recommendation:** Delete after confirming new implementation works correctly.

---

## 6. Implementation Steps (Numbered for Tracking)

### Step 1: Create Data Files
- [ ] 1a. Create `/public/data/biography-homepage.json` (see §2.1)
- [ ] 1b. Create `/public/data/ben-page.json` (see §2.2)

### Step 2: Create Ben Page
- [ ] 2a. Create directory `/src/app/ben/`
- [ ] 2b. Create `/src/app/ben/page.tsx` (see §3.1)

### Step 3: Update Homepage
- [ ] 3a. Update `/src/app/page.tsx` data source (see §4.1)
- [ ] 3b. Update `/src/components/about.tsx` - add import (see §4.2)
- [ ] 3c. Update `/src/components/about.tsx` - add CTA (see §4.2)

### Step 4: Update Navigation
- [ ] 4a. Update `/src/components/header.tsx` (see §4.3)
- [ ] 4b. Update `/src/components/mobile-nav.tsx` (see §4.4)

### Step 5: Testing
- [ ] 5a. Run `npm run dev` to start development server
- [ ] 5b. Verify homepage shows only 2 paragraphs
- [ ] 5c. Verify homepage CTA link appears and works
- [ ] 5d. Verify "Ben" appears in header navigation
- [ ] 5e. Verify "Ben" appears in mobile navigation
- [ ] 5f. Navigate to `/ben` and verify page renders
- [ ] 5g. Verify telescope icon appears in Research Vision card
- [ ] 5h. Verify compass icon appears in How I Build Teams card
- [ ] 5i. Verify all 5 paragraphs appear correctly in sections

### Step 6: Build & Type Check
- [ ] 6a. Run `npm run typecheck` - ensure no TypeScript errors
- [ ] 6b. Run `npm run build` - ensure production build succeeds
- [ ] 6c. Verify static export generates `/ben/index.html`

### Step 7: Cleanup
- [ ] 7a. Delete `/public/data/biography.json` (see §5.1)
- [ ] 7b. Commit changes with descriptive message

---

## 7. Testing Checklist

### Visual Verification
- [ ] Homepage headshot, heading, tagline display correctly
- [ ] Homepage shows exactly 2 paragraphs (not 7)
- [ ] CTA text reads: "Want to learn more about my research vision and team philosophy? Read my full story."
- [ ] "Read my full story" link is styled (primary color, underline on hover)
- [ ] Header navigation shows: Home | Ben | Research | Publications | Experience | Contact
- [ ] Mobile nav includes "Ben" link

### Ben Page Verification
- [ ] Page title is "Ben"
- [ ] Tagline reads: "How I ask big questions and who I ask them with"
- [ ] Two cards render with shadows
- [ ] Card 1: Telescope icon + "Research Vision" heading + 2 paragraphs
- [ ] Card 2: Compass icon + "How I Build Teams" heading + 3 paragraphs
- [ ] Icons are primary color, positioned left of headings
- [ ] Cards have proper spacing (space-y-8)
- [ ] Text is readable (text-lg, text-muted-foreground)

### Functional Verification
- [ ] Clicking "Read my full story" navigates to `/ben`
- [ ] Clicking "Ben" in nav navigates to `/ben`
- [ ] Browser back button works correctly
- [ ] Mobile navigation closes after clicking "Ben"
- [ ] Page metadata shows correct title: "Ben | B. L. Alterman"

### Build Verification
- [ ] `npm run typecheck` passes
- [ ] `npm run build` succeeds
- [ ] `/out/ben/index.html` exists
- [ ] No console errors in browser
- [ ] No 404 errors for data files

---

## 8. Rollback Plan

If issues arise, revert by:

1. **Restore original homepage:**
   - Change `/src/app/page.tsx` line 13 back to `'biography.json'`
   - Remove CTA from `/src/components/about.tsx`

2. **Remove Ben page:**
   - Delete `/src/app/ben/` directory
   - Remove "Ben" links from header and mobile nav

3. **Restore data:**
   - Delete `biography-homepage.json` and `ben-page.json`
   - Keep or restore original `biography.json`

---

## 9. Future Enhancements (Optional)

### Potential Improvements
- Add animations to cards (hover effects, transitions)
- Add social share metadata for Ben page
- Consider adding a "Back to Home" link at bottom of Ben page
- Add analytics tracking for Ben page visits
- Consider A/B testing different CTAs on homepage

### Content Updates
- Ben page content lives in `/public/data/ben-page.json`
- Homepage excerpt lives in `/public/data/biography-homepage.json`
- Edit JSON files directly - no code changes needed

---

## 10. Notes & Decisions Log

### Why Compass Icon?
- Represents "philosophy guides our work"
- More metaphorical depth than literal "Users" icon
- Pairs well with Telescope (explore + navigate)
- Aligns with content about principles, values, direction

### Why Separate JSON Files?
- Zero content duplication (paragraphs 1-2 only on homepage, 3-7 only on Ben page)
- Clear separation of concerns
- Follows existing site pattern (research-projects.json + research-paragraphs.json)
- Easier to maintain (edit homepage vs. Ben page independently)

### Why Card Layout?
- Follows Experience page pattern (consistency)
- Visual hierarchy helps scannability
- Icons add personality without overwhelming content
- Still highly readable for long-form text

### Tagline Synthesis
Selected from three favorites:
1. "Asking big questions and building the teams to answer them"
2. "How I explore and who I explore with"
3. "Asking big questions and building trusted teams"

Final: "How I ask big questions and who I ask them with"
- Combines "how/who" elegance with "big questions"
- Personal voice, natural flow
- Perfect match to dual-section structure

---

## Completed Steps

<!-- Append completed step numbers here as you progress -->
<!-- Example:
- Step 1a: Completed 2025-10-25
- Step 1b: Completed 2025-10-25
-->
