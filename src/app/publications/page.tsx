import { PublicationsList } from "@/components/publications-list";
import { ads_publications } from "@/lib/publications-data";

type PublicationType = "phdthesis" | "article" | "inproceedings" | "abstract" | "techreport" | "eprint" | "dataset";

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

async function getPublications(): Promise<Publication[]> {
  // Data is imported directly from the data file.
  // In a real-world scenario with a database or external API,
  // the fetch call would be here.
  return ads_publications as Publication[];
}


export default async function PublicationsPage() {
    const publications = await getPublications();
    
    const publicationGroups: Record<string, Publication[]> = {};

    publications.forEach(pub => {
        if (!publicationGroups[pub.publication_type]) {
            publicationGroups[pub.publication_type] = [];
        }
        publicationGroups[pub.publication_type].push(pub);
    });

    const sortedPublicationGroups = Object.entries(publicationGroups).map(([type, pubs]) => ({
        type: type as PublicationType,
        pubs: pubs.sort((a, b) => parseInt(b.year) - parseInt(a.year) || a.title.localeCompare(b.title)),
    }));

    return (
        <PublicationsList publications={sortedPublicationGroups} />
    );
}
