import { FeaturedResearch } from "@/components/featured-research";
import fs from "fs";
import path from "path";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Research | B. L. Alterman",
    description: "Explore featured research projects by B. L. Alterman, including studies on proton beams, helium abundance, space weather, and other topics in heliophysics.",
};

export default function ResearchPage() {
    const filePath = path.join(process.cwd(), 'data', 'research-projects.json');
    const researchProjects = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    return (
        <FeaturedResearch researchProjects={researchProjects} />
    );
}
