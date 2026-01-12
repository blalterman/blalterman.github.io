import { ResearchTopicPrototype } from '@/components/research-topic-prototype';
import { ResearchTopicData } from '@/types/research-topic';
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

// Load all topic data from JSON files
function loadAllTopics(): ResearchTopicData[] {
  const topicsDir = path.join(process.cwd(), 'public/data/research-topics');
  const files = fs.readdirSync(topicsDir).filter(f => f.endsWith('.json'));

  return files.map(file => {
    const filePath = path.join(topicsDir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  });
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
