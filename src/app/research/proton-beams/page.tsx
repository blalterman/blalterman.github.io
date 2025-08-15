
import { ResearchFigure } from '@/components/research-figure';
import { loadJSONData } from '@/lib/data-loader';
import { Metadata, ResolvingMetadata } from 'next';

type Props = {
    params: { slug: string };
};

const pageSlug = 'proton-beams';
const pageTitle = 'Proton Beams';

export async function generateMetadata(
    { params }: Props,
    parent: ResolvingMetadata
): Promise<Metadata> {
    const paragraphs = loadJSONData<Record<string, string>>('research-paragraphs.json');
    const paragraph = paragraphs[pageSlug];

    return {
        title: `${pageTitle} | B. L. Alterman`,
        description: paragraph,
    };
}

export default function ProtonBeamsPage() {
    const paragraphs = loadJSONData<Record<string, string>>('research-paragraphs.json');
    const figuresData = loadJSONData<any[]>('research-figures-with-captions.json');
    
    const pageData = figuresData.find((p: any) => p.slug === pageSlug);
    const paragraph = paragraphs[pageSlug];
    const figure = pageData?.figure;
    
    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <h1 className="font-headline">{pageTitle}</h1>
            <p className="text-lg text-muted-foreground mt-4">
                {paragraph}
            </p>
            <p className="text-sm text-muted-foreground mt-4">
                Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
            </p>
            {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
        </main>
    );
}
