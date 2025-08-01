import { About } from '@/components/about';
import { Contact } from '@/components/contact';
import { Header } from '@/components/header';
import { FeaturedResearch } from '@/components/featured-research';
import { Skills } from '@/components/skills';

export default function Home() {
  return (
    <div className="flex min-h-screen w-full flex-col bg-background">
      <Header />
      <main className="flex-1">
        <About />
        <Skills />
        <FeaturedResearch />
      </main>
      <Contact />
    </div>
  );
}
