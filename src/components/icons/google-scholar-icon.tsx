import Image from 'next/image';

export function GoogleScholarIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/google-scholar.svg" alt="Google Scholar Icon" width={24} height={24} {...props} />
  );
}
