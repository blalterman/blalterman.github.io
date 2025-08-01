
import fs from 'fs';
import path from 'path';
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
  
  export default function PublicationsPage() {
    const metricsPath = path.join(process.cwd(), 'public', 'data', 'ads_metrics.json');
    const adsMetrics = JSON.parse(fs.readFileSync(metricsPath, 'utf-8'));

    const publicationsPath = path.join(process.cwd(), 'public', 'data', 'ads_publications.json');
    const adsPublications = JSON.parse(fs.readFileSync(publicationsPath, 'utf-8'));


    if (!adsMetrics || !adsPublications.length) {
      return (
        <div className="container mx-auto py-16 md:py-24 text-center">
          <p>Loading publication data...</p>
        </div>
      );
    }

    const techReports = adsPublications.filter((pub: any) => pub.publication_type === "techreport");
    const eprints = adsPublications.filter((pub: any) => pub.publication_type === "eprint");
    const datasets = adsPublications.filter((pub: any) => pub.publication_type === "dataset");
    const inproceedings = adsPublications.filter((pub: any) => pub.publication_type === "inproceedings");
    const articles = adsPublications.filter((pub: any) => pub.publication_type === "article");
    const abstracts = adsPublications.filter((pub: any) => pub.publication_type === "abstract");
    const phdThesis = adsPublications.filter((pub: any) => pub.publication_type === "phdthesis");


    const sortedRefereedPublications = [...articles].sort((a, b) => parseInt(b.year.substring(0, 4)) - parseInt(a.year.substring(0, 4)));
    const sortedDatasets = [...datasets].sort((a, b) => parseInt(b.year.substring(0, 4)) - parseInt(a.year.substring(0, 4)));
    const sortedConferenceProceedings = [...inproceedings].sort((a, b) => parseInt(a.year) - parseInt(b.year));
    const sortedConferencePresentations = [...abstracts].sort((a, b) => parseInt(b.year.substring(0, 4)) - parseInt(a.year.substring(0, 4)));
    const sortedWhitePapers = [...techReports].sort((a, b) => parseInt(a.year) - parseInt(b.year));
    const sortedPrePrints = [...eprints].sort((a, b) => parseInt(a.year.substring(0, 4)) - parseInt(a.year.substring(0, 4)));
    const sortedPhdThesis = [...phdThesis].sort((a, b) => parseInt(a.year.substring(0, 4)) - parseInt(a.year.substring(0, 4)));

    return (
      <div className="container mx-auto py-16 md:py-24">
        <div className="text-center mb-12">
          <h1 className="text-3xl md:text-4xl font-bold font-headline">Publications</h1>
          <p className="text-lg text-muted-foreground mt-2">A list of my research publications and conference presentations.</p>
        </div>
        <div className="flex justify-center flex-wrap space-x-8 mb-12">
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
            <h2 className="text-2xl font-bold font-headline mt-8">PhD Thesis</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg">
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
                  {sortedPhdThesis.map((pub: any, index: number) => (
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
        
        <h2 className="text-2xl font-bold font-headline mt-8">Refereed Publications</h2>
        <div className="border rounded-lg overflow-hidden shadow-lg">
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
              {sortedRefereedPublications.map((pub: any, index: number) => (
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

        {sortedDatasets.length > 0 && (
          <>
            <h2 className="text-2xl font-bold font-headline mt-8">Datasets</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg">
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
                  {sortedDatasets.map((pub: any, index: number) => (
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
            <h2 className="text-2xl font-bold font-headline mt-8">Conference Proceedings</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg">
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
                  {sortedConferenceProceedings.map((pub: any, index: number) => (
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
            <h2 className="text-2xl font-bold font-headline mt-8">Conference Presentations</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg">
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
                  {sortedConferencePresentations.map((pub: any, index: number) => (
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
            <h2 className="text-2xl font-bold font-headline mt-8">White Papers</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg">
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
                  {sortedWhitePapers.map((pub: any, index: number) => (
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
            <h2 className="text-2xl font-bold font-headline mt-8">Pre-Prints</h2>
            <div className="border rounded-lg overflow-hidden shadow-lg">
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
                  {sortedPrePrints.map((pub: any, index: number) => (
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
