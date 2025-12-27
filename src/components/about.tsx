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
      <div className="space-y-4">
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
    </section>
  );
}
