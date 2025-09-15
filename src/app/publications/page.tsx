
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
  import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
  import { Metadata } from 'next';
import { loadJSONData } from "@/lib/data-loader";
import { getPublicationsByType } from "@/lib/publication-utils";
import type { Publication } from "@/types/publication";

  export const metadata: Metadata = {
    title: "Publications | B. L. Alterman",
    description: "A comprehensive list of peer-reviewed articles, datasets, conference proceedings, and other publications by B. L. Alterman, with links to NASA/ADS.",
  };
  
  export default function PublicationsPage() {
    const adsMetrics = loadJSONData<any>('ads_metrics.json');
    const adsPublications = loadJSONData<Publication[]>('ads_publications.json');

    if (!adsMetrics || !adsPublications.length) {
      return (
        <div className="container mx-auto py-16 md:py-24 text-center">
          <p>Loading publication data...</p>
        </div>
      );
    }

    // Use centralized sorting functions for all publication types
    const sortedRefereedPublications = getPublicationsByType(adsPublications, "article");
    const sortedDatasets = getPublicationsByType(adsPublications, "dataset");
    const sortedConferenceProceedings = getPublicationsByType(adsPublications, "inproceedings");
    const sortedConferencePresentations = getPublicationsByType(adsPublications, "abstract");
    const sortedWhitePapers = getPublicationsByType(adsPublications, "techreport");
    const sortedPrePrints = getPublicationsByType(adsPublications, "eprint");
    const sortedPhdThesis = getPublicationsByType(adsPublications, "phdthesis");

    return (
      <div className="container mx-auto py-16 md:py-24">
        <div className="text-center mb-12">
          <h1 className="font-headline">Publications</h1>
          <p className="text-lg text-muted-foreground mt-2">A list of my research publications and conference presentations.</p>
        </div>
        <div className="flex justify-center flex-wrap gap-x-8 mb-12">
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

        {sortedPhdThesis.length > 0 && (
          <>
            <h2 className="text-2xl font-bold mt-8 text-center">PhD Thesis</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead className="w-[100px] font-bold">Year</TableHead>
                    <TableHead className="font-bold">Title</TableHead>
                    <TableHead className="font-bold">Authors</TableHead>
                    <TableHead className="font-bold">Journal</TableHead>
                    <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedPhdThesis.map((pub: Publication, index: number) => (
                    <TableRow key={index} className="hover:bg-muted/30">
                      <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                      <TableCell>{pub.title}</TableCell>
                      <TableCell>{pub.authors.join(', ')}</TableCell>
                      <TableCell>{pub.journal}</TableCell>
                      <TableCell className="text-right space-x-2">
                        {pub.url && (
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="outline" size="icon" asChild>
                                  <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                    <BookOpen className="h-4 w-4" />
                                  </a>
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Publication</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </>
        )}
        
        <h2 className="text-2xl font-bold mt-8 text-center">Refereed Publications</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                <TableHead className="text-center w-[100px] font-bold">Citations</TableHead>
                <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedRefereedPublications.map((pub: Publication, index: number) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors.join(', ')}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
                  <TableCell className="text-center">{pub.citations}</TableCell>
                  <TableCell className="text-right space-x-2">
                    {pub.url && (
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button variant="outline" size="icon" asChild>
                              <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                <BookOpen className="h-4 w-4" />
                              </a>
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Publication</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {sortedDatasets.length > 0 && (
          <>
            <h2 className="text-2xl font-bold mt-8 text-center">Datasets</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead className="w-[100px] font-bold">Year</TableHead>
                    <TableHead className="font-bold">Title</TableHead>
                    <TableHead className="font-bold">Authors</TableHead>
                    <TableHead className="font-bold">Journal</TableHead>
                    <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedDatasets.map((pub: Publication, index: number) => (
                    <TableRow key={index} className="hover:bg-muted/30">
                      <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                      <TableCell>{pub.title}</TableCell>
                      <TableCell>{pub.authors.join(', ')}</TableCell>
                      <TableCell>{pub.journal}</TableCell>
                      <TableCell className="text-right space-x-2">
                        {pub.url && (
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="outline" size="icon" asChild>
                                  <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                    <Database className="h-4 w-4" />
                                  </a>
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Dataset</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </>
        )}

        {sortedConferenceProceedings.length > 0 && (
          <>
            <h2 className="text-2xl font-bold mt-8 text-center">Conference Proceedings</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead className="w-[100px] font-bold">Year</TableHead>
                    <TableHead className="font-bold">Title</TableHead>
                    <TableHead className="font-bold">Authors</TableHead>
                    <TableHead className="font-bold">Journal</TableHead>
                    <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedConferenceProceedings.map((pub: Publication, index: number) => (
                    <TableRow key={index} className="hover:bg-muted/30">
                      <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                      <TableCell>{pub.title}</TableCell>
                      <TableCell>{pub.authors.join(', ')}</TableCell>
                      <TableCell>{pub.journal}</TableCell>
                      <TableCell className="text-right space-x-2">
                        {pub.url && (
                           <TooltipProvider>
                           <Tooltip>
                             <TooltipTrigger asChild>
                               <Button variant="outline" size="icon" asChild>
                                 <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                   <BookOpen className="h-4 w-4" />
                                 </a>
                               </Button>
                             </TooltipTrigger>
                             <TooltipContent>
                               <p>Publication</p>
                             </TooltipContent>
                           </Tooltip>
                         </TooltipProvider>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </>
        )}

        {sortedConferencePresentations.length > 0 && (
          <>
            <h2 className="text-2xl font-bold mt-8 text-center">Conference Presentations</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead className="w-[100px] font-bold">Year</TableHead>
                    <TableHead className="font-bold">Title</TableHead>
                    <TableHead className="font-bold">Authors</TableHead>
                    <TableHead className="font-bold">Journal</TableHead>
                    <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedConferencePresentations.map((pub: Publication, index: number) => (
                    <TableRow key={index} className="hover:bg-muted/30">
                      <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                      <TableCell>{pub.title}</TableCell>
                      <TableCell>{pub.authors.join(', ')}</TableCell>
                      <TableCell>{pub.journal}</TableCell>
                      <TableCell className="text-right space-x-2">
                        {pub.url && (
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="outline" size="icon" asChild>
                                  <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                    <FileText className="h-4 w-4" />
                                  </a>
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Presentation</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </>
        )}

        {sortedWhitePapers.length > 0 && (
          <>
            <h2 className="text-2xl font-bold mt-8 text-center">White Papers</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead className="w-[100px] font-bold">Year</TableHead>
                    <TableHead className="font-bold">Title</TableHead>
                    <TableHead className="font-bold">Authors</TableHead>
                    <TableHead className="font-bold">Journal</TableHead>
                    <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedWhitePapers.map((pub: Publication, index: number) => (
                    <TableRow key={index} className="hover:bg-muted/30">
                      <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                      <TableCell>{pub.title}</TableCell>
                      <TableCell>{pub.authors.join(', ')}</TableCell>
                      <TableCell>{pub.journal}</TableCell>
                      <TableCell className="text-right space-x-2">
                        {pub.url && (
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="outline" size="icon" asChild>
                                  <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                    <FileText className="h-4 w-4" />
                                  </a>
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Paper</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </>
        )}

        {sortedPrePrints.length > 0 && (
          <>
            <h2 className="text-2xl font-bold mt-8 text-center">Pre-Prints</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead className="w-[100px] font-bold">Year</TableHead>
                    <TableHead className="font-bold">Title</TableHead>
                    <TableHead className="font-bold">Authors</TableHead>
                    <TableHead className="font-bold">Journal</TableHead>
                    <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {sortedPrePrints.map((pub: Publication, index: number) => (
                    <TableRow key={index} className="hover:bg-muted/30">
                      <TableCell className="font-medium">{pub.year.substring(0, 4)}</TableCell>
                      <TableCell>{pub.title}</TableCell>
                      <TableCell>{pub.authors.join(', ')}</TableCell>
                      <TableCell>{pub.journal}</TableCell>
                      <TableCell className="text-right space-x-2">
                        {pub.url && (
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="outline" size="icon" asChild>
                                  <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                    <FileText className="h-4 w-4" />
                                  </a>
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Preprint</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </>
        )}
      </div>
    );
  }
