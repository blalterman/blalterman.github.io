
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRight } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';

interface ResearchProject {
  title: string;
  description: string;
  image: string;
  imageHint: string;
  slug: string;
}

interface FeaturedResearchProps {
    heading: string;
    tagline: string;
    researchProjects: ResearchProject[];
}

export function FeaturedResearch({ heading, tagline, researchProjects }: FeaturedResearchProps) {
  return (
    <section id="research" className="py-16 md:py-24">
      <div className="container mx-auto">
        <div className="text-center mb-12">
          <h2 className="font-headline">{heading}</h2>
          <p className="text-lg text-muted-foreground mt-2">{tagline}</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {researchProjects.map((project: any) => (
            <Card key={project.title} className="flex flex-col overflow-hidden shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <div className="flex flex-col flex-1 p-6">
                <CardHeader className="p-0 mb-4">
                  <CardTitle>{project.title}</CardTitle>
                </CardHeader>
                <CardContent className="p-0 flex-1">
                  <CardDescription>{project.description}</CardDescription>
                </CardContent>
                <CardFooter className="p-0 pt-4 flex justify-end gap-2">
                  <Button asChild>
                    <Link href={`/research/${project.slug}`}>
                      Details
                      <ArrowRight className="ml-2 h-4 w-4" />
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
