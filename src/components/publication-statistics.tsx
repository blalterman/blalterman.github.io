'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog'
import { TrendingUp } from 'lucide-react'

interface PublicationStatisticsProps {
  stats: any;
}

/**
 * Displays publication statistics from NASA ADS metrics.
 * Shows h-index, total papers, citations, and refereed publications.
 * Makes "Total papers" and "Total citations" clickable to view timeline plots in modals.
 */
export function PublicationStatistics({ stats }: PublicationStatisticsProps) {
  const [publicationsDialogOpen, setPublicationsDialogOpen] = useState(false)
  const [citationsDialogOpen, setCitationsDialogOpen] = useState(false)
  const [refereedPapersDialogOpen, setRefereedPapersDialogOpen] = useState(false)
  const [refereedCitationsDialogOpen, setRefereedCitationsDialogOpen] = useState(false)
  const [hIndexDialogOpen, setHIndexDialogOpen] = useState(false)

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
        {/* CLICKABLE: h-index → H-Index Timeline */}
        <ClickableMetric
          value={stats.summary.h_index}
          label="H-Index"
          onClick={() => setHIndexDialogOpen(true)}
        />

        {/* CLICKABLE: Total papers → Publications Timeline */}
        <ClickableMetric
          value={stats.summary.total_papers}
          label={<>Total<br />Papers</>}
          onClick={() => setPublicationsDialogOpen(true)}
        />

        {/* CLICKABLE: Total citations → Citations Timeline */}
        <ClickableMetric
          value={stats.summary.total_citations}
          label={<>Total<br />Citations</>}
          onClick={() => setCitationsDialogOpen(true)}
        />

        {/* CLICKABLE: Refereed papers → Publications Timeline */}
        <ClickableMetric
          value={stats.summary.refereed_papers}
          label={<>Refereed<br />Papers</>}
          onClick={() => setRefereedPapersDialogOpen(true)}
        />

        {/* CLICKABLE: Refereed citations → Citations Timeline */}
        <ClickableMetric
          value={stats.summary.refereed_citations}
          label={<>Refereed<br />Citations</>}
          onClick={() => setRefereedCitationsDialogOpen(true)}
        />

        {/* CLICKABLE: Invited Presentations → Publications Timeline (MOVED TO END) */}
        <ClickableMetric
          value={stats.summary.invited_total}
          label={<>Invited<br />Presentations</>}
          onClick={() => setPublicationsDialogOpen(true)}
        />
      </div>

      {/* Publications Timeline Dialog */}
      <Dialog open={publicationsDialogOpen} onOpenChange={setPublicationsDialogOpen}>
        <DialogContent className="w-[95vw] max-w-[min(896px,calc((90vh-4rem)*10/7))] max-h-[90vh] overflow-hidden">
          <DialogTitle className="sr-only">Cumulative Publications</DialogTitle>
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/publications_timeline.svg"
              alt="Cumulative publications showing total refereed articles, conference contributions, and other publications from 2014-2025"
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
          <DialogTitle className="sr-only">Cumulative Citations</DialogTitle>
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/citations_by_year.svg"
              alt="Cumulative citations showing total refereed and non-refereed citations from 2018-2026"
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
          <DialogTitle className="sr-only">Cumulative Publications</DialogTitle>
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/publications_timeline.svg"
              alt="Cumulative publications showing total refereed articles, conference contributions, and other publications from 2014-2025"
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
          <DialogTitle className="sr-only">Cumulative Citations</DialogTitle>
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/citations_by_year.svg"
              alt="Cumulative citations showing total refereed and non-refereed citations from 2018-2026"
              fill
              className="object-contain"
              priority
            />
          </div>
        </DialogContent>
      </Dialog>

      {/* H-Index Timeline Dialog */}
      <Dialog open={hIndexDialogOpen} onOpenChange={setHIndexDialogOpen}>
        <DialogContent className="w-[95vw] max-w-[min(896px,calc((90vh-4rem)*10/7))] max-h-[90vh] overflow-hidden">
          <DialogTitle className="sr-only">H-Index Timeline</DialogTitle>
          <div className="relative w-full aspect-[10/7]">
            <Image
              src="/plots/h_index_timeline.svg"
              alt="h-index timeline showing growth from 2014 to 2025"
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
