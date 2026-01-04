/**
 * Types for the new research topic data structure.
 * This supports rich summaries, multiple figures, and detailed metadata.
 */

export interface FigureSummary {
  what_we_see: string;
  the_finding: string;
  why_it_matters: string;
}

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

export interface ResearchTopicData {
  slug: string;
  title: string;
  subtitle: string;
  description: string;
  primary_figure: PrimaryFigure;
  related_figures: RelatedFigure[];
  paper: PaperInfo;
}
