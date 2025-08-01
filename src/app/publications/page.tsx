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
  import publicationsData from "../../../public/data/publications.json";
  import adsPublications from "../../../public/data/ads_publications.json";

  
  export default function PublicationsPage() {
    const techReports = adsPublications.filter(pub => pub.publication_type === "techreport");

    const sortedRefereedPublications = [...publicationsData.refereedPublications].sort((a, b) => b.year - a.year);
    const sortedDatasets = [...publicationsData.datasets].sort((a, b) => b.year - a.year);
    const sortedConferenceProceedings = [...publicationsData.conferenceProceedings].sort((a, b) => b.year - a.year);
    const sortedConferencePresentations = [...publicationsData.conferencePresentations].sort((a, b) => b.year - a.year);
    const sortedWhitePapers = [...techReports].sort((a, b) => parseInt(b.year) - parseInt(a.year));
    const sortedPrePrints = [...publicationsData.prePrints].sort((a, b) => b.year - a.year);

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
                  <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors.join(', ')}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
                  <TableCell className="text-right space-x-2">
                    {pub.url && (
                      <Button variant="outline" size="sm" asChild>
                        <a href={pub.url} target="_blank" rel="noopener noreferrer">
                          <BookOpen className="mr-2 h-4 w-4" />
                          Publication
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