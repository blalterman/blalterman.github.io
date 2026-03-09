import Image from 'next/image';
import { cn } from '@/lib/utils';

export function GithubMarkIcon({ className, ...props }: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/github-mark.svg" alt="GitHub Icon" width={24} height={24} className={cn("dark:invert", className)} {...props} />
  );
}
