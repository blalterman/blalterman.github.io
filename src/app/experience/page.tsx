
import { Experience } from "@/components/experience";
import { loadJSONData } from "@/lib/data-loader";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Experience & Education | B. L. Alterman",
    description: "An overview of B. L. Alterman's professional positions and academic background, including roles at NASA, SwRI, and degrees from the University of Michigan and Macalester College.",
};

interface Education {
    Institution: string;
    Department: string;
    Location: string;
    Dates: string;
    Degree: string;
}

interface Position {
    Company: string;
    "Position Title": string;
    Dates: string;
    Location: string;
}

export default function ExperiencePage() {
    const educationData = loadJSONData<Education[]>('education.json');
    const positionsData = loadJSONData<Position[]>('positions.json');

    return (
        <Experience educationData={educationData} professionalData={positionsData} />
    );
}
