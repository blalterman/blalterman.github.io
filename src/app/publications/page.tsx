import {
    Table,
    TableHeader,
    TableBody,
    TableRow,
    TableHead,
    TableCell,
  } from "@/components/ui/table";
  import { Button } from "@/components/ui/button";
  import { BookOpen, Database, FileText } from "lucide-react";
  import adsMetrics from "../../../public/data/ads_metrics.json";
  
  const refereedPublications = [
      {
          year: 2023,
          title: "Mapping Martian Surface Composition",
          authors: "John Doe, Jane Smith",
          journal: "Journal of Geophysical Research: Planets",
          links: {
              publication: "#",
              dataset: "#",
          }
      },
      {
          year: 2023,
          title: "Photochemical Haze Formation in the Atmosphere of TRAPPIST-1e",
          authors: "Peter Jones, Mary Brown",
          journal: "The Astrophysical Journal",
          links: {
              publication: "#",
          }
      },
      {
          year: 2022,
          title: "Exoplanet Atmosphere Characterization",
          authors: "David Green, Sarah White",
          journal: "Nature Astronomy",
          links: {
              publication: "#",
              dataset: "#",
          }
      },
      {
          year: 2022,
          title: "Modeling Galactic Chemical Evolution",
          authors: "Michael Black, Emily Blue",
          journal: "Monthly Notices of the Royal Astronomical Society",
          links: {
              publication: "#",
              dataset: "#",
          }
      },
      {
          year: 2021,
          title: "A Search for Technosignatures Around Cool Stars",
          authors: "Chris Grey, Olivia Pink",
          journal: "The Astronomical Journal",
          links: {
              publication: "#",
          }
      },
      {
          year: 2020,
          title: "Constraints on the Abundance of Primordial Black Holes",
          authors: "Daniel Cyan, Sophia Magenta",
          journal: "Physical Review D",
          links: {
              publication: "#",
          }
      },
      {
        year: 2024,
        title: "The Role of Magnetic Fields in Star Formation",
        authors: "Matthew Yellow, Isabella Red",
        journal: "Science",
        links: {
          preprint: "#",
        }
      },
  ];

  const datasets = [
    {
      year: 2023,
      title: "Martian Surface Imagery Dataset",
      authors: "Data Curator One, Data Curator Two",
      journal: "", // Datasets may not have a journal
      links: {
        dataset: "#",
      },
    },
    {
      year: 2022,
      title: "Exoplanet Atmospheric Data",
      authors: "Data Provider One",
      journal: "",
      links: {
        dataset: "#",
      },
    },
  ];

  const conferenceProceedings = [
    {
      year: 2023,
      title: "Proceedings of the 1st International Conference on Space",
      authors: "Author One, Author Two",
      journal: "Space Conference Proceedings",
      links: {
        publication: "#",
      },
    },
    {
      year: 2022,
      title: "Proceedings of the 15th Annual Astronomy Symposium",
      authors: "Author Three, Author Four",
      journal: "Astronomy Symposium Proceedings",
      links: {
        publication: "#",
      },
    },
  ];

  const conferencePresentations = [
    {
      year: 2024,
      title: "Presented research on exoplanet atmospheres at conference",
      authors: "Presenter One",
      journal: "Conference Name",
      links: {
        preprint: "#",
      },
    },
    {
      year: 2023,
      title: "Poster presentation on galactic modeling",
      authors: "Presenter Two",
      journal: "Another Conference Name",
      links: {
        dataset: "#",
      },
    },
  ];

  const whitePapers = [
    {
      year: 2023,
      title: "White paper on future space missions",
      authors: "Committee Member One, Committee Member Two",
      journal: "", // White papers may not have a journal
      links: {
        publication: "#",
      },
    },
    {
      year: 2022,
      title: "Recommendations for data analysis in astrophysics",
      authors: "Working Group Lead",
      journal: "",
      links: {
        publication: "#",
      },
    },
  ];

  const prePrints = [
    {
      year: 2024,
      title: "Pre-print on new telescope technology",
      authors: "Researcher A, Researcher B",
      journal: "arXiv", // Pre-prints often have arXiv as journal
      links: {
        preprint: "#",
      },
    },
    {
      year: 2023,
      title: "Pre-print on dark matter research",
      authors: "Researcher C",
      journal: "arXiv",
      links: {
        preprint: "#",
      },
    },
  ];
  
  export default function PublicationsPage() {
    const sortedRefereedPublications = [...refereedPublications].sort((a, b) => b.year - a.year);
    const sortedDatasets = [...datasets].sort((a, b) => b.year - a.year);
    const sortedConferenceProceedings = [...conferenceProceedings].sort((a, b) => b.year - a.year);
    const sortedConferencePresentations = [...conferencePresentations].sort((a, b) => b.year - a.year);
    const sortedWhitePapers = [...whitePapers].sort((a, b) => b.year - a.year);
    const sortedPrePrints = [...prePrints].sort((a, b) => b.year - a.year);

    return (
      <div className="container py-16 md:py-24">
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold font-headline">Publications</h1>
          <p className="text-lg text-muted-foreground mt-2">A list of my research publications and conference presentations.</p>
        </div>
        <div className="flex justify-center space-x-8 mb-12">
          <div className="flex flex-col items-center">
            <span className="text-2xl font-bold">{adsMetrics["indicators"]["h"]}</span>
            <span className="text-sm text-muted-foreground">h-index</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-2xl font-bold">{adsMetrics["basic stats"]["number of papers"]}</span>
            <span className="text-sm text-muted-foreground">Total papers</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-2xl font-bold">{adsMetrics["citation stats"]["total number of citations"]}</span>
            <span className="text-sm text-muted-foreground">Total citations</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-2xl font-bold">{adsMetrics["basic stats refereed"]["number of papers"]}</span>
            <span className="text-sm text-muted-foreground">Refereed papers</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="text-2xl font-bold">{adsMetrics["citation stats refereed"]["total number of citations"]}
            </span>
            <span className="text-sm text-muted-foreground">Refereed citations</span>
          </div>
        </div>
        
        <h2 className="text-2xl font-bold font-headline mt-8">Refereed Publications</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="text-right w-[280px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedRefereedPublications.map((pub, index) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
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

        <h2 className="text-2xl font-bold font-headline mt-8">Datasets</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="text-right w-[280px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedDatasets.map((pub, index) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
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

        <h2 className="text-2xl font-bold font-headline mt-8">Conference Proceedings</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="text-right w-[280px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedConferenceProceedings.map((pub, index) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
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

        <h2 className="text-2xl font-bold font-headline mt-8">Conference Presentations</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="text-right w-[280px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedConferencePresentations.map((pub, index) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
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

        <h2 className="text-2xl font-bold font-headline mt-8">White Papers</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="text-right w-[280px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedWhitePapers.map((pub, index) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
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

        <h2 className="text-2xl font-bold font-headline mt-8">Pre-Prints</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="text-right w-[280px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedPrePrints.map((pub, index) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
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