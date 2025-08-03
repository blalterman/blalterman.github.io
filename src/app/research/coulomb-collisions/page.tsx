
import fs from 'fs';
import path from 'path';
import { ResearchFigure } from '@/components/research-figure';

export default function CoulombCollisionsPage() {
  const paragraphsPath = path.join(process.cwd(), 'data', 'research-paragraphs.json');
  const figuresPath = path.join(process.cwd(), 'data', 'research-figures.json');

  const paragraphs = JSON.parse(fs.readFileSync(paragraphsPath, 'utf-8'));
  const figures = JSON.parse(fs.readFileSync(figuresPath, 'utf-8'));

  const paragraph = paragraphs['coulomb-collisions'];
  const figure = figures['coulomb-collisions'];

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24">
      <h1 className="text-3xl md:text-4xl font-bold font-headline">Coulomb Collisions</h1>
      <p className="text-lg text-muted-foreground mt-4">
        {paragraph}
      </p>
      <p className="text-sm text-muted-foreground mt-8">
        Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
      </p>
      {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
    </main>
  );
}
