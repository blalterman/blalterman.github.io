
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

interface ExperiencePageData {
    heading: string;
    tagline: string;
}

export default function ExperiencePage() {
    const educationData = loadJSONData<Education[]>('education.json');
    const positionsData = loadJSONData<Position[]>('positions.json');
    const honorsData = loadJSONData<Honor[]>('honors.json');
    const experiencePageData = loadJSONData<ExperiencePageData>('experience-page.json');

    return (
        <Experience
            heading={experiencePageData.heading}
            tagline={experiencePageData.tagline}
            educationData={educationData}
            professionalData={positionsData}
            honorsData={honorsData}
        />
    );
}
