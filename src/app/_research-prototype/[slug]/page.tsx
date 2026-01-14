import { ResearchTopicPrototype } from '@/components/research-topic-prototype';
import {
  ResearchTopicData,
  RawResearchTopicData,
  FigureRegistry,
  PrimaryFigure,
  RelatedFigure
} from '@/types/research-topic';
import { filterPublishedProjects } from '@/lib/research-utils';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import fs from 'fs';
import path from 'path';

// Only allow statically generated paths (required for static export with zero pages)
export const dynamicParams = false;

type Props = {
  params: Promise<{ slug: string }>;
};

// Load the figure registry
function loadFigureRegistry(): FigureRegistry {
  const registryPath = path.join(process.cwd(), 'public/data/figure-registry.json');
  const content = fs.readFileSync(registryPath, 'utf8');
  return JSON.parse(content);
}

// Load all raw topic data from JSON files
function loadAllRawTopics(): RawResearchTopicData[] {
  const topicsDir = path.join(process.cwd(), 'public/data/research-topics');
  const files = fs.readdirSync(topicsDir).filter(f => f.endsWith('.json'));

  return files.map(file => {
    const filePath = path.join(topicsDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  });
}

// Resolve a raw topic by joining with the figure registry
function resolveTopicData(
  raw: RawResearchTopicData,
  registry: FigureRegistry
): ResearchTopicData {
  // Resolve primary figure
  const primaryEntry = registry[raw.primary_figure.ref];
  if (!primaryEntry) {
    throw new Error(`Figure not found in registry: ${raw.primary_figure.ref}`);
  }

  const primaryFigure: PrimaryFigure = {
    paper_id: primaryEntry.paper_id,
    figure_id: primaryEntry.figure_id,
    src: primaryEntry.src,
    short_title: primaryEntry.short_title,
    alt: primaryEntry.alt,
    summary: primaryEntry.summary!,  // Primary figures must have extended summary
    // Merge registry keywords with topic-specific keywords
    keywords: [
      ...primaryEntry.keywords,
      ...(raw.primary_figure.topic_keywords || [])
    ].filter((k, i, arr) => arr.indexOf(k) === i)  // dedupe
  };

  // Resolve related figures
  const relatedFigures: RelatedFigure[] = raw.related_figures.map(rf => {
    const entry = registry[rf.ref];
    if (!entry) {
      throw new Error(`Figure not found in registry: ${rf.ref}`);
    }

    return {
      paper_id: entry.paper_id,
      figure_id: entry.figure_id,
      src: entry.src,
      short_title: entry.short_title,
      alt: entry.alt,
      relevance: rf.relevance,  // From topic, not registry
      summary_short: entry.summary_short || ''
    };
  });

  return {
    slug: raw.slug,
    title: raw.title,
    subtitle: raw.subtitle,
    description: raw.description,
    primary_figure: primaryFigure,
    related_figures: relatedFigures,
    related_topics: raw.related_topics,
    published: raw.published,
    paper: raw.paper
  };
}

// Load and resolve all topics
function loadAllTopics(): ResearchTopicData[] {
  const registry = loadFigureRegistry();
  const rawTopics = loadAllRawTopics();
  return rawTopics.map(raw => resolveTopicData(raw, registry));
}

export async function generateStaticParams() {
  const topics = loadAllTopics();
  const publishedTopics = filterPublishedProjects(topics);

  return publishedTopics.map((topic) => ({
    slug: topic.slug,
  }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const topics = loadAllTopics();
  const topic = topics.find(t => t.slug === slug);

  return {
    title: `${topic?.title || 'Research'} (Prototype) | B. L. Alterman`,
    description: topic?.description,
  };
}

export default async function ResearchPrototypePage({ params }: Props) {
  const { slug } = await params;
  const topics = loadAllTopics();
  const topic = topics.find(t => t.slug === slug);

  if (!topic) {
    notFound();
  }

  // Redirect/404 if unpublished in production
  const isDev = process.env.NODE_ENV === 'development';
  if (!isDev && topic.published === false) {
    notFound();
  }

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24 max-w-4xl">
      <div className="mb-8 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          <strong>Prototype:</strong> This is a prototype page testing the new research topic format with rich summaries.
          <a href={`/research/${slug}`} className="ml-2 underline">
            View current page →
          </a>
        </p>
      </div>
      <ResearchTopicPrototype data={topic} />
    </main>
  );
}
