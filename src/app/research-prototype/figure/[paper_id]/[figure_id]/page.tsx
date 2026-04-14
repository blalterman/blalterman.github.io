import Link from 'next/link';
import { FigureRegistry, FigureRegistryEntry } from '@/types/research-topic';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import fs from 'fs';
import path from 'path';

export const dynamicParams = false;

type Props = {
  params: Promise<{ paper_id: string; figure_id: string }>;
};

function loadFigureRegistry(): FigureRegistry {
  const registryPath = path.join(process.cwd(), 'public/data/figure-registry.json');
  const content = fs.readFileSync(registryPath, 'utf8');
  return JSON.parse(content);
}

export async function generateStaticParams() {
  const registry = loadFigureRegistry();
  return Object.values(registry).map((entry: FigureRegistryEntry) => ({
    paper_id: entry.paper_id,
    figure_id: entry.figure_id,
  }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { paper_id, figure_id } = await params;
  const registry = loadFigureRegistry();
  const entry = registry[`${paper_id}/${figure_id}`];

  return {
    title: `${entry?.short_title || 'Figure'} | B. L. Alterman`,
    description: entry?.summary_short || undefined,
  };
}

function SummarySection({ title, content }: { title: string; content: string }) {
  return (
    <div className="border-b border-border last:border-b-0 py-4">
      <h3 className="font-medium text-foreground mb-2">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">{content}</p>
    </div>
  );
}

export default async function FigureDetailPage({ params }: Props) {
  const { paper_id, figure_id } = await params;
  const registry = loadFigureRegistry();
  const key = `${paper_id}/${figure_id}`;
  const entry = registry[key];

  if (!entry) {
    notFound();
  }

  // Find topic pages where this figure appears
  const primaryTopics = entry.used_as_primary_in || [];
  const relatedTopics = entry.used_as_related_in || [];
  const notShownTopics = entry.used_as_not_shown_in || [];

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24 max-w-4xl">
      <div className="mb-8">
        <button
          onClick={undefined}
          className="inline-flex items-center gap-1 text-muted-foreground hover:text-foreground transition-colors text-sm"
        >
          <ArrowLeft className="h-4 w-4" />
          <Link href="/research-prototype">Back to Research Topics</Link>
        </button>
      </div>

      <div className="space-y-8">
        {/* Figure Image */}
        <div className="flex justify-center overflow-hidden">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={entry.src}
            alt={entry.alt}
            className="max-w-full h-auto"
          />
        </div>

        {/* Title */}
        <h1 className="font-headline text-3xl">{entry.short_title}</h1>

        {/* Summary */}
        {entry.summary && (
          <div className="border border-border rounded-lg px-4">
            <SummarySection title="What We See" content={entry.summary.what_we_see} />
            <SummarySection title="The Finding" content={entry.summary.the_finding} />
            <SummarySection title="Why It Matters" content={entry.summary.why_it_matters} />
          </div>
        )}

        {/* Keywords */}
        {entry.keywords.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {entry.keywords.map((keyword: string) => (
              <span
                key={keyword}
                className="px-2 py-1 text-xs bg-muted text-muted-foreground rounded-full"
              >
                {keyword}
              </span>
            ))}
          </div>
        )}

        {/* Appears In */}
        {(primaryTopics.length > 0 || relatedTopics.length > 0 || notShownTopics.length > 0) && (
          <section className="border-t border-border pt-6">
            <h2 className="font-headline text-lg mb-3">Appears In</h2>
            <div className="space-y-2">
              {primaryTopics.map((slug: string) => (
                <Link
                  key={slug}
                  href={`/research-prototype/${slug}`}
                  className="block text-primary hover:underline"
                >
                  {slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} (primary figure)
                </Link>
              ))}
              {relatedTopics.map((slug: string) => (
                <Link
                  key={slug}
                  href={`/research-prototype/${slug}`}
                  className="block text-primary hover:underline"
                >
                  {slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                </Link>
              ))}
              {notShownTopics.map((slug: string) => (
                <Link
                  key={slug}
                  href={`/research-prototype/${slug}`}
                  className="block text-muted-foreground hover:text-primary hover:underline"
                >
                  {slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')} (related topic)
                </Link>
              ))}
            </div>
          </section>
        )}

        {/* Source */}
        <section className="border-t border-border pt-6">
          <p className="text-sm text-muted-foreground">
            {paper_id.replace(/_/g, ' ')} &middot; {figure_id.replace('_', ' ')}
          </p>
        </section>
      </div>
    </main>
  );
}
