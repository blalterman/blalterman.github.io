"use client";

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Briefcase, GraduationCap } from "lucide-react";

interface Education {
    Institution: string;
    Department: string;
    Location: string;
    Dates: string;
}

interface Position {
    Company: string;
    "Position Title": string;
    Dates: string;
    Location: string;
}

export function Experience() {
    const [educationData, setEducationData] = useState<Education[]>([]);
    const [professionalData, setProfessionalData] = useState<Position[]>([]);

    useEffect(() => {
        async function fetchData() {
            try {
                const eduResponse = await fetch('/data/education.json');
                const eduData = await eduResponse.json();
                setEducationData(eduData);

                const profResponse = await fetch('/data/positions.json');
                const profData = await profResponse.json();
                setProfessionalData(profData);
            } catch (error) {
                console.error("Failed to fetch experience data", error);
            }
        }
        fetchData();
    }, []);

    return (
        <section id="experience" className="container py-16 md:py-24">
            <div className="text-center mb-16">
                <h2 className="text-3xl md:text-4xl font-bold font-headline">Experience & Education</h2>
                <p className="text-lg text-muted-foreground mt-2">My academic journey and professional background.</p>
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
                                    <CardTitle>{edu.Institution}</CardTitle>
                                    <CardDescription>{edu.Department}</CardDescription>
                                    <p className="text-sm text-muted-foreground pt-1">{edu.Dates}</p>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm">{edu.Location}</p>
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
                                     <p className="text-sm text-muted-foreground pt-1">{job.Dates}</p>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm">{job.Location}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
