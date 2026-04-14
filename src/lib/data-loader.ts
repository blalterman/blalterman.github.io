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

/**
 * Loads all publications by merging ADS-indexed and non-ADS publications.
 * Non-ADS publications (conferences without ADS bibcodes, Zenodo white papers, etc.)
 * are stored separately so the weekly ADS fetch doesn't overwrite them.
 */
export function loadAllPublications<T>(): T[] {
  const ads = loadJSONData<T[]>('ads_publications.json');
  const nonAds = loadJSONData<T[]>('non_ads_publications.json');
  return [...ads, ...nonAds];
}
