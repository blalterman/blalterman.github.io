
import fs from 'fs';
import path from 'path';
import { ResearchFigure } from '@/components/research-figure';
import { Metadata, ResolvingMetadata } from 'next';

type Props = {
  params: { slug: string };
};

const pageSlug = 'space-weather';
const pageTitle = 'Space Weather';

export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const paragraphsPath = path.join(process.cwd(), 'data', 'research-paragraphs.json');
  const paragraphs = JSON.parse(fs.readFileSync(paragraphsPath, 'utf-8'));
  const paragraph = paragraphs[pageSlug];

  return {
    title: `${pageTitle} | B. L. Alterman`,
    description: paragraph,
  };
}

export default function SpaceWeatherPage() {
  const paragraphsPath = path.join(process.cwd(), 'data', 'research-paragraphs.json');
  const figuresPath = path.join(process.cwd(), 'data', 'research-figures-with-captions.json');

  const paragraphs = JSON.parse(fs.readFileSync(paragraphsPath, 'utf-8'));
  const figuresData = JSON.parse(fs.readFileSync(figuresPath, 'utf-8'));
  
  const pageData = figuresData.find((p: any) => p.slug === pageSlug);
  const paragraph = paragraphs[pageSlug];
  const figure = pageData?.figure;

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24">
      <h1 className="text-3xl md:text-4xl font-bold font-headline">{pageTitle}</h1>
      <p className="text-lg text-muted-foreground mt-4">
        {paragraph}
      </p>
      <p className="text-sm text-muted-foreground mt-4">
        Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
      </p>
      {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
    </main>
  );
}
