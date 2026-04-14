
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Award, Briefcase, GraduationCap } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

interface Education {
    Institution: string;
    Department: string;
    Location: string;
    Dates: string;
    Degree: string;
    dissertation?: {
        title: string;
        url: string;
    };
    advisors?: string[];
}

interface Position {
    Company: string;
    "Position Title": string;
    Dates: string;
    Location: string;
}

interface HonorItem {
    name: string;
    url?: string;
    active?: boolean;
}

interface Honor {
    title: string;
    organization: string;
    year: string;
    url?: string;
    description?: string;
    items?: HonorItem[];
    published?: boolean;
    category: "honor" | "leadership";
}

interface ExperienceProps {
    heading: string;
    tagline: string;
    educationData: Education[];
    professionalData: Position[];
    honorsData: Honor[];
}

export function Experience({ heading, tagline, educationData, professionalData, honorsData }: ExperienceProps) {
    const publishedHonors = honorsData.filter((h) => h.published !== false);
    return (
        <section id="experience" className="container mx-auto py-16 md:py-24">
            <div className="text-center mb-16">
                <h2 className="font-headline">{heading}</h2>
                <p className="text-lg text-muted-foreground mt-2">{tagline}</p>
                <Button variant="outline" asChild className="mt-4">
                    <Link href="/Alterman-CV.pdf" target="_blank" rel="noopener noreferrer">
                        Download My CV (PDF)
                    </Link>
                </Button>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <div>
                    <h3 className="flex items-center text-2xl font-bold mb-6">
                        <GraduationCap className="mr-3 h-7 w-7 text-primary" />
                        Education
                    </h3>
                    <div className="space-y-8">
                        {educationData.map((edu) => (
                            <Card key={edu.Institution} className="shadow-lg">
                                <CardHeader>
                                    <CardTitle>{edu.Degree}</CardTitle>
                                    <CardDescription>{edu.Institution}</CardDescription>
                                    <p className="text-sm text-muted-foreground pt-1">{edu.Department}</p>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-muted-foreground pt-1">{edu.Dates}</p>
                                    <p className="text-sm">{edu.Location}</p>
                                    {edu.dissertation && (
                                        <p className="text-sm mt-3">
                                            <Link href={edu.dissertation.url} className="italic text-primary hover:underline">
                                                {edu.dissertation.title}
                                            </Link>
                                        </p>
                                    )}
                                    {edu.advisors && (
                                        <p className="text-sm text-muted-foreground mt-1">
                                            Advisors: {edu.advisors.join(" & ")}
                                        </p>
                                    )}
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
                <div>
                    <h3 className="flex items-center text-2xl font-bold mb-6">
                        <Briefcase className="mr-3 h-7 w-7 text-primary" />
                        Professional Positions
                    </h3>
                    <div className="space-y-8">
                        {professionalData.map((job) => (
                            <Card key={`${job["Position Title"]}-${job.Company}`} className="shadow-lg">
                                <CardHeader>
                                    <CardTitle>{job["Position Title"]}</CardTitle>
                                    <CardDescription>{job.Company}</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-muted-foreground pt-1">{job.Dates}</p>
                                    <p className="text-sm">{job.Location}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </div>

            {publishedHonors.length > 0 && (
                <div className="mt-16">
                    <h3 className="flex items-center text-2xl font-bold mb-6">
                        <Award className="mr-3 h-7 w-7 text-primary" />
                        Honors & Leadership
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {publishedHonors.map((honor) => (
                            <Card key={honor.title} className="shadow-lg h-full flex flex-col">
                                <CardHeader className="pb-2 flex-1">
                                    <CardTitle className="text-base">
                                        {honor.url ? (
                                            <a href={honor.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                                                {honor.title}
                                            </a>
                                        ) : (
                                            honor.title
                                        )}
                                    </CardTitle>
                                    <CardDescription>{honor.organization} &middot; {honor.year}</CardDescription>
                                </CardHeader>
                                {(honor.description || honor.items) && (
                                    <CardContent>
                                        {honor.description && (
                                            <p className="text-sm text-muted-foreground">{honor.description}</p>
                                        )}
                                        {honor.items && (
                                            <p className="text-sm text-muted-foreground">
                                                {honor.items.map((item, i) => (
                                                    <span key={item.name}>
                                                        {i > 0 && ", "}
                                                        {item.url ? (
                                                            <a href={item.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                                                                {item.name}
                                                            </a>
                                                        ) : (
                                                            item.name
                                                        )}
                                                        {item.active === false && (
                                                            <span className="text-xs"> (former)</span>
                                                        )}
                                                    </span>
                                                ))}
                                            </p>
                                        )}
                                    </CardContent>
                                )}
                            </Card>
                        ))}
                    </div>
                </div>
            )}
        </section>
    );
}
