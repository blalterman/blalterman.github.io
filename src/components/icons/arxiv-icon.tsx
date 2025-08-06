import Image from 'next/image';

export function ArxivIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/arxiv.svg" alt="arXiv Icon" width={24} height={24} {...props} />
  );
}
