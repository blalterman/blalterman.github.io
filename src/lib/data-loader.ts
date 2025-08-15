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
