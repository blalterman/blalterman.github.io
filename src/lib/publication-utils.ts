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
 *
 * @param publications Array of publications to filter
 * @param type Publication type to filter by
 * @returns New array containing only publications of the specified type
 */
export function filterPublicationsByType(
  publications: Publication[],
  type: string
): Publication[] {
  return publications.filter(pub => pub.publication_type === type);
}

/**
 * Get publications of a specific type, sorted by date.
 * Combines filtering and sorting in a single operation.
 *
 * @param publications Array of publications to process
 * @param type Publication type to filter by
 * @param order Sort order: 'desc' for newest first, 'asc' for oldest first
 * @returns New array of filtered and sorted publications
 */
export function getPublicationsByType(
  publications: Publication[],
  type: string,
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