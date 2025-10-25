# Fix Plan: Render HTML Links in Research Paragraphs and Figure Captions

## Problem Analysis

### Problem 1: Research paragraph link doesn't render
- **Current:** `{introductoryParagraph}` renders as plain text
- **Result:** HTML tags like `<a href=...>` show literally on page
- **Fix:** Use `dangerouslySetInnerHTML` with `renderMathInText()` processing

### Problem 2: Escaped quotes breaking links
- **Current in JSON:** `<a href=\\"/research/helium-abundance\\">\\"saturation\\" speed</a>`
- **After JSON parse:** `<a href=\"/research/helium-abundance\">\"saturation\" speed</a>`
- **Result:** Backslash-escaped quotes create invalid HTML
- **Fix:** Remove extra backslashes - JSON only needs single escaping

## Solution Steps

### 1. Fix Research Paragraph Rendering (Code Change)
**File:** `src/app/research/[slug]/page.tsx`

Change line 47-49 from:
```typescript
<p className="text-lg text-muted-foreground mt-4">
    {introductoryParagraph}
</p>
```

To:
```typescript
<p
    className="text-lg text-muted-foreground mt-4"
    dangerouslySetInnerHTML={{ __html: renderMathInText(introductoryParagraph) }}
/>
```

Also add import at top:
```typescript
import { renderMathInText } from '@/lib/render-math';
```

### 2. Fix JSON Escaping (Data Changes)

**File:** `public/data/research-paragraphs.json`

Current (incorrect):
```json
"<a href=\\\"/research/helium-abundance\\\">\\\"saturation\\\" speed</a>"
```

Should be:
```json
"<a href=\"/research/helium-abundance\">\"saturation\" speed</a>"
```

**File:** `public/paper-figures/figure-metadata.json`

Current (incorrect):
```json
"<a href=\\\"/research/sources-of-the-solar-wind\\\">Sources of the Solar Wind</a>"
```

Should be:
```json
"<a href=\"/research/sources-of-the-solar-wind\">Sources of the Solar Wind</a>"
```

### 3. Rebuild and Test
- Validate JSON syntax
- Run `npm run build`
- Test links on affected pages

## Files Modified
1. `src/app/research/[slug]/page.tsx` - Add HTML rendering for paragraphs
2. `public/data/research-paragraphs.json` - Fix quote escaping
3. `public/paper-figures/figure-metadata.json` - Fix quote escaping

## Testing
- `/research/solar-wind-compressibility` - Check paragraph link to helium-abundance works
- `/research/solar-wind-compressibility` - Check figure caption links to sources-of-the-solar-wind and space-weather work

## Root Cause
The issue is that we're triple-escaping quotes in the JSON files:
1. JSON requires `\"` for a literal quote character
2. We added extra `\` thinking we needed more escaping
3. This creates `\\\"` which becomes `\"` after JSON parsing (backslash + quote instead of just quote)

The fix is to use standard JSON escaping only:
- `\"` for quote characters in HTML attributes and quoted text
- No triple or quadruple escaping needed
