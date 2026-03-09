import Image from 'next/image';
import { cn } from '@/lib/utils';

export function LinkedinIcon({ className, ...props }: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/linkedin.svg" alt="LinkedIn Icon" width={24} height={24} className={cn("dark:invert", className)} {...props} />
  );
}
