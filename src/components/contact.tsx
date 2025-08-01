"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Mail, Github, Linkedin, Twitter } from 'lucide-react';
import Link from 'next/link';

export function Contact() {
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());

  useEffect(() => {
    setCurrentYear(new Date().getFullYear());
  }, []);

  return (
    <footer id="contact" className="bg-muted/50 py-12 md:py-16">
      <div className="container text-center">
        <h2 className="text-2xl md:text-3xl font-bold font-headline">Get in Touch</h2>
        <p className="text-muted-foreground mt-2 mb-6 max-w-xl mx-auto">
          I'm always open to discussing new research, projects, or collaboration opportunities. Feel free to reach out.
        </p>
        <div className="mb-8">
          <Button size="lg" asChild>
            <a href="mailto:ben.alterman@example.com">
              <Mail className="mr-2 h-5 w-5" />
              Email Me
            </a>
          </Button>
        </div>
        <div className="flex justify-center items-center space-x-4 mb-4">
          <Link href="https://github.com/blalterman" target="_blank" rel="noopener noreferrer" aria-label="GitHub" className="text-muted-foreground hover:text-foreground transition-colors">
            <Github className="h-6 w-6" />
          </Link>
          <Link href="#" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" className="text-muted-foreground hover:text-foreground transition-colors">
            <Linkedin className="h-6 w-6" />
          </Link>
          <Link href="#" target="_blank" rel="noopener noreferrer" aria-label="Twitter" className="text-muted-foreground hover:text-foreground transition-colors">
            <Twitter className="h-6 w-6" />
          </Link>
        </div>
        <p className="text-sm text-muted-foreground">
          &copy; {currentYear} Ben Alterman. All Rights Reserved.
        </p>
      </div>
    </footer>
  );
}
