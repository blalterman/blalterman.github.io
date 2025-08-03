
import fs from 'fs';
import path from 'path';
import { ResearchFigure } from '@/components/research-figure';

const paragraphs = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data/research-paragraphs.json'), 'utf-8'));
const figures = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data/research-figures.json'), 'utf-8'));

export default function CoulombCollisionsPage() {
  const paragraph = paragraphs['coulomb-collisions'];
  const figure = figures['coulomb-collisions'];

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24">
      <h1 className="text-3xl md:text-4xl font-bold font-headline">Coulomb Collisions</h1>
      <p className="text-lg text-muted-foreground mt-4">
        {paragraph}
      </p>
      {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
    </main>
  );
}
