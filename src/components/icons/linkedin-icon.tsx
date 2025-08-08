import Image from 'next/image';

export function LinkedinIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/linkedin.svg" alt="LinkedIn Icon" width={24} height={24} {...props} />
  );
}
