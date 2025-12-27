import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import Image from 'next/image';

interface BiographyData {
  heading: string;
  tagline: string;
  paragraphs: string[];
}

interface HeroProps {
  biographyData: BiographyData;
}

export function Hero({ biographyData }: HeroProps) {
  return (
    <section className="container mx-auto py-8 md:py-12">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12 items-center">
        {/* Headshot - Left Column */}
        <div className="md:col-span-1 flex justify-center">
          <Avatar className="h-48 w-48 md:h-64 md:w-64 border-4 border-primary/50 shadow-lg">
            <Image
              src="/images/headshot.jpg"
              alt="B. L. Alterman"
              width={256}
              height={256}
              className="rounded-full object-cover w-full h-full"
            />
            <AvatarFallback>BA</AvatarFallback>
          </Avatar>
        </div>

        {/* Name + Tagline - Right Columns */}
        <div className="md:col-span-2 space-y-4">
          <h1 className="text-3xl md:text-5xl font-bold font-headline tracking-tighter">
            {biographyData.heading}
          </h1>
          <p className="text-xl md:text-2xl text-primary font-light">
            {biographyData.tagline}
          </p>
        </div>
      </div>
    </section>
  );
}
