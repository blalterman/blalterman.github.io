import { PublicationsList } from "@/components/publications-list";
import { ads_publications } from "@/lib/publications-data";

type PublicationType = "phdthesis" | "article" | "inproceedings" | "abstract" | "techreport" | "eprint" | "dataset" | "phdthesis" | "bookreview" | "catalog" | "inbook" | "mastersthesis" | "misc" | "pressrelease" | "proposal" | "software";

interface Publication {
  bibcode: string;
  year: string;
  title: string;
  authors: string[];
  journal: string;
  publication_type: PublicationType;
  citations: number;
  url: string;
}

interface PublicationGroup {
    type: PublicationType;
    pubs: Publication[];
}

async function getPublications(): Promise<Publication[]> {
  // Data is imported directly from the data file.
  return ads_publications as Publication[];
}

export default async function PublicationsPage() {
    const publications = await getPublications();
    
    // Group publications by type
    const publicationGroups = publications.reduce((acc, pub) => {
        const type = pub.publication_type;
        if (!acc[type]) {
            acc[type] = [];
        }
        acc[type].push(pub);
        return acc;
    }, {} as Record<PublicationType, Publication[]>);

    // Sort publications within each group and create the final structure
    const sortedPublicationGroups: PublicationGroup[] = Object.entries(publicationGroups)
        .map(([type, pubs]) => ({
            type: type as PublicationType,
            pubs: pubs.sort((a, b) => {
                const yearA = parseInt(a.year, 10);
                const yearB = parseInt(b.year, 10);
                if (yearB !== yearA) {
                    return yearB - yearA;
                }
                // Fallback to sorting by bibcode if years are the same
                return b.bibcode.localeCompare(a.bibcode);
            }),
        }));

    return (
        <PublicationsList publications={sortedPublicationGroups} />
    );
}
