import { PublicationsList } from "@/components/publications-list";

type PublicationType = "phdthesis" | "article" | "inproceedings" | "abstract" | "techreport" | "eprint" | "dataset" | "bookreview" | "catalog" | "inbook" | "mastersthesis" | "misc" | "pressrelease" | "proposal" | "software";

interface Publication {
  bibcode: string;
  year: string;
  title: string;
  authors: string[];
  journal: string;
  publication_type: PublicationType;
  citations: number;
  url: string;
  month?: string; // Added optional month property
}

interface PublicationGroup {
    type: PublicationType;
    pubs: Publication[];
}

const stubPublications: Publication[] = [
    {
        "bibcode": "2023A&A...676A..36L",
        "title": "First results from the Solar Orbiter Heavy Ion Sensor",
        "authors": ["Livi, S.", "Lepri, S. T.", "Raines, J. M."],
        "month": "August",
        "year": "2023",
        "journal": "Astronomy and Astrophysics",
        "publication_type": "article",
        "citations": 19,
        "url": "https://dx.doi.org/10.1051/0004-6361/202346304"
    },
    {
        "bibcode": "2025arXiv250418092A",
        "title": "The Evolution of Heavy Ion Abundances with Solar Activity",
        "authors": ["Alterman, B. L.", "Rivera, Y. J.", "Lepri, S. T."],
        "month": "April",
        "year": "2025",
        "journal": "arXiv e-prints",
        "publication_type": "eprint",
        "citations": 0,
        "url": "https://dx.doi.org/10.48550/arXiv.2504.18092"
    },
    {
        "bibcode": "2019PhDT.......121A",
        "title": "The significance of proton beams in the multiscale solar wind",
        "authors": ["Alterman, Benjamin L."],
        "month": "",
        "year": "2019",
        "journal": "Ph.D. Thesis",
        "publication_type": "phdthesis",
        "citations": 2,
        "url": "https://ui.adsabs.harvard.edu/abs/2019PhDT.......121A"
    }
];


// Group publications by type
const publicationGroups = stubPublications.reduce((acc, pub) => {
    const type = pub.publication_type;
    if (!acc[type]) {
        acc[type] = [];
    }
    acc[type].push(pub);
    return acc;
}, {} as Record<PublicationType, Publication[]>);

// Create the final structure and sort publications within each group
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

export default function PublicationsPage() {
    return (
        <PublicationsList publications={sortedPublicationGroups} />
    );
}