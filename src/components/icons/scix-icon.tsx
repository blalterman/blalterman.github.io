import Image from 'next/image';
import { cn } from '@/lib/utils';

export function SciXIcon({ className, ...props }: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/scix-icon-light.svg" alt="SciX Icon" width={24} height={24} className={cn("dark:invert", className)} {...props} />
  );
}
