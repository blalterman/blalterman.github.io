import Image from 'next/image';
import { cn } from '@/lib/utils';

export function GoogleScholarIcon({ className, ...props }: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/google-scholar.svg" alt="Google Scholar Icon" width={24} height={24} className={cn("dark:invert", className)} {...props} />
  );
}
