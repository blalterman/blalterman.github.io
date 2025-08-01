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
import { ExternalLink, BookOpen } from "lucide-react";
import Link from "next/link";

const publications = [
    {
        year: 2023,
        title: "Mapping Martian Surface Composition",
        journal: "Journal of Geophysical Research: Planets",
        status: "Published",
        links: {
            publication: "#",
            dataset: "#",
        }
    },
    {
        year: 2023,
        title: "Photochemical Haze Formation in the Atmosphere of TRAPPIST-1e",
        journal: "The Astrophysical Journal",
        status: "Published",
        links: {
            publication: "#",
        }
    },
    {
        year: 2022,
        title: "Exoplanet Atmosphere Characterization",
        journal: "Nature Astronomy",
        status: "Published",
        links: {
            publication: "#",
            dataset: "#",
        }
    },
    {
        year: 2022,
        title: "Modeling Galactic Chemical Evolution",
        journal: "Monthly Notices of the Royal Astronomical Society",
        status: "Published",
        links: {
            publication: "#",
            dataset: "#",
        }
    },
    {
        year: 2021,
        title: "A Search for Technosignatures Around Cool Stars",
        journal: "The Astronomical Journal",
        status: "Published",
        links: {
            publication: "#",
        }
    },
    {
        year: 2020,
        title: "Constraints on the Abundance of Primordial Black Holes",
        journal: "Physical Review D",
        status: "Published",
        links: {
            publication: "#",
        }
    },
    {
      year: 2024,
      title: "The Role of Magnetic Fields in Star Formation",
      journal: "Science",
      status: "In Review",
      links: {
        preprint: "#",
      }
    }
];

export function PublicationsList() {
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
                <div className="grid grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-2 mt-4 text-sm">
                    <p><strong>h-index:</strong> 15</p>
                    <p><strong>Total papers:</strong> 133</p>
                    <p><strong>Total citations:</strong> 741</p>
                    <p><strong>Refereed papers:</strong> 32</p>
                    <p><strong>Refereed citations:</strong> 730</p>
                </div>
            </div>
            <div className="border rounded-lg">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-[100px]">Year</TableHead>
                            <TableHead>Title</TableHead>
                            <TableHead>Journal / Venue</TableHead>
                            <TableHead className="text-center">Status</TableHead>
                            <TableHead className="text-right">Links</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {publications.sort((a, b) => b.year - a.year).map((pub) => (
                            <TableRow key={pub.title}>
                                <TableCell className="font-medium">{pub.year}</TableCell>
                                <TableCell className="font-semibold">{pub.title}</TableCell>
                                <TableCell>{pub.journal}</TableCell>
                                <TableCell className="text-center">
                                    <Badge variant={pub.status === 'Published' ? 'secondary' : 'outline'}>
                                        {pub.status}
                                    </Badge>
                                </TableCell>
                                <TableCell className="text-right space-x-2">
                                    {pub.links.publication && (
                                        <Button variant="outline" size="sm" asChild>
                                            <a href={pub.links.publication} target="_blank">
                                                <BookOpen className="mr-2 h-4 w-4" />
                                                Publication
                                            </a>
                                        </Button>
                                    )}
                                    {pub.links.dataset && (
                                        <Button size="sm" asChild>
                                            <a href={pub.links.dataset} target="_blank">
                                                <ExternalLink className="mr-2 h-4 w-4" />
                                                Dataset
                                            </a>
                                        </Button>
                                    )}
                                     {pub.links.preprint && (
                                        <Button variant="outline" size="sm" asChild>
                                            <a href={pub.links.preprint} target="_blank">
                                                <BookOpen className="mr-2 h-4 w-4" />
                                                Preprint
                                            </a>
                                        </Button>
                                    )}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>
        </section>
    );
}
