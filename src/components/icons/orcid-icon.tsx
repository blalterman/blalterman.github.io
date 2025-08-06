import Image from 'next/image';

export function OrcidIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/orcid.svg" alt="ORCID Icon" width={24} height={24} {...props} />
  );
}
