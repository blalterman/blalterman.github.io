import Image from 'next/image';

export function ClaudeIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/claude-clay.svg" alt="Claude Icon" width={24} height={24} {...props} />
  );
}
