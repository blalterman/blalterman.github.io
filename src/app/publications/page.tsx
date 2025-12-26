import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { GraduationCap, BookOpen, Database, FileText, Presentation, ScrollText, FileCode, ArrowRight } from "lucide-react";
import { Metadata } from 'next';
import { loadJSONData } from "@/lib/data-loader";
import { getPublicationsByType } from "@/lib/publication-utils";
import type { Publication } from "@/types/publication";
import Link from "next/link";
import { PublicationStatistics } from "@/components/publication-statistics";

export const metadata: Metadata = {
  title: "Publications | B. L. Alterman",
  description: "A comprehensive list of peer-reviewed articles, datasets, conference proceedings, and other publications by B. L. Alterman, with links to NASA/ADS.",
};

interface PublicationsPageData {
  heading: string;
  tagline: string;
}

interface PublicationCategory {
  title: string;
  slug: string;
  icon: string;
  description: string;
  publicationType: string;
  showCitations: boolean;
}

interface PublicationsCategoriesData {
  heading: string;
  tagline: string;
  categories: PublicationCategory[];
}

const iconMap = {
  GraduationCap: GraduationCap,
  BookOpen: BookOpen,
  Database: Database,
  FileText: FileText,
  Presentation: Presentation,
  ScrollText: ScrollText,
  FileCode: FileCode,
};

export default function PublicationsPage() {
  const adsMetrics = loadJSONData<any>('ads_metrics.json');
  const adsPublications = loadJSONData<Publication[]>('ads_publications.json');
  const categoriesData = loadJSONData<PublicationsCategoriesData>('publications-categories.json');

  if (!adsMetrics || !adsPublications.length) {
    return (
      <div className="container mx-auto py-16 md:py-24 text-center">
        <p>Loading publication data...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-16 md:py-24">
      {/* Page heading */}
      <div className="text-center mb-12">
        <h1 className="font-headline">{categoriesData.heading}</h1>
        <p className="text-lg text-muted-foreground mt-2">{categoriesData.tagline}</p>
      </div>

      {/* Metrics display */}
      <PublicationStatistics adsMetrics={adsMetrics} />

      {/* Category cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
        {categoriesData.categories.map((category) => {
          const IconComponent = iconMap[category.icon as keyof typeof iconMap];
          const publications = getPublicationsByType(adsPublications, category.publicationType);
          const count = publications.length;

          // Only show categories that have publications
          if (count === 0) return null;

          return (
            <Card
              key={category.slug}
              className="flex flex-col overflow-hidden shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
            >
              <div className="flex flex-col flex-1 p-6">
                <CardHeader className="p-0 mb-4">
                  <CardTitle className="flex items-center justify-between text-2xl">
                    <span className="flex items-center">
                      {IconComponent && <IconComponent className="mr-3 h-6 w-6 text-primary" />}
                      {category.title}
                    </span>
                    <span className="text-sm font-normal bg-primary/10 text-primary px-3 py-1 rounded-full">
                      {count}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-0 flex-1">
                  <CardDescription className="text-base">
                    {category.description}
                  </CardDescription>
                </CardContent>
                <CardFooter className="p-0 pt-4 flex justify-end gap-2">
                  <Button asChild>
                    <Link href={`/publications/${category.slug}`}>
                      View
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                </CardFooter>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
