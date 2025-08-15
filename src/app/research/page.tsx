
import { FeaturedResearch } from "@/components/featured-research";
import { loadJSONData } from "@/lib/data-loader";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Research | B. L. Alterman",
    description: "Explore featured research projects by B. L. Alterman, including studies on proton beams, helium abundance, space weather, and other topics in heliophysics.",
};

interface ResearchProject {
    title: string;
    description: string;
    image: string;
    imageHint: string;
    slug: string;
}

export default function ResearchPage() {
    const researchProjects = loadJSONData<ResearchProject[]>('research-projects.json');

    return (
        <FeaturedResearch researchProjects={researchProjects} />
    );
}
