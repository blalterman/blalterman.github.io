import { ResearchFigure } from '@/components/research-figure';
import { loadJSONData } from '@/lib/data-loader';
import { filterPublishedProjects } from '@/lib/research-utils';
import { renderMathInText } from '@/lib/render-math';
import { Metadata, ResolvingMetadata } from 'next';
import { redirect } from 'next/navigation';

type Props = {
    params: Promise<{ slug: string }>;
};

export async function generateStaticParams() {
    const projects = loadJSONData<any[]>('research-projects.json');
    // Only generate static params for published projects (environment-aware)
    const publishedProjects = filterPublishedProjects(projects);
    return publishedProjects.map((project) => ({
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

    // Redirect to /research if page is unpublished in production
    // (In development, allow access to all pages)
    const isDev = process.env.NODE_ENV === 'development';
    if (!isDev && project?.published === false) {
        redirect('/research');
    }

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
            {figure && <ResearchFigure src={figure.src} alt={figure.alt} caption={figure.caption} />}
        </main>
    );
}