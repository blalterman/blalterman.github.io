
import { FeaturedResearch } from "@/components/featured-research";
import { loadJSONData } from "@/lib/data-loader";
import { filterPublishedProjects } from "@/lib/research-utils";
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
    published?: boolean;
}

interface ResearchPageData {
    heading: string;
    tagline: string;
}

export default function ResearchPage() {
    const researchProjects = loadJSONData<ResearchProject[]>('research-projects.json');
    const researchPageData = loadJSONData<ResearchPageData>('research-page.json');

    // Filter published projects (environment-aware: shows all in dev, only published in production)
    const publishedProjects = filterPublishedProjects(researchProjects);

    // Shuffle research projects at build time to avoid implied priority hierarchy
    // Order will be identical for all visitors until next deployment
    const shuffledProjects = [...publishedProjects].sort(() => Math.random() - 0.5);

    return (
        <FeaturedResearch
            heading={researchPageData.heading}
            tagline={researchPageData.tagline}
            researchProjects={shuffledProjects}
        />
    );
}
