import Image from 'next/image';

export function GithubMarkIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/github-mark.svg" alt="GitHub Icon" width={24} height={24} {...props} />
  );
}
