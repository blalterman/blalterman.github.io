import fs from 'fs';
import path from 'path';

/**
 * Reads and parses a JSON file from the public/data directory.
 * @param fileName The name of the JSON file to load (e.g., 'education.json').
 * @returns The parsed JSON data.
 */
export function loadJSONData<T>(fileName: string): T {
  const filePath = path.join(process.cwd(), 'public', 'data', fileName);
  const fileContents = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(fileContents);
}

/** One entry of the curated self-hosted-PDF registry (public/data/publication-pdfs.json). */
interface PublicationPdf {
  /** Root-absolute path to the PDF under public/ (e.g. "/papers/pdfs/2018ApJ_864_112A.pdf"). */
  path: string;
  /** Which version is hosted. */
  version: 'vor' | 'preprint' | 'thesis';
  /** Human-readable license/provenance note (not rendered). */
  license: string;
  /** Where the file was sourced from (research-corpus | zotero | unpaywall | arxiv). */
  source: string;
}

/**
 * Loads all publications by merging ADS-indexed and non-ADS publications, then
 * joins in self-hosted PDF info from publication-pdfs.json (keyed by bibcode).
 *
 * The PDF registry is curated and lives outside ads_publications.json, which the
 * weekly ADS fetch overwrites wholesale; storing pdf paths there would be wiped.
 * Bibcodes can also change on that weekly refresh, which would silently orphan a
 * registry entry, so every registry key is checked against the loaded set and an
 * orphan is surfaced loudly rather than dropping a Download button without a trace.
 */
export function loadAllPublications<T extends { bibcode: string }>(): T[] {
  const ads = loadJSONData<T[]>('ads_publications.json');
  const nonAds = loadJSONData<T[]>('non_ads_publications.json');
  const pdfs = loadJSONData<Record<string, PublicationPdf>>('publication-pdfs.json');
  const merged = [...ads, ...nonAds];

  // Positive control: every registry key must match a loaded publication.
  const bibcodes = new Set(merged.map((p) => p.bibcode));
  for (const key of Object.keys(pdfs)) {
    if (!bibcodes.has(key)) {
      console.warn(
        `[publication-pdfs] orphan registry key "${key}" matches no publication (bibcode may have changed on the weekly ADS refresh)`
      );
    }
  }

  return merged.map((p) => {
    const pdf = pdfs[p.bibcode];
    return pdf ? { ...p, pdfPath: pdf.path, pdfVersion: pdf.version } : p;
  });
}
