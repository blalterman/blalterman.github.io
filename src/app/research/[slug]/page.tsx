import { ResearchFigure } from '@/components/research-figure';
import { loadJSONData } from '@/lib/data-loader';
import { renderMathInText } from '@/lib/render-math';
import { Metadata, ResolvingMetadata } from 'next';

type Props = {
    params: Promise<{ slug: string }>;
};

export async function generateStaticParams() {
    const projects = loadJSONData<any[]>('research-projects.json');
    return projects.map((project) => ({
        slug: project.slug,
    }));
}

export async function generateMetadata(
    { params }: Props,
    parent: ResolvingMetadata
): Promise<Metadata> {
    const { slug } = await params;
    const projects = loadJSONData<any[]>('research-projects.json');
    const project = projects.find((p: any) => p.slug === slug);
    const paragraphs = loadJSONData<Record<string, string>>('research-paragraphs.json');
    const paragraph = paragraphs[slug];

    return {
        title: `${project?.title || 'Research'} | B. L. Alterman`,
        description: paragraph || project?.description,
    };
}

export default async function ResearchPage({ params }: { params: Promise<{ slug: string }> }) {
    const { slug } = await params;

    const projects = loadJSONData<any[]>('research-projects.json');
    const project = projects.find((p: any) => p.slug === slug);
    const paragraphs = loadJSONData<Record<string, string>>('research-paragraphs.json');
    const figuresData = loadJSONData<any[]>('research-figures-with-captions.json');

    const pageData = figuresData.find((p: any) => p.slug === slug);
    const introductoryParagraph = paragraphs[slug];
    const figure = pageData?.figure;

    return (
        <main className="flex-1 container mx-auto py-16 md:py-24">
            <h1 className="font-headline">{project?.title}</h1>
            <p
                className="text-lg text-muted-foreground mt-4 [&_a]:text-primary [&_a:hover]:underline"
                dangerouslySetInnerHTML={{ __html: renderMathInText(introductoryParagraph) }}
            />
            <p className="text-sm text-muted-foreground mt-4">
                Summary generated with ChatGPT based on my first-author publications for clarity and accessibility.
            </p>
            {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
        </main>
    );
}