
import { Experience } from "@/components/experience";
import fs from "fs";
import path from "path";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Experience & Education | B. L. Alterman",
    description: "An overview of B. L. Alterman's professional positions and academic background, including roles at NASA, SwRI, and degrees from the University of Michigan and Macalester College.",
};

export default function ExperiencePage() {
    const educationPath = path.join(process.cwd(), 'public', 'data', 'education.json');
    const educationData = JSON.parse(fs.readFileSync(educationPath, 'utf-8'));

    const positionsPath = path.join(process.cwd(), 'public', 'data', 'positions.json');
    const positionsData = JSON.parse(fs.readFileSync(positionsPath, 'utf-8'));

    return (
        <Experience educationData={educationData} professionalData={positionsData} />
    );
}
