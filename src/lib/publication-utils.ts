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
 * Removes parenthetical content from a string
 * @param text - Text that may contain parenthetical content
 * @returns Text with all parenthetical content removed
 * @example stripParenthetical("Yaireska (Yari)") // "Yaireska"
 * @example stripParenthetical("John (Jack) Smith") // "John Smith"
 */
function stripParenthetical(text: string): string {
  // Remove all content within parentheses, including the parentheses
  // Handles multiple occurrences: "John (Jack) (Johnny)" → "John"
  return text.replace(/\s*\([^)]*\)\s*/g, ' ').trim();
}

/**
 * Converts a name component to initial format with period
 * @param name - Name part (full name like "Yeimy" or initial like "B.")
 * @returns Initial with period (e.g., "Yeimy" → "Y.", "B." → "B.")
 */
function toInitial(name: string): string {
  const trimmed = name.trim();

  // Already an initial with period
  if (trimmed.endsWith('.')) {
    return trimmed;
  }

  // Single letter without period
  if (trimmed.length === 1) {
    return `${trimmed}.`;
  }

  // Full name - extract first letter
  return `${trimmed.charAt(0).toUpperCase()}.`;
}

/**
 * Transforms author name from ADS format to initials-only display format
 * @param adsName - Author name in ADS format: "LastName, FirstName(s)/Initials"
 * @returns Display format: "Initials LastName"
 * @example formatAuthorName("Rivera, Yeimy J.") // "Y. J. Rivera"
 * @example formatAuthorName("Alterman, B. L.") // "B. L. Alterman"
 * @example formatAuthorName("Del Zanna, Giulio") // "G. Del Zanna"
 */
export function formatAuthorName(adsName: string): string {
  const cleaned = adsName.trim();
  const parts = cleaned.split(',').map(p => p.trim());

  if (parts.length === 1) {
    return cleaned; // Already formatted or mononym
  }

  if (parts.length === 2) {
    // Standard: "LastName, FirstName/Initials MiddleInitial"
    const [lastName, firstNames] = parts;

    // Strip parenthetical content: "Yaireska (Yari)" → "Yaireska"
    const cleanedFirstNames = stripParenthetical(firstNames);

    // Split first names by whitespace: "Yeimy J." → ["Yeimy", "J."]
    const nameComponents = cleanedFirstNames.split(/\s+/).filter(n => n.length > 0);

    // Convert each component to initial: ["Yeimy", "J."] → ["Y.", "J."]
    const initials = nameComponents.map(toInitial).join(' ');

    return `${initials} ${lastName}`;
  }

  if (parts.length === 3) {
    // With suffix: "LastName, Suffix, FirstName/Initials MiddleInitial"
    const [lastName, suffix, firstNames] = parts;

    // Strip parenthetical content: "Yaireska (Yari)" → "Yaireska"
    const cleanedFirstNames = stripParenthetical(firstNames);

    // Split and convert to initials
    const nameComponents = cleanedFirstNames.split(/\s+/).filter(n => n.length > 0);
    const initials = nameComponents.map(toInitial).join(' ');

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

/**
 * Filter publications by invited status.
 *
 * @param publications Array of publications to filter
 * @param invited Filter for invited (true) or contributed (false)
 * @returns Filtered publications
 */
export function filterPublicationsByInvited(
  publications: Publication[],
  invited: boolean
): Publication[] {
  return publications.filter(pub => pub.invited === invited);
}

/**
 * Get invited publications of a specific type, sorted by date.
 * Convenience function combining type and invited filtering.
 *
 * @param publications Array of all publications
 * @param type Publication type(s) to filter by
 * @param order Sort order ('desc' for newest first, 'asc' for oldest first)
 * @returns Filtered and sorted invited publications
 */
export function getInvitedPublications(
  publications: Publication[],
  type: string | string[],
  order: 'desc' | 'asc' = 'desc'
): Publication[] {
  return sortPublicationsByDate(
    filterPublicationsByInvited(
      filterPublicationsByType(publications, type),
      true
    ),
    order
  );
}

/**
 * Filter publications by keywords field.
 * Used to distinguish conference talks ("invited") from seminars ("invitedother").
 *
 * @param publications Array of publications to filter
 * @param keywords Keywords value to filter by
 * @returns Filtered publications
 */
export function filterPublicationsByKeywords(
  publications: Publication[],
  keywords: string
): Publication[] {
  return publications.filter(pub => pub.keywords === keywords);
}

/**
 * Get seminar/colloquium presentations (keywords: "invitedother").
 * These are institution visits, department seminars, specialist talks.
 * Does NOT include conference presentations (even if invited).
 *
 * @param publications Array of all publications
 * @param order Sort order ('desc' for newest first, 'asc' for oldest first)
 * @returns Filtered and sorted seminar presentations
 */
export function getSeminarPresentations(
  publications: Publication[],
  order: 'desc' | 'asc' = 'desc'
): Publication[] {
  return sortPublicationsByDate(
    filterPublicationsByKeywords(publications, 'invitedother'),
    order
  );
}

/**
 * Decode HTML entities in text (e.g., &amp; → &, &lt; → <).
 *
 * Handles common HTML entities returned by ADS API in publication titles.
 * Uses browser's DOMParser for accurate decoding.
 *
 * @param text Text containing HTML entities
 * @returns Decoded text with entities replaced by actual characters
 *
 * @example
 * decodeHtmlEntities("Solar &amp; Space Physics") // "Solar & Space Physics"
 * decodeHtmlEntities("E &lt; 10 keV") // "E < 10 keV"
 */
export function decodeHtmlEntities(text: string): string {
  if (typeof window === 'undefined') {
    // Server-side: use regex-based decoding for common entities
    return text
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&nbsp;/g, ' ');
  }

  // Client-side: use DOMParser for complete entity decoding
  const parser = new DOMParser();
  const doc = parser.parseFromString(text, 'text/html');
  return doc.documentElement.textContent || text;
}