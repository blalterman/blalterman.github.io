import Image from 'next/image';
import { cn } from '@/lib/utils';
import { renderMathInText } from '@/lib/render-math';

interface ResearchFigureProps {
  src: string;
  alt: string;
  caption: string;
  className?: string;
}

export function ResearchFigure({ src, alt, caption, className }: ResearchFigureProps) {
  // Process caption to render LaTeX math expressions at build time
  const processedCaption = renderMathInText(caption);

  return (
    <figure className={cn('my-8 flex flex-col items-center', className)}>
      <div className="relative w-full max-w-4xl aspect-[4/3] border rounded-lg overflow-hidden shadow-lg">
        <Image
          src={src}
          alt={alt}
          fill
          className="object-contain"
        />
      </div>
      <figcaption
        className="mt-4 text-sm text-center text-muted-foreground max-w-3xl"
        dangerouslySetInnerHTML={{ __html: processedCaption }}
      />
    </figure>
  );
}
