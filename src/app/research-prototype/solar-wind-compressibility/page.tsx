import { ResearchTopicPrototype } from '@/components/research-topic-prototype';
import { ResearchTopicData } from '@/types/research-topic';
import { Metadata } from 'next';
import fs from 'fs';
import path from 'path';

export const metadata: Metadata = {
  title: 'Solar Wind Compressibility (Prototype) | B. L. Alterman',
  description: 'How density fluctuations regulate helium - prototype page with rich summaries',
};

function loadTopicData(): ResearchTopicData {
  const filePath = path.join(process.cwd(), 'public/data/research-topics/solar-wind-compressibility.json');
  const fileContents = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(fileContents);
}

export default function SolarWindCompressibilityPrototype() {
  const data = loadTopicData();

  return (
    <main className="flex-1 container mx-auto py-16 md:py-24 max-w-4xl">
      <div className="mb-8 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          <strong>Prototype:</strong> This is a prototype page testing the new research topic format with rich summaries.
        </p>
      </div>
      <ResearchTopicPrototype data={data} />
    </main>
  );
}
