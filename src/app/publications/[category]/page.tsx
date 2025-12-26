import { Button } from "@/components/ui/button";
import { GraduationCap, BookOpen, Database, FileText, Presentation, ScrollText, FileCode } from "lucide-react";
import { Metadata, ResolvingMetadata } from 'next';
import { loadJSONData } from "@/lib/data-loader";
import { getPublicationsByType } from "@/lib/publication-utils";
import type { Publication } from "@/types/publication";
import { redirect } from "next/navigation";
import Link from "next/link";
import { PublicationFilters } from "@/components/publication-filters";

type Props = {
  params: Promise<{ category: string }>;
};

interface PublicationCategory {
  title: string;
  slug: string;
  icon: string;
  description: string;
  publicationType: string | string[];
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

export async function generateStaticParams() {
  const categoriesData = loadJSONData<PublicationsCategoriesData>('publications-categories.json');
  const adsPublications = loadJSONData<Publication[]>('ads_publications.json');

  // Only generate routes for categories that have publications
  const categoriesWithPublications = categoriesData.categories.filter((category) => {
    const publications = getPublicationsByType(adsPublications, category.publicationType);
    return publications.length > 0;
  });

  return categoriesWithPublications.map((category) => ({
    category: category.slug,
  }));
}

export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const { category } = await params;
  const categoriesData = loadJSONData<PublicationsCategoriesData>('publications-categories.json');
  const categoryData = categoriesData.categories.find((c) => c.slug === category);

  return {
    title: `${categoryData?.title || 'Publications'} | B. L. Alterman`,
    description: categoryData?.description || "Publications by B. L. Alterman",
  };
}

export default async function PublicationCategoryPage({ params }: { params: Promise<{ category: string }> }) {
  const { category } = await params;

  const categoriesData = loadJSONData<PublicationsCategoriesData>('publications-categories.json');
  const categoryData = categoriesData.categories.find((c) => c.slug === category);

  // If category not found, redirect to /publications
  if (!categoryData) {
    redirect('/publications');
  }

  const adsPublications = loadJSONData<Publication[]>('ads_publications.json');
  const publications = getPublicationsByType(adsPublications, categoryData.publicationType);

  // If no publications in this category, redirect to /publications
  if (publications.length === 0) {
    redirect('/publications');
  }

  const IconComponent = iconMap[categoryData.icon as keyof typeof iconMap];

  return (
    <div className="container mx-auto py-16 md:py-24">
      {/* Breadcrumb navigation */}
      <nav className="mb-8 text-sm text-muted-foreground">
        <Link href="/" className="hover:text-foreground transition-colors">
          Home
        </Link>
        {" / "}
        <Link href="/publications" className="hover:text-foreground transition-colors">
          Publications
        </Link>
        {" / "}
        <span className="text-foreground">{categoryData.title}</span>
      </nav>

      {/* Page title with icon */}
      <h1 className="text-2xl font-bold text-center flex items-center justify-center mb-8">
        {IconComponent && <IconComponent className="mr-3 h-8 w-8 text-primary" />}
        {categoryData.title}
      </h1>

      {/* Publications with filtering */}
      <PublicationFilters
        publications={publications}
        categoryData={categoryData}
        {...(categoryData.slug === 'conferences' && {
          labels: { journal: 'Conference' }
        })}
      />

      {/* Back to overview button */}
      <div className="text-center mt-8">
        <Button asChild variant="outline">
          <Link href="/publications">
            ← Back to All Publications
          </Link>
        </Button>
      </div>
    </div>
  );
}
