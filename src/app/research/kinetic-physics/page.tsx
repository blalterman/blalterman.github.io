
import fs from 'fs';
import path from 'path';

const paragraphs = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data/research-paragraphs.json'), 'utf8'));
const paragraph = paragraphs['kinetic-physics'];

export default function KineticPhysicsPage() {
    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <h1 className="text-3xl md:text-4xl font-bold font-headline">Kinetic Physics</h1>
            <p className="text-lg text-muted-foreground mt-4">
                {paragraph}
            </p>
            <p className="text-sm text-muted-foreground mt-4">
                Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
            </p>
        </main>
    );
}