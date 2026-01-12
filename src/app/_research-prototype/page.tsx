import { Metadata } from 'next';
import Link from 'next/link';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight } from 'lucide-react';
import { filterPublishedProjects } from '@/lib/research-utils';
import { ResearchTopicData } from '@/types/research-topic';
import fs from 'fs';
import path from 'path';

export const metadata: Metadata = {
  title: 'Research Topics (Prototype) | B. L. Alterman',
  description: 'Prototype research pages organized by fundamental research questions in heliophysics.',
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

// Convert slug to title case (e.g., "solar-activity" -> "Solar Activity")
function slugToTitle(slug: string): string {
  return slug
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

interface ResearchQuestion {
  question: string;
  subtitle: string;
  topics: string[];
}

const researchQuestions: ResearchQuestion[] = [
  {
    question: 'Where does the solar wind come from?',
    subtitle: 'Source Identification',
    topics: [
      'sources-of-the-solar-wind',
      'helium-abundance',
      'heavy-ion-composition',
      'solar-wind-compressibility',
      'space-weather',
    ],
  },
  {
    question: 'How does the solar wind evolve on its journey to Earth?',
    subtitle: 'Heliospheric Evolution',
    topics: ['alfven-waves', 'coulomb-collisions'],
  },
  {
    question: "How does the Sun's activity cycle shape the heliosphere?",
    subtitle: 'Temporal Evolution',
    topics: ['solar-activity'],
  },
  {
    question: 'What energetic particles populate the heliosphere?',
    subtitle: 'Energetic Particle Environment',
    topics: ['suprathermal-ions'],
  },
];

export default function ResearchPrototypePage() {
  // Load and filter topics by published status
  const allTopics = loadAllTopics();
  const publishedTopics = filterPublishedProjects(allTopics);
  const publishedSlugs = new Set(publishedTopics.map(t => t.slug));

  // Filter each section's topics to only include published ones
  const filteredQuestions = researchQuestions
    .map(section => ({
      ...section,
      topics: section.topics.filter(slug => publishedSlugs.has(slug))
    }))
    .filter(section => section.topics.length > 0);

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24 max-w-5xl">
      <div className="mb-8 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          <strong>Prototype:</strong> These are prototype research pages organized by fundamental research questions.
        </p>
      </div>

      <header className="text-center mb-12">
        <h1 className="font-headline text-4xl md:text-5xl mb-4">Research Topics</h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Exploring the Sun-Earth connection through fundamental questions about solar wind origins, evolution, and variability.
        </p>
      </header>

      <div className="space-y-16">
        {filteredQuestions.map((section) => (
          <section key={section.subtitle}>
            <div className="mb-6">
              <h2 className="font-headline text-2xl md:text-3xl text-primary mb-1">
                {section.question}
              </h2>
              <p className="text-sm text-muted-foreground uppercase tracking-wide">
                {section.subtitle}
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {section.topics.map((slug) => (
                <Link key={slug} href={`/research-prototype/${slug}`}>
                  <Card className="h-full hover:shadow-lg hover:-translate-y-1 transition-all duration-300 cursor-pointer group">
                    <CardHeader className="flex flex-row items-center justify-between">
                      <CardTitle className="text-lg">{slugToTitle(slug)}</CardTitle>
                      <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
                    </CardHeader>
                  </Card>
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
