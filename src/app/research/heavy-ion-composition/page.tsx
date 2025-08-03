
import fs from 'fs';
import path from 'path';
import { ResearchFigure } from '@/components/research-figure';

export default function HeavyIonCompositionPage() {
  const paragraphsPath = path.join(process.cwd(), 'data', 'research-paragraphs.json');
  const figuresPath = path.join(process.cwd(), 'data', 'research-figures-with-captions.json');

  const paragraphs = JSON.parse(fs.readFileSync(paragraphsPath, 'utf-8'));
  const figuresData = JSON.parse(fs.readFileSync(figuresPath, 'utf-8'));

  const pageData = figuresData.find((p: any) => p.slug === 'heavy-ion-composition');
  const paragraph = paragraphs['heavy-ion-composition'];
  const figure = pageData?.figure;

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24">
      <h1 className="text-3xl md:text-4xl font-bold font-headline">Heavy Ion Composition</h1>
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
