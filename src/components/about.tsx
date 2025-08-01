import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import Image from 'next/image';

export function About() {
  return (
    <section id="about" className="container py-16 md:py-24">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12 items-center">
        <div className="md:col-span-1 flex justify-center">
            <Avatar className="h-48 w-48 md:h-64 md:w-64 border-4 border-primary/50 shadow-lg">
                <Image src="/images/headshot.jpg" alt="B. L. Alterman" width={256} height={256} className="rounded-full object-cover w-full h-full" unoptimized />
                <AvatarFallback>BA</AvatarFallback>
            </Avatar>
        </div>
        <div className="md:col-span-2 space-y-4">
          <h1 className="text-3xl md:text-5xl font-bold font-headline tracking-tighter">
            Academic. Researcher. Innovator.
          </h1>
          <p className="text-xl md:text-2xl text-primary font-light">
            Exploring the Solar Wind to Understand Our Place in the Cosmos
          </p>
          <p className="text-lg text-muted-foreground">
            I am an academic and researcher with a passion for uncovering insights from complex data. My work focuses on planetary science and astrophysics, leveraging advanced data analysis techniques and computational modeling to answer fundamental questions about the universe. I thrive in collaborative environments and am always eager to explore new frontiers in science and technology.
          </p>
        </div>
      </div>
    </section>
  );
}
