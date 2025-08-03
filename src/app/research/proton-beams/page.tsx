
import fs from 'fs';
import path from 'path';
import { ResearchFigure } from '@/components/research-figure';

const paragraphs = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data/research-paragraphs.json'), 'utf8'));
const figures = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data/research-figures.json'), 'utf-8'));
const paragraph = paragraphs['proton-beams'];

export default function ProtonBeamsPage() {
    const figure = figures['proton-beams'];
    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <h1 className="text-3xl md:text-4xl font-bold font-headline">Proton Beams</h1>
            <p className="text-lg text-muted-foreground mt-4">
                {paragraph}
            </p>
            {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
            <p className="text-sm text-muted-foreground mt-4">
                Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
            </p>
        </main>
    );
}
