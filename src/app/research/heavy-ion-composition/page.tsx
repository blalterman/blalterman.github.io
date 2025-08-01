
import fs from 'fs';
import path from 'path';

const paragraphs = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data/research-paragraphs.json'), 'utf-8'));

export default function HeavyIonCompositionPage() {
  const paragraph = paragraphs['heavy-ion-composition'];

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24">
        <h1 className="text-3xl md:text-4xl font-bold font-headline">Heavy Ion Composition</h1>
        <p className="text-lg text-muted-foreground mt-4">
            {paragraph}
        </p>
        <p className="text-sm text-muted-foreground mt-8">
            Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
        </p>
    </main>
  );
}

