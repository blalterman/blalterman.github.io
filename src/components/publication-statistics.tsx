'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import { useTheme } from 'next-themes'
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog'
import { ChevronLeft, ChevronRight, TrendingUp } from 'lucide-react'

interface PublicationStatisticsProps {
  stats: any;
}

const PLOTS = [
  {
    src: 'publications_timeline',
    alt: 'Cumulative publications showing total refereed articles, conference contributions, and other publications from 2014-2025',
    title: 'Cumulative Publications',
  },
  {
    src: 'citations_by_year',
    alt: 'Cumulative citations showing total refereed and non-refereed citations from 2018-2026',
    title: 'Cumulative Citations',
  },
  {
    src: 'h_index_timeline',
    alt: 'h-index timeline showing growth from 2014 to 2025',
    title: 'H-Index Timeline',
  },
] as const

const METRIC_TO_PLOT_INDEX = {
  h_index: 2,
  total_papers: 0,
  total_citations: 1,
  refereed_papers: 0,
  refereed_citations: 1,
  invited_total: 0,
} as const

/**
 * Displays publication statistics from NASA ADS metrics.
 * Shows h-index, total papers, citations, and refereed publications.
 */
export function PublicationStatistics({ stats }: PublicationStatisticsProps) {
  const { resolvedTheme } = useTheme()
  const plotSuffix = resolvedTheme === 'dark' ? '_dark' : ''

  const [currentPlotIndex, setCurrentPlotIndex] = useState<number | null>(null)

  useEffect(() => {
    if (currentPlotIndex === null) return
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft') {
        setCurrentPlotIndex((i) => (i === null ? null : (i - 1 + PLOTS.length) % PLOTS.length))
      } else if (e.key === 'ArrowRight') {
        setCurrentPlotIndex((i) => (i === null ? null : (i + 1) % PLOTS.length))
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [currentPlotIndex])

  const ClickableMetric = ({
    value,
    label,
    onClick,
  }: {
    value: string | number
    label: React.ReactNode
    onClick: () => void
  }) => (
    <button
      onClick={onClick}
      className="flex flex-col items-center cursor-pointer transition-all duration-200 hover:scale-105 hover:opacity-80 rounded-lg p-2 md:p-3 hover:bg-accent/50 group"
      aria-label={`View ${typeof label === 'string' ? label.toLowerCase() : 'metric'} timeline`}
    >
      <span className="text-xl md:text-2xl font-bold">{value}</span>
      <span className="text-xs md:text-sm text-muted-foreground group-hover:text-foreground transition-colors text-center">
        {label}
      </span>
      <TrendingUp className="h-3 w-3 mt-1 opacity-0 group-hover:opacity-100 transition-opacity text-primary" />
    </button>
  )

  return (
    <>
      <div className="flex justify-center flex-wrap gap-x-4 md:gap-x-8 mb-12">
        <ClickableMetric
          value={stats.summary.h_index}
          label="H-Index"
          onClick={() => setCurrentPlotIndex(METRIC_TO_PLOT_INDEX.h_index)}
        />

        <ClickableMetric
          value={stats.summary.total_papers}
          label={<>Total<br />Papers</>}
          onClick={() => setCurrentPlotIndex(METRIC_TO_PLOT_INDEX.total_papers)}
        />

        <ClickableMetric
          value={stats.summary.total_citations}
          label={<>Total<br />Citations</>}
          onClick={() => setCurrentPlotIndex(METRIC_TO_PLOT_INDEX.total_citations)}
        />

        <ClickableMetric
          value={stats.summary.refereed_papers}
          label={<>Refereed<br />Papers</>}
          onClick={() => setCurrentPlotIndex(METRIC_TO_PLOT_INDEX.refereed_papers)}
        />

        <ClickableMetric
          value={stats.summary.refereed_citations}
          label={<>Refereed<br />Citations</>}
          onClick={() => setCurrentPlotIndex(METRIC_TO_PLOT_INDEX.refereed_citations)}
        />

        <ClickableMetric
          value={stats.summary.invited_total}
          label={<>Invited<br />Presentations</>}
          onClick={() => setCurrentPlotIndex(METRIC_TO_PLOT_INDEX.invited_total)}
        />
      </div>

      <Dialog open={currentPlotIndex !== null} onOpenChange={(open) => { if (!open) setCurrentPlotIndex(null) }}>
        <DialogContent
          className="w-[95vw] max-w-[min(896px,calc((90vh-4rem)*10/7))] max-h-[90vh]"
          onOpenAutoFocus={(e) => e.preventDefault()}
        >
          <DialogTitle className="sr-only">
            {currentPlotIndex !== null ? PLOTS[currentPlotIndex].title : ''}
          </DialogTitle>
          {currentPlotIndex !== null && (
            <>
              <div className="relative w-full aspect-[10/7]">
                <Image
                  src={`/plots/${PLOTS[currentPlotIndex].src}${plotSuffix}.svg`}
                  alt={PLOTS[currentPlotIndex].alt}
                  fill
                  className="object-contain"
                  priority
                />
              </div>
              <button
                onClick={() => setCurrentPlotIndex((i) => (i === null ? null : (i - 1 + PLOTS.length) % PLOTS.length))}
                aria-label="Previous plot"
                className="absolute -left-12 top-1/2 -translate-y-1/2 rounded-full bg-background/90 hover:bg-background p-2 shadow-md border focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>
              <button
                onClick={() => setCurrentPlotIndex((i) => (i === null ? null : (i + 1) % PLOTS.length))}
                aria-label="Next plot"
                className="absolute -right-12 top-1/2 -translate-y-1/2 rounded-full bg-background/90 hover:bg-background p-2 shadow-md border focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </>
          )}
        </DialogContent>
      </Dialog>
    </>
  )
}
