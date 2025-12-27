'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Dialog, DialogContent } from '@/components/ui/dialog'
import { TrendingUp } from 'lucide-react'

interface PublicationStatisticsProps {
  adsMetrics: any;
}

/**
 * Displays publication statistics from NASA ADS metrics.
 * Shows h-index, total papers, citations, and refereed publications.
 * Makes "Total papers" and "Total citations" clickable to view timeline plots in modals.
 */
export function PublicationStatistics({ adsMetrics }: PublicationStatisticsProps) {
  const [publicationsDialogOpen, setPublicationsDialogOpen] = useState(false)
  const [citationsDialogOpen, setCitationsDialogOpen] = useState(false)
  const [refereedPapersDialogOpen, setRefereedPapersDialogOpen] = useState(false)
  const [refereedCitationsDialogOpen, setRefereedCitationsDialogOpen] = useState(false)

  const ClickableMetric = ({
    value,
    label,
    onClick,
  }: {
    value: string | number
    label: string
    onClick: () => void
  }) => (
    <button
      onClick={onClick}
      className="flex flex-col items-center cursor-pointer transition-all duration-200 hover:scale-105 hover:opacity-80 rounded-lg p-3 hover:bg-accent/50 group"
      aria-label={`View ${label.toLowerCase()} timeline`}
    >
      <span className="text-2xl font-bold">{value}</span>
      <span className="text-sm text-muted-foreground group-hover:text-foreground transition-colors">
        {label}
      </span>
      <TrendingUp className="h-3 w-3 mt-1 opacity-0 group-hover:opacity-100 transition-opacity text-primary" />
    </button>
  )

  return (
    <>
      <div className="flex justify-center flex-wrap gap-x-8 mb-12">
        {/* Non-clickable: h-index */}
        <div className="flex flex-col items-center">
          <span className="text-2xl font-bold">{adsMetrics["indicators"]["h"]}</span>
          <span className="text-sm text-muted-foreground">h-index</span>
        </div>

        {/* CLICKABLE: Total papers → Publications Timeline */}
        <ClickableMetric
          value={adsMetrics["basic stats"]["number of papers"]}
          label="Total papers"
          onClick={() => setPublicationsDialogOpen(true)}
        />

        {/* CLICKABLE: Total citations → Citations Timeline */}
        <ClickableMetric
          value={adsMetrics["citation stats"]["total number of citations"]}
          label="Total citations"
          onClick={() => setCitationsDialogOpen(true)}
        />

        {/* CLICKABLE: Refereed papers → Publications Timeline */}
        <ClickableMetric
          value={adsMetrics["basic stats refereed"]["number of papers"]}
          label="Refereed papers"
          onClick={() => setRefereedPapersDialogOpen(true)}
        />

        {/* CLICKABLE: Refereed citations → Citations Timeline */}
        <ClickableMetric
          value={adsMetrics["citation stats refereed"]["total number of citations"]}
          label="Refereed citations"
          onClick={() => setRefereedCitationsDialogOpen(true)}
        />
      </div>

      {/* Publications Timeline Dialog */}
      <Dialog open={publicationsDialogOpen} onOpenChange={setPublicationsDialogOpen}>
        <DialogContent className="w-[95vw] max-w-[min(896px,calc((90vh-4rem)*10/7))] max-h-[90vh] overflow-hidden">
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/publications_timeline.svg"
              alt="Publications Timeline showing refereed articles, conference contributions, and other publications from 2014-2025"
              fill
              className="object-contain"
              priority
            />
          </div>
        </DialogContent>
      </Dialog>

      {/* Citations Timeline Dialog */}
      <Dialog open={citationsDialogOpen} onOpenChange={setCitationsDialogOpen}>
        <DialogContent className="w-[95vw] max-w-[min(896px,calc((90vh-4rem)*10/7))] max-h-[90vh] overflow-hidden">
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/citations_by_year.svg"
              alt="Citations Timeline showing refereed and non-refereed citations from 2018-2026"
              fill
              className="object-contain"
              priority
            />
          </div>
        </DialogContent>
      </Dialog>

      {/* Refereed Papers Timeline Dialog */}
      <Dialog open={refereedPapersDialogOpen} onOpenChange={setRefereedPapersDialogOpen}>
        <DialogContent className="w-[95vw] max-w-[min(896px,calc((90vh-4rem)*10/7))] max-h-[90vh] overflow-hidden">
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/publications_timeline.svg"
              alt="Publications Timeline showing refereed articles, conference contributions, and other publications from 2014-2025"
              fill
              className="object-contain"
              priority
            />
          </div>
        </DialogContent>
      </Dialog>

      {/* Refereed Citations Timeline Dialog */}
      <Dialog open={refereedCitationsDialogOpen} onOpenChange={setRefereedCitationsDialogOpen}>
        <DialogContent className="w-[95vw] max-w-[min(896px,calc((90vh-4rem)*10/7))] max-h-[90vh] overflow-hidden">
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/citations_by_year.svg"
              alt="Citations Timeline showing refereed and non-refereed citations from 2018-2026"
              fill
              className="object-contain"
              priority
            />
          </div>
        </DialogContent>
      </Dialog>
    </>
  )
}
