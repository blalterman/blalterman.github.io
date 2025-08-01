import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { BookOpen } from "lucide-react";

const publications = [
  {
    title: "Defining the Middle Corona",
    authors: "West, Matthew J., Seaton, Daniel B., Wexler, David B., et al.",
    journal: "Solar Physics",
    year: "2023",
    url: "https://dx.doi.org/10.1007/s11207-023-02170-1"
  },
  {
    title: "The Trans-Heliospheric Survey. Radial trends in plasma parameters across the heliosphere",
    authors: "Maruca, Bennett A., Qudsi, Ramiz A., Alterman, B. L., et al.",
    journal: "Astronomy and Astrophysics",
    year: "2023",
    url: "https://dx.doi.org/10.1051/0004-6361/202345951"
  },
  {
    title: "Majority of Solar Wind Intervals Support Ion-Driven Instabilities",
    authors: "Klein, K. G., Alterman, B. L., Stevens, M. L., Vech, D., Kasper, J. C.",
    journal: "Physical Review Letters",
    year: "2018",
    url: "https://dx.doi.org/10.1103/PhysRevLett.120.205102"
  }
];

export function PublicationsList() {
  return (
    <section id="publications" className="container py-16 md:py-24">
      <div className="text-center mb-12">
        <h2 className="text-3xl md:text-4xl font-bold font-headline">Publications</h2>
        <p className="text-lg text-muted-foreground mt-2">A selection of my key research papers.</p>
      </div>
      <div className="space-y-8">
        {publications.map((pub, index) => (
          <Card key={index} className="shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader>
              <CardTitle>{pub.title}</CardTitle>
              <CardDescription>{pub.authors}</CardDescription>
            </CardHeader>
            <CardContent className="flex justify-between items-center">
              <p className="text-sm text-muted-foreground">{pub.journal}, {pub.year}</p>
              <Button asChild variant="outline">
                <Link href={pub.url} target="_blank">
                  <BookOpen className="mr-2 h-4 w-4" />
                  Read Paper
                </Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
