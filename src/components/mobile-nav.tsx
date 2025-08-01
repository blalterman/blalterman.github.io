"use client";

import { useState } from 'react';
import Link from 'next/link';
import { Menu, Mountain, Github } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Separator } from '@/components/ui/separator';
import { OrcidIcon } from './icons/orcid-icon';
import { NasaAdsIcon } from './icons/nasa-ads-icon';
import { GoogleScholarIcon } from './icons/google-scholar-icon';
import { ArxivIcon } from './icons/arxiv-icon';

export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false);

  const closeSheet = () => setIsOpen(false);

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-6 w-6" />
          <span className="sr-only">Toggle navigation menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-full max-w-xs pr-0">
        <nav className="flex flex-col h-full">
          <div className="border-b p-4">
            <Link href="/" className="flex items-center gap-2 font-bold" onClick={closeSheet}>
              <Mountain className="h-6 w-6 text-primary" />
              <span className="text-lg">B. L. Alterman</span>
            </Link>
          </div>
          <div className="flex-1 overflow-y-auto">
            <div className="grid gap-2 py-6">
              <Link href="/research" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Research
              </Link>
              <Link href="/publications" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Publications
              </Link>
              <Link href="/skills" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Skills
              </Link>
              <Link href="/experience" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Experience
              </Link>
              <Link href="/#contact" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Contact
              </Link>
            </div>
          </div>
          <Separator />
          <div className="p-4 flex justify-center items-center space-x-2">
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
        </nav>
      </SheetContent>
    </Sheet>
  );
}
