import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Telescope, Compass, HeartHandshake, ArrowRight } from "lucide-react";
import { loadJSONData } from "@/lib/data-loader";
import { filterPublishedProjects } from "@/lib/research-utils";
import { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
    title: "B. L. Alterman",
    description: "Learn about Ben's research vision and team-building philosophy.",
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
};

export default function BenPage() {
    const benData = loadJSONData<BenPageData>('ben-page.json');

    // Filter published sections (dev shows all, production filters)
    const publishedSections = filterPublishedProjects(benData.sections);

    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <div className="text-center mb-12">
                <h1 className="font-headline">{benData.heading}</h1>
                <p className="text-lg text-muted-foreground mt-2">
                    {benData.tagline}
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {publishedSections.map((section) => {
                    const IconComponent = iconMap[section.icon as keyof typeof iconMap];

                    return (
                        <Card
                            key={section.slug}
                            className="flex flex-col overflow-hidden shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
                        >
                            <div className="flex flex-col flex-1 p-6">
                                <CardHeader className="p-0 mb-4">
                                    <CardTitle className="flex items-center text-2xl">
                                        {IconComponent && <IconComponent className="mr-3 h-6 w-6 text-primary" />}
                                        {section.title}
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="p-0 flex-1">
                                    <CardDescription className="text-base">
                                        {section.excerpt}
                                    </CardDescription>
                                </CardContent>
                                <CardFooter className="p-0 pt-4 flex justify-end gap-2">
                                    <Button asChild>
                                        <Link href={`/ben/${section.slug}`}>
                                            Details
                                            <ArrowRight className="ml-2 h-4 w-4" />
                                        </Link>
                                    </Button>
                                </CardFooter>
                            </div>
                        </Card>
                    );
                })}
            </div>
        </main>
    );
}
