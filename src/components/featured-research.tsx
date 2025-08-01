import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ExternalLink, BookOpen, ArrowRight } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';
import researchProjects from '../../public/data/research-projects.json';

export function FeaturedResearch() {
  return (
    <section id="research" className="bg-muted/50 py-16 md:py-24">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold font-headline">Featured Research</h2>
          <p className="text-lg text-muted-foreground mt-2">Highlights from my research contributions and discoveries.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {researchProjects.map((project) => (
            <Card key={project.title} className="flex flex-col overflow-hidden shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <div className="relative aspect-[16/9] w-full">
                <Image src={project.image} alt={project.title} fill className="object-cover" data-ai-hint={project.imageHint} />
              </div>
              <div className="flex flex-col flex-1 p-6">
                <CardHeader className="p-0 mb-4">
                  <CardTitle>{project.title}</CardTitle>
                </CardHeader>
                <CardContent className="p-0 flex-1">
                  <CardDescription>{project.description}</CardDescription>
                </CardContent>
                <CardFooter className="p-0 pt-4 flex justify-end gap-2">
                  <Button variant="outline" asChild>
                    <Link href={project.publicationLink} target="_blank">
                      <BookOpen className="mr-2 h-4 w-4" />
                      Publication
                    </Link>
                  </Button>
                  <Button asChild>
                    <Link href={project.datasetLink} target="_blank">
                      <ExternalLink className="mr-2 h-4 w-4" />
                      Dataset
                    </Link>
                  </Button>
                </CardFooter>
              </div>
            </Card>
          ))}
        </div>
        <div className="text-center mt-12">
            <Button size="lg" asChild>
                <Link href="/publications">
                    View All Publications
                    <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
            </Button>
        </div>
      </div>
    </section>
  );
}
