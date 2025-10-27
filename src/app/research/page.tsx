
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

interface ResearchPageData {
    heading: string;
    tagline: string;
}

export default function ResearchPage() {
    const researchProjects = loadJSONData<ResearchProject[]>('research-projects.json');
    const researchPageData = loadJSONData<ResearchPageData>('research-page.json');

    // Shuffle research projects at build time to avoid implied priority hierarchy
    // Order will be identical for all visitors until next deployment
    const shuffledProjects = [...researchProjects].sort(() => Math.random() - 0.5);

    return (
        <FeaturedResearch
            heading={researchPageData.heading}
            tagline={researchPageData.tagline}
            researchProjects={shuffledProjects}
        />
    );
}
