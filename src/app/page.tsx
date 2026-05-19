import { About } from '@/components/about';
import { Contact } from '@/components/contact';
import { Header } from '@/components/header';
import { Hero } from '@/components/hero';
import { loadJSONData } from '@/lib/data-loader';
import { Metadata } from 'next';
import { buildPageMetadata } from '@/lib/metadata';

interface BiographyData {
  heading: string;
  tagline: string;
  paragraphs: string[];
}

export const metadata: Metadata = buildPageMetadata({
  path: '/',
  title: 'B. L. Alterman | Research Astrophysicist',
  description: 'Research astrophysicist studying the solar wind, heliophysics, and space weather. Explore publications, projects, and academic collaborations.',
});

export default function Home() {
  const biographyData = loadJSONData<BiographyData>('biography-homepage.json');

  return (
    <div className="flex min-h-screen w-full flex-col bg-background">
      <Header />
      <main className="flex-1">
        <Hero biographyData={biographyData} />
        <About biographyData={biographyData} />
      </main>
      <Contact />
    </div>
  );
}
