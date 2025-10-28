import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Telescope, Compass, HeartHandshake } from "lucide-react";
import { loadJSONData } from "@/lib/data-loader";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "B. L. Alterman",
    description: "Learn about Ben's research vision and team-building philosophy.",
};

interface BenSection {
    heading: string;
    icon: string;
    paragraphs: string[];
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

    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <div className="text-center mb-12">
                <h1 className="font-headline">{benData.heading}</h1>
                <p className="text-lg text-muted-foreground mt-2">
                    {benData.tagline}
                </p>
            </div>

            <div className="max-w-4xl mx-auto space-y-8">
                {benData.sections.map((section) => {
                    const IconComponent = iconMap[section.icon as keyof typeof iconMap];

                    return (
                        <Card key={section.heading} className="shadow-lg">
                            <CardHeader>
                                <CardTitle className="flex items-center text-2xl">
                                    {IconComponent && <IconComponent className="mr-3 h-6 w-6 text-primary" />}
                                    {section.heading}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {section.paragraphs.map((paragraph, index) => (
                                    <p key={index} className="text-lg text-muted-foreground">
                                        {paragraph}
                                    </p>
                                ))}
                            </CardContent>
                        </Card>
                    );
                })}
            </div>
        </main>
    );
}
