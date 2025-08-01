import {
    Table,
    TableHeader,
    TableBody,
    TableRow,
    TableHead,
    TableCell,
  } from "@/components/ui/table";
  import { Button } from "@/components/ui/button";
  import { Badge } from "@/components/ui/badge";
  import { BookOpen, Database, FileText } from "lucide-react";
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
      },
  ];
  
  export default function PublicationsPage() {
    return (
      <div className="container py-16 md:py-24">
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold font-headline">Publications</h1>
          <p className="text-lg text-muted-foreground mt-2">A list of my research publications and conference presentations.</p>
        </div>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="w-[120px] font-bold">Status</TableHead>
                <TableHead className="text-right w-[280px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {publications.map((pub, index) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
                  <TableCell>
                    <Badge variant={pub.status === 'Published' ? 'default' : 'secondary'} className="capitalize">
                      {pub.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    {pub.links.publication && (
                      <Button variant="outline" size="sm" asChild>
                        <a href={pub.links.publication} target="_blank" rel="noopener noreferrer">
                          <BookOpen className="mr-2 h-4 w-4" />
                          Publication
                        </a>
                      </Button>
                    )}
                    {pub.links.dataset && (
                      <Button variant="outline" size="sm" asChild>
                        <a href={pub.links.dataset} target="_blank" rel="noopener noreferrer">
                          <Database className="mr-2 h-4 w-4" />
                          Dataset
                        </a>
                      </Button>
                    )}
                    {pub.links.preprint && (
                      <Button variant="outline" size="sm" asChild>
                        <a href={pub.links.preprint} target="_blank" rel="noopener noreferrer">
                          <FileText className="mr-2 h-4 w-4" />
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
      </div>
    );
  }