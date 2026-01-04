'use client';

import { useState } from 'react';
import Image from 'next/image';
import { ResearchTopicData } from '@/types/research-topic';
import { ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';

interface ResearchTopicPrototypeProps {
  data: ResearchTopicData;
}

function SummarySection({
  title,
  content,
  defaultOpen = false
}: {
  title: string;
  content: string;
  defaultOpen?: boolean;
}) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border-b border-border last:border-b-0">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between py-3 text-left hover:bg-muted/50 transition-colors"
      >
        <span className="font-medium text-foreground">{title}</span>
        {isOpen ? (
          <ChevronUp className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        )}
      </button>
      {isOpen && (
        <div className="pb-4 text-muted-foreground leading-relaxed">
          {content}
        </div>
      )}
    </div>
  );
}

export function ResearchTopicPrototype({ data }: ResearchTopicPrototypeProps) {
  const { primary_figure, related_figures, paper } = data;

  return (
    <div className="space-y-12">
      {/* Header */}
      <header>
        <h1 className="font-headline text-4xl mb-2">{data.title}</h1>
        <p className="text-xl text-muted-foreground">{data.subtitle}</p>
      </header>

      {/* Description */}
      <section>
        <p className="text-lg leading-relaxed">{data.description}</p>
      </section>

      {/* Primary Figure */}
      <section className="space-y-6">
        <div className="relative w-full aspect-[4/3] bg-muted rounded-lg overflow-hidden">
          <Image
            src={primary_figure.src}
            alt={primary_figure.alt}
            fill
            className="object-contain p-4"
            priority
          />
        </div>

        <div className="space-y-4">
          <h2 className="font-headline text-2xl">{primary_figure.short_title}</h2>

          {/* Summary Accordion */}
          <div className="border border-border rounded-lg px-4">
            <SummarySection
              title="What We See"
              content={primary_figure.summary.what_we_see}
              defaultOpen={true}
            />
            <SummarySection
              title="The Finding"
              content={primary_figure.summary.the_finding}
            />
            <SummarySection
              title="Why It Matters"
              content={primary_figure.summary.why_it_matters}
            />
          </div>

          {/* Keywords */}
          <div className="flex flex-wrap gap-2">
            {primary_figure.keywords.map((keyword) => (
              <span
                key={keyword}
                className="px-2 py-1 text-xs bg-muted text-muted-foreground rounded-full"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Related Figures */}
      {related_figures.length > 0 && (
        <section className="space-y-6">
          <h2 className="font-headline text-2xl">Related Figures</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {related_figures.map((fig) => (
              <div
                key={`${fig.paper_id}-${fig.figure_id}`}
                className="border border-border rounded-lg overflow-hidden"
              >
                <div className="relative w-full aspect-[4/3] bg-muted">
                  <Image
                    src={fig.src}
                    alt={fig.alt}
                    fill
                    className="object-contain p-2"
                  />
                </div>
                <div className="p-4 space-y-2">
                  <h3 className="font-medium">{fig.short_title}</h3>
                  <p className="text-sm text-muted-foreground">{fig.summary_short}</p>
                  <p className="text-xs text-primary">{fig.relevance}</p>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Paper Citation */}
      <section className="border-t border-border pt-6">
        <h2 className="font-headline text-lg mb-2">Source</h2>
        <p className="text-muted-foreground">
          {paper.title}
        </p>
        <p className="text-sm text-muted-foreground mt-1">
          {paper.journal} ({paper.year})
        </p>
        <a
          href={paper.doi}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-primary hover:underline text-sm mt-2"
        >
          View Paper <ExternalLink className="h-3 w-3" />
        </a>
        <p className="text-xs text-muted-foreground mt-2">
          © {paper.license.year} {paper.license.holder}. {paper.license.type}
        </p>
      </section>
    </div>
  );
}
