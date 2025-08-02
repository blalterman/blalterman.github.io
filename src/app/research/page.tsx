import { FeaturedResearch } from "@/components/featured-research";
import fs from "fs";
import path from "path";

export default function ResearchPage() {
    const filePath = path.join(process.cwd(), 'data', 'research-projects.json');
    const researchProjects = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    return (
        <FeaturedResearch researchProjects={researchProjects} />
    );
}
