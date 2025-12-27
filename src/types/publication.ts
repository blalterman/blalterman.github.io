/**
 * Publication interface based on the structure of NASA ADS publication data.
 */
export interface Publication {
  /** NASA ADS bibcode identifier */
  bibcode: string;

  /** Publication title */
  title: string;

  /** List of authors (formatted as "Lastname, F. M.") */
  authors: string[];

  /** Publication year/month in format "YYYY-MM-DD" */
  year: string;

  /** Full month name (e.g., "February") or empty string */
  month: string;

  /** Journal or publication venue name */
  journal: string;

  /** Publication type (e.g., "article", "dataset", "inproceedings", etc.) */
  publication_type: string;

  /** Number of citations */
  citations: number;

  /** URL to the publication (DOI or NASA ADS link) */
  url: string;

  /** Whether this is an invited presentation/talk (optional during migration, will become required) */
  invited?: boolean;

  /** Publication keywords for categorization
   * - "invited" = invited conference talk
   * - "invitedother" = invited seminar/colloquium
   * - "public" = public lecture
   */
  keywords?: string;

  /** Venue/institution name for presentations */
  booktitle?: string;

  /** Geographic location (e.g., "Greenbelt, MD") */
  location?: string;

  /** Day of month (for presentations) */
  day?: string;

  /** Direct URL to invited talk announcement */
  invited_url?: string;
}