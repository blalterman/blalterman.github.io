import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button";
import { ExternalLink } from "lucide-react";
import Link from "next/link";

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

interface PublicationGroup {
    type: PublicationType;
    pubs: Publication[];
}

interface PublicationsListProps {
  publications: PublicationGroup[];
}

const publicationTypeTitles: Record<PublicationType, string> = {
    phdthesis: "PhD Thesis",
    article: "Refereed Publications",
    inproceedings: "Conference Proceedings",
    abstract: "Conference Presentations",
    techreport: "White Papers",
    eprint: "Pre-Prints",
    dataset: "Datasets"
};

const customOrder: PublicationType[] = ["phdthesis", "article", "inproceedings", "abstract", "techreport", "eprint", "dataset"];


export function PublicationsList({ publications }: PublicationsListProps) {
    const sortedPublications = publications.sort((a, b) => customOrder.indexOf(a.type) - customOrder.indexOf(b.type));

    return (
        <section id="publications" className="container py-16 md:py-24">
            <div className="text-center mb-12">
                <h2 className="text-3xl md:text-4xl font-bold font-headline">Publications</h2>
                <p className="text-lg text-muted-foreground mt-2">A comprehensive list of my research papers and preprints.</p>
            </div>
            <div className="text-center mb-12 text-muted-foreground max-w-3xl mx-auto">
                <p>
                    This page is automatically generated using data from{' '}
                    <Link
                        href="https://ui.adsabs.harvard.edu/search/p_=0&q=orcid%3A0000-0001-6673-3432&sort=date%20desc%2C%20bibcode%20desc"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary hover:underline"
                    >
                        NASA ADS
                    </Link>
                    {' '}and is updated weekly.
                </p>
                <div className="flex flex-wrap justify-center gap-x-4 gap-y-2 mt-4 text-sm">
                    <p><strong>h-index:</strong> 15</p>
                    <p><strong>Total papers:</strong> 133</p>
                    <p><strong>Total citations:</strong> 741</p>
                    <p><strong>Refereed papers:</strong> 32</p>
                    <p><strong>Refereed citations:</strong> 730</p>
                </div>
            </div>
            
            {sortedPublications.map(({ type, pubs }) => (
                pubs.length > 0 && (
                    <div key={type} className="mb-12">
                         <h3 className="text-2xl font-bold font-headline mb-6">{publicationTypeTitles[type]}</h3>
                        <div className="border rounded-lg overflow-hidden">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead className="w-[80px]">Year</TableHead>
                                        <TableHead>Title & Authors</TableHead>
                                        <TableHead>Journal / Venue</TableHead>
                                        <TableHead className="text-center w-[120px]">Citations</TableHead>
                                        <TableHead className="text-right w-[120px]">Link</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {pubs.map((pub) => (
                                        <TableRow key={pub.bibcode}>
                                            <TableCell className="font-medium">{pub.year}</TableCell>
                                            <TableCell>
                                                <p className="font-semibold">{pub.title}</p>
                                                <p className="text-sm text-muted-foreground mt-1">{pub.authors.join(', ')}</p>
                                            </TableCell>
                                            <TableCell>{pub.journal}</TableCell>
                                            <TableCell className="text-center">
                                                <Badge variant="secondary">{pub.citations}</Badge>
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <Button variant="ghost" size="sm" asChild>
                                                    <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                                        View
                                                        <ExternalLink className="ml-2 h-4 w-4" />
                                                    </a>
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>
                    </div>
                )
            ))}
        </section>
    );
}
