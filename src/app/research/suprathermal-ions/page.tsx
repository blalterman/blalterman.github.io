
import fs from 'fs';
import path from 'path';
import { ResearchFigure } from '@/components/research-figure';

export default function SuprathermalIonsPage() {
  const dataFilePath = path.join(process.cwd(), 'data', 'research-paragraphs.json');
  const jsonData = fs.readFileSync(dataFilePath, 'utf-8');
  const researchParagraphs = JSON.parse(jsonData);
  const introductoryParagraph = researchParagraphs['suprathermal-ions'];

  const figuresFilePath = path.join(process.cwd(), 'data', 'research-figures.json');
  const figuresData = fs.readFileSync(figuresFilePath, 'utf-8');
  const figures = JSON.parse(figuresData);

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24">
      <h1 className="text-3xl md:text-4xl font-bold font-headline">Suprathermal Ions</h1>
      <p className="text-lg text-muted-foreground mt-4">
              {introductoryParagraph}
      </p>
      <ResearchFigure src="/paper-figures/html/STQT-SpectralIndex-Fig4.html"
                      alt="Figure 4 from S. T. Quine and R. G. W. Ratcliffe, 2021, ApJ, 917, 98"
                      caption="Figure 4 from S. T. Quine and R. G. W. Ratcliffe, 2021, ApJ, 917, 98. This figure shows the spectral index of suprathermal ions as a function of solar wind speed." />
      <p className="text-sm text-muted-foreground mt-4">
                Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
            </p>
    </main>
  );
}
