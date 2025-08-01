"use client";

import { useState } from 'react';
import Link from 'next/link';
import { Menu, Mountain, Github } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Separator } from '@/components/ui/separator';

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
              <Link href="/skills" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Skills
              </Link>
              <Link href="/experience" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Experience
              </Link>
              <Link href="/research" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Research
              </Link>
              <Link href="/publications" className="flex w-full items-center py-2 text-lg font-semibold px-4 rounded-md hover:bg-muted" onClick={closeSheet}>
                Publications
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
          </div>
        </nav>
      </SheetContent>
    </Sheet>
  );
}
