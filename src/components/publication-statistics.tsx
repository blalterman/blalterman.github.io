interface PublicationStatisticsProps {
  adsMetrics: any;
}

/**
 * Displays publication statistics from NASA ADS metrics.
 * Shows h-index, total papers, citations, and refereed publications.
 */
export function PublicationStatistics({ adsMetrics }: PublicationStatisticsProps) {
  return (
    <div className="flex justify-center flex-wrap gap-x-8 mb-12">
      <div className="flex flex-col items-center">
        <span className="text-2xl font-bold">{adsMetrics["indicators"]["h"]}</span>
        <span className="text-sm text-muted-foreground">h-index</span>
      </div>
      <div className="flex flex-col items-center">
        <span className="text-2xl font-bold">{adsMetrics["basic stats"]["number of papers"]}</span>
        <span className="text-sm text-muted-foreground">Total papers</span>
      </div>
      <div className="flex flex-col items-center">
        <span className="text-2xl font-bold">{adsMetrics["citation stats"]["total number of citations"]}</span>
        <span className="text-sm text-muted-foreground">Total citations</span>
      </div>
      <div className="flex flex-col items-center">
        <span className="text-2xl font-bold">{adsMetrics["basic stats refereed"]["number of papers"]}</span>
        <span className="text-sm text-muted-foreground">Refereed papers</span>
      </div>
      <div className="flex flex-col items-center">
        <span className="text-2xl font-bold">{adsMetrics["citation stats refereed"]["total number of citations"]}</span>
        <span className="text-sm text-muted-foreground">Refereed citations</span>
      </div>
    </div>
  );
}
