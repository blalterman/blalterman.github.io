/**
 * Types for the new research topic data structure.
 * This supports rich summaries, multiple figures, and detailed metadata.
 */

export interface FigureSummary {
  what_we_see: string;
  the_finding: string;
  why_it_matters: string;
}

// ============================================
// Resolved types (after joining with registry)
// ============================================

export interface PrimaryFigure {
  paper_id: string;
  figure_id: string;
  src: string;
  short_title: string;
  alt: string;
  summary: FigureSummary;
  keywords: string[];
}

export interface RelatedFigure {
  paper_id: string;
  figure_id: string;
  src: string;
  short_title: string;
  alt: string;
  relevance: string;
  summary_short: string;
}

// ============================================
// Raw types (as stored in JSON files)
// ============================================

export interface PrimaryFigureRef {
  ref: string;  // "paper_id/figure_id"
  topic_keywords?: string[];  // Topic-specific keywords to merge
}

export interface RelatedFigureRef {
  ref: string;  // "paper_id/figure_id"
  relevance: string;  // Context-specific relevance
}

export interface RawResearchTopicData {
  slug: string;
  title: string;
  subtitle: string;
  description: string;
  primary_figure: PrimaryFigureRef;
  related_figures: RelatedFigureRef[];
  related_topics?: RelatedTopic[];
  published?: boolean;
  paper: PaperInfo;
}

// ============================================
// Figure Registry types
// ============================================

export interface FigureRegistryEntry {
  paper_id: string;
  figure_id: string;
  src: string;
  short_title: string;
  alt: string;
  summary: FigureSummary | null;
  summary_short: string | null;
  keywords: string[];
  used_as_primary_in?: string[];
  used_as_related_in?: string[];
}

export interface FigureRegistry {
  [key: string]: FigureRegistryEntry;  // key = "paper_id/figure_id"
}

export interface PaperInfo {
  id: string;
  title: string;
  doi: string;
  bibcode: string;
  journal: string;
  year: number;
  license: {
    holder: string;
    year: number;
    type: string;
  };
}

export interface RelatedTopic {
  slug: string;
  connection: string;
}

export interface ResearchTopicData {
  slug: string;
  title: string;
  subtitle: string;
  description: string;
  primary_figure: PrimaryFigure;
  related_figures: RelatedFigure[];
  related_topics?: RelatedTopic[];
  published?: boolean; // defaults to true if not specified
  paper: PaperInfo;
}
