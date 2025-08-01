import Link from "next/link";

interface PublicationsListProps {
  // The publications prop is kept for future use but is ignored in this simplified version.
  publications: any[];
}

export function PublicationsList({ publications }: PublicationsListProps) {
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
            
            <div className="mb-12">
                <h3 className="text-2xl font-bold font-headline mb-6">Refereed Publications</h3>
                <div className="border rounded-lg p-4">
                    <p>Sample Publication Title</p>
                    <p className="text-sm text-muted-foreground">Author A, Author B</p>
                </div>
            </div>
        </section>
    );
}
