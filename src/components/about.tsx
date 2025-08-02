
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import Image from 'next/image';

export function About() {
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
            Academic. Researcher. Explorer.
          </h1>
          <p className="text-xl md:text-2xl text-primary font-light">
            Exploring the Solar Wind to Understand Our Place in the Cosmos
          </p>
          <p className="text-lg text-muted-foreground">
            I'm a Research Astrophysicist based in Greenbelt, MD, where I study how the Sun drives the solar wind and shapes the space environment of our solar system. I earned my PhD in Applied Physics from the University of Michigan, where I focused on how Coulomb collisions and kinetic processes influence the solar wind. After a postdoc at the Southwest Research Institute in San Antonio—where I was later promoted to Research Scientist—I joined NASA as a civil servant to continue my work in heliophysics.
          </p>
          <p className="text-lg text-muted-foreground">
            I consider myself a heliophysics generalist, working across the thermal and suprathermal solar wind. My research spans multiple spacecraft—including Wind, ACE, Parker Solar Probe, and Solar Orbiter—and timescales ranging from seconds to decades. I’m especially interested in how the composition and structure of the solar wind reflect both its solar source and the processes it undergoes during interplanetary travel. My recent work on helium abundance and heavy ion composition has opened up new questions about solar cycle variability and space weather forecasting.
          </p>
          <p className="text-lg text-muted-foreground">
            At the heart of my work is a deep curiosity about our Sun, humanity’s place in the Universe, and how solar variability affects life on Earth through space weather. As a Fellow of The Explorers Club and an active member of the heliophysics community, I try to bring energy, creativity, and a systems-level perspective to everything I do.
          </p>
        </div>
      </div>
    </section>
  );
}
