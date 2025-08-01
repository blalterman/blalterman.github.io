import Link from 'next/link';
import { Github, Linkedin, Twitter, Mountain } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { MobileNav } from '@/components/mobile-nav';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 max-w-screen-2xl items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <Mountain className="h-6 w-6 text-primary" />
            <span className="font-bold sm:inline-block">Ben Alterman</span>
          </Link>
          <nav className="hidden items-center space-x-6 text-sm font-medium md:flex">
            <Link href="/#about" className="transition-colors hover:text-foreground/80 text-foreground/60">About</Link>
            <Link href="/#skills" className="transition-colors hover:text-foreground/80 text-foreground/60">Skills</Link>
            <Link href="/#research" className="transition-colors hover:text-foreground/80 text-foreground/60">Research</Link>
            <Link href="/publications" className="transition-colors hover:text-foreground/80 text-foreground/60">Publications</Link>
            <Link href="/#contact" className="transition-colors hover:text-foreground/80 text-foreground/60">Contact</Link>
          </nav>
        </div>
        <div className="flex flex-1 items-center justify-end">
          <div className="hidden md:flex items-center space-x-2">
            <Button variant="ghost" size="icon" asChild>
              <Link href="https://github.com/blalterman" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                <Github className="h-5 w-5" />
              </Link>
            </Button>
            <Button variant="ghost" size="icon" asChild>
              <Link href="#" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                <Linkedin className="h-5 w-5" />
              </Link>
            </Button>
            <Button variant="ghost" size="icon" asChild>
              <Link href="#" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                <Twitter className="h-5 w-5" />
              </Link>
            </Button>
          </div>
          <MobileNav />
        </div>
      </div>
    </header>
  );
}
