import Link from 'next/link';

interface BiographyData {
  heading: string;
  tagline: string;
  paragraphs: string[];
}

interface AboutProps {
  biographyData: BiographyData;
}

export function About({ biographyData }: AboutProps) {
  return (
    <section id="about" className="container mx-auto pt-0 pb-16 md:pb-24">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
        {/* Empty space on left to align with hero headshot column */}
        <div className="md:col-span-1"></div>

        {/* Biography text aligned with hero name/tagline */}
        <div className="md:col-span-2 space-y-4">
          {biographyData.paragraphs.map((paragraph, index) => (
            <p key={index} className="text-lg text-muted-foreground">
              {paragraph}
            </p>
          ))}
          <p className="text-lg text-muted-foreground mt-4">
            Explore my research vision, leadership philosophy, and approach to building scientific systems that drive discovery{' '}
            <Link href="/ben" className="text-primary hover:underline font-medium">
              →
            </Link>
          </p>
        </div>
      </div>
    </section>
  );
}
