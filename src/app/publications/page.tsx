import { PublicationsList } from "@/components/publications-list";

// This is a placeholder and not used in the simplified component.
const stubPublications = [
    {
        type: "article" as const,
        pubs: [
            {
                "bibcode": "2023A&A...676A..36L",
                "title": "First results from the Solar Orbiter Heavy Ion Sensor",
                "authors": ["Livi, S.", "Lepri, S. T.", "Raines, J. M."],
                "month": "August",
                "year": "2023",
                "journal": "Astronomy and Astrophysics",
                "publication_type": "article" as const,
                "citations": 19,
                "url": "https://dx.doi.org/10.1051/0004-6361/202346304"
            }
        ]
    }
];


export default function PublicationsPage() {
    // Passing stubbed data, but the component will be simplified to not use it for now
    return (
        <PublicationsList publications={stubPublications} />
    );
}
