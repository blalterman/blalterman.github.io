import Image from 'next/image';

export function SciXIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/scix-icon-light.svg" alt="SciX Icon" width={24} height={24} {...props} />
  );
}
