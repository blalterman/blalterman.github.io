import { About } from '@/components/about';
import { Contact } from '@/components/contact';
import { Header } from '@/components/header';
import { loadJSONData } from '@/lib/data-loader';

interface BiographyData {
  heading: string;
  tagline: string;
  paragraphs: string[];
}

export default function Home() {
  const biographyData = loadJSONData<BiographyData>('biography.json');

  return (
    <div className="flex min-h-screen w-full flex-col bg-background">
      <Header />
      <main className="flex-1">
        <About biographyData={biographyData} />
      </main>
      <Contact />
    </div>
  );
}
