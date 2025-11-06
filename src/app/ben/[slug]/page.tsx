import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Telescope, Compass, HeartHandshake, GitBranch, Wand2 } from "lucide-react";
import { loadJSONData } from "@/lib/data-loader";
import { filterPublishedProjects } from "@/lib/research-utils";
import { Metadata, ResolvingMetadata } from "next";
import { redirect } from "next/navigation";
import Link from "next/link";

type Props = {
    params: Promise<{ slug: string }>;
};

interface BenSection {
    title: string;
    slug: string;
    icon: string;
    excerpt: string;
    paragraphs: string[];
    published?: boolean;
}

interface BenPageData {
    heading: string;
    tagline: string;
    sections: BenSection[];
}

const iconMap = {
    Telescope: Telescope,
    Compass: Compass,
    HeartHandshake: HeartHandshake,
    GitBranch: GitBranch,
    Wand2: Wand2,
};

export async function generateStaticParams() {
    const benData = loadJSONData<BenPageData>('ben-page.json');
    // Only generate static params for published sections (environment-aware)
    const publishedSections = filterPublishedProjects(benData.sections);
    return publishedSections.map((section) => ({
        slug: section.slug,
    }));
}

export async function generateMetadata(
    { params }: Props,
    parent: ResolvingMetadata
): Promise<Metadata> {
    const { slug } = await params;
    const benData = loadJSONData<BenPageData>('ben-page.json');
    const section = benData.sections.find((s) => s.slug === slug);

    return {
        title: `${section?.title || 'About Ben'} | B. L. Alterman`,
        description: section?.excerpt || "Learn about Ben's research vision and team-building philosophy.",
    };
}

export default async function BenSubpage({ params }: { params: Promise<{ slug: string }> }) {
    const { slug } = await params;

    const benData = loadJSONData<BenPageData>('ben-page.json');
    const section = benData.sections.find((s) => s.slug === slug);

    // Redirect to /ben if page is unpublished in production
    // (In development, allow access to all pages)
    const isDev = process.env.NODE_ENV === 'development';
    if (!isDev && section?.published === false) {
        redirect('/ben');
    }

    // If section not found, redirect to /ben
    if (!section) {
        redirect('/ben');
    }

    const IconComponent = iconMap[section.icon as keyof typeof iconMap];

    return (
        <main className="flex-1 container mx-auto py-16 md:py-24 px-4">
            {/* Breadcrumb navigation */}
            <nav className="max-w-4xl mx-auto mb-8 text-sm text-muted-foreground">
                <Link href="/" className="hover:text-foreground transition-colors">
                    Home
                </Link>
                {" / "}
                <Link href="/ben" className="hover:text-foreground transition-colors">
                    Ben
                </Link>
                {" / "}
                <span className="text-foreground">{section.title}</span>
            </nav>

            {/* Content wrapped in Card */}
            <Card className="max-w-4xl mx-auto shadow-lg">
                <CardHeader>
                    <CardTitle className="flex items-center text-3xl md:text-4xl">
                        {IconComponent && <IconComponent className="mr-4 h-10 w-10 text-primary" />}
                        {section.title}
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                    {section.paragraphs.map((paragraph, index) => (
                        <p key={index} className="text-lg text-muted-foreground leading-relaxed">
                            {paragraph}
                        </p>
                    ))}
                </CardContent>
            </Card>
        </main>
    );
}
