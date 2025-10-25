
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import Image from 'next/image';
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
    <section id="about" className="container mx-auto py-16 md:py-24">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12 items-center">
        <div className="md:col-span-1 flex justify-center">
            <Avatar className="h-48 w-48 md:h-64 md:w-64 border-4 border-primary/50 shadow-lg">
                <Image src="/images/headshot.jpg" alt="B. L. Alterman" width={256} height={256} className="rounded-full object-cover w-full h-full" />
                <AvatarFallback>BA</AvatarFallback>
            </Avatar>
        </div>
        <div className="md:col-span-2 space-y-4">
          <h1 className="text-3xl md:text-5xl font-bold font-headline tracking-tighter">
            {biographyData.heading}
          </h1>
          <p className="text-xl md:text-2xl text-primary font-light">
            {biographyData.tagline}
          </p>
          {biographyData.paragraphs.map((paragraph, index) => (
            <p key={index} className="text-lg text-muted-foreground">
              {paragraph}
            </p>
          ))}
          <p className="text-lg text-muted-foreground mt-4">
            Want to learn more about my research vision and team philosophy?{' '}
            <Link href="/ben" className="text-primary hover:underline font-medium">
              Read my full story
            </Link>.
          </p>
        </div>
      </div>
    </section>
  );
}
