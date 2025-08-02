
import fs from 'fs';
import path from 'path';

export default function HeliumAbundancePage() {
    const dataFilePath = path.join(process.cwd(), 'data', 'research-paragraphs.json');
    const jsonData = fs.readFileSync(dataFilePath, 'utf-8');
    const paragraphs = JSON.parse(jsonData);
    const introductoryParagraph = paragraphs['helium-abundance'];

    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <h1 className="text-3xl md:text-4xl font-bold font-headline">Helium Abundance</h1>
            <p className="text-lg text-muted-foreground mt-4">
                {introductoryParagraph}
            </p>
            <p className="text-sm text-muted-foreground mt-8">
                Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
            </p>
        </main>
    );
}
