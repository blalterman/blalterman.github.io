import type { Publication } from '@/types/publication';

/**
 * Sort publications by date in chronological order.
 *
 * @param publications Array of publications to sort
 * @param order Sort order: 'desc' for newest first, 'asc' for oldest first
 * @returns New array of publications sorted by date
 */
export function sortPublicationsByDate(
  publications: Publication[],
  order: 'desc' | 'asc' = 'desc'
): Publication[] {
  return [...publications].sort((a, b) => {
    // Use full date string comparison for proper chronological order
    const comparison = b.year.localeCompare(a.year);
    return order === 'desc' ? comparison : -comparison;
  });
}

/**
 * Filter publications by publication type.
 * Supports both single type (string) and multiple types (array).
 *
 * @param publications Array of publications to filter
 * @param type Publication type(s) to filter by
 * @returns New array containing only publications of the specified type(s)
 */
export function filterPublicationsByType(
  publications: Publication[],
  type: string | string[]
): Publication[] {
  const types = Array.isArray(type) ? type : [type];
  return publications.filter(pub => types.includes(pub.publication_type));
}

/**
 * Get publications of a specific type, sorted by date.
 * Combines filtering and sorting in a single operation.
 * Supports both single type (string) and multiple types (array).
 *
 * @param publications Array of publications to process
 * @param type Publication type(s) to filter by
 * @param order Sort order: 'desc' for newest first, 'asc' for oldest first
 * @returns New array of filtered and sorted publications
 */
export function getPublicationsByType(
  publications: Publication[],
  type: string | string[],
  order: 'desc' | 'asc' = 'desc'
): Publication[] {
  return sortPublicationsByDate(
    filterPublicationsByType(publications, type),
    order
  );
}

/**
 * Sort publications by citation count.
 *
 * @param publications Array of publications to sort
 * @param order Sort order: 'desc' for most cited first, 'asc' for least cited first
 * @returns New array of publications sorted by citation count
 */
export function sortPublicationsByCitations(
  publications: Publication[],
  order: 'desc' | 'asc' = 'desc'
): Publication[] {
  return [...publications].sort((a, b) => {
    const comparison = b.citations - a.citations;
    return order === 'desc' ? comparison : -comparison;
  });
}

/**
 * Check if a publication is first-authored by Alterman.
 * Handles both "Alterman, B. L." and "B. L. Alterman" formats.
 *
 * @param publication Publication to check
 * @returns True if Alterman is the first author
 */
export function isFirstAuthor(publication: Publication): boolean {
  const firstAuthor = publication.authors[0]?.toLowerCase() || '';
  return firstAuthor.includes('alterman');
}

/**
 * Extract unique journal names from publications.
 *
 * @param publications Array of publications
 * @returns Sorted array of unique journal names
 */
export function extractUniqueJournals(publications: Publication[]): string[] {
  return Array.from(new Set(publications.map(p => p.journal))).sort();
}

/**
 * Extract unique years from publications.
 *
 * @param publications Array of publications
 * @returns Array of unique years sorted newest first
 */
export function extractUniqueYears(publications: Publication[]): string[] {
  return Array.from(
    new Set(publications.map(p => p.year.substring(0, 4)))
  )
    .sort()
    .reverse();
}

/**
 * Transforms author name from ADS format to display format
 * @param adsName - Author name in ADS format: "LastName, F. M."
 * @returns Display format: "F. M. LastName"
 * @example formatAuthorName("Alterman, B. L.") // "B. L. Alterman"
 */
export function formatAuthorName(adsName: string): string {
  const cleaned = adsName.trim();
  const parts = cleaned.split(',').map(p => p.trim());

  if (parts.length === 1) {
    return cleaned; // Already formatted or single name
  }

  if (parts.length === 2) {
    // Standard: "LastName, Initials" → "Initials LastName"
    const [lastName, initials] = parts;
    return `${initials} ${lastName}`;
  }

  if (parts.length === 3) {
    // With suffix: "LastName, Suffix, Initials" → "Initials LastName, Suffix"
    const [lastName, suffix, initials] = parts;
    return `${initials} ${lastName}, ${suffix}`;
  }

  // Fallback for unexpected formats
  console.warn(`Unexpected author name format: ${adsName}`);
  return cleaned;
}

/**
 * Transforms array of ADS-formatted author names to display format
 * @param adsAuthors - Array of author names in ADS format
 * @returns Array of author names in display format
 */
export function formatAuthorNames(adsAuthors: string[]): string[] {
  return adsAuthors.map(formatAuthorName);
}

/**
 * Checks if an author name matches B. L. Alterman (format-agnostic)
 * @param authorName - Author name in any format
 * @returns True if author is B. L. Alterman
 */
export function isAlterman(authorName: string): boolean {
  const normalized = authorName.trim().toLowerCase();

  return (
    normalized === 'alterman, b. l.' ||
    normalized === 'b. l. alterman' ||
    normalized === 'alterman, b.l.' ||
    normalized === 'b.l. alterman'
  );
}