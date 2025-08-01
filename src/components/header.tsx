import Link from 'next/link';
import { Github, Mountain } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { MobileNav } from '@/components/mobile-nav';
import { ArxivIcon } from '@/components/icons/arxiv-icon';
import { GoogleScholarIcon } from '@/components/icons/google-scholar-icon';
import { NasaAdsIcon } from '@/components/icons/nasa-ads-icon';
import { OrcidIcon } from '@/components/icons/orcid-icon';

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 max-w-screen-2xl items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <Mountain className="h-6 w-6 text-primary" />
            <span className="font-bold sm:inline-block">B. L. Alterman</span>
          </Link>
          <nav className="hidden items-center space-x-6 text-sm font-medium md:flex">
            <Link href="/research" className="transition-colors hover:text-foreground/80 text-foreground/60">Research</Link>
            <Link href="/skills" className="transition-colors hover:text-foreground/80 text-foreground/60">Skills</Link>
            <Link href="/experience" className="transition-colors hover:text-foreground/80 text-foreground/60">Experience</Link>
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
                <Link href="https://orcid.org/0000-0001-6673-3432" target="_blank" rel="noopener noreferrer" aria-label="ORCID">
                    <OrcidIcon className="h-5 w-5" />
                </Link>
            </Button>
            <Button variant="ghost" size="icon" asChild>
                <Link href="https://ui.adsabs.harvard.edu/search/p_=0&q=orcid%3A0000-0001-6673-3432&sort=date%20desc%2C%20bibcode%20desc" target="_blank" rel="noopener noreferrer" aria-label="NASA ADS">
                    <NasaAdsIcon className="h-5 w-5" />
                </Link>
            </Button>
            <Button variant="ghost" size="icon" asChild>
                <Link href="https://scholar.google.com/citations?user=yF0j6J8AAAAJ" target="_blank" rel="noopener noreferrer" aria-label="Google Scholar">
                    <GoogleScholarIcon className="h-5 w-5" />
                </Link>
            </Button>
            <Button variant="ghost" size="icon" asChild>
                <Link href="https://arxiv.org/a/alterman_b_1.html" target="_blank" rel="noopener noreferrer" aria-label="arXiv">
                    <ArxivIcon className="h-5 w-5" />
                </Link>
            </Button>
          </div>
          <MobileNav />
        </div>
      </div>
    </header>
  );
}
