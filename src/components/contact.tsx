"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Mail, Github } from 'lucide-react';
import Link from 'next/link';
import { OrcidIcon } from './icons/orcid-icon';
import { NasaAdsIcon } from './icons/nasa-ads-icon';
import { GoogleScholarIcon } from './icons/google-scholar-icon';
import { ArxivIcon } from './icons/arxiv-icon';
import { FirebaseIcon } from './icons/firebase-icon';
import { GithubMarkIcon } from './icons/github-mark-icon';
import { LinkedinIcon } from './icons/linkedin-icon';
import { ClaudeIcon } from './icons/claude-icon';
import { ChatGptIcon } from './icons/chatgpt-icon';

export function Contact() {
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());

  useEffect(() => {
    setCurrentYear(new Date().getFullYear());
  }, []);

  return (
    <footer id="contact" className="bg-muted/50 py-12 md:py-16">
      <div className="container mx-auto max-w-screen-xl text-center">
        <h2 className="text-2xl md:text-3xl font-bold font-headline">Get in Touch</h2>
        <p className="text-muted-foreground mt-2 mb-6 max-w-xl mx-auto">
          I'm always open to discussing new research, projects, or collaboration opportunities.
        </p>
        <div className="mb-8">
          <Button size="lg" asChild>
            <a href="mailto:blaltermanphd+web_inquiry@gmail.com">
              <Mail className="mr-2 h-5 w-5" />
              Email Me
            </a>
          </Button>
        </div>
        <div className="flex justify-center items-center space-x-4 mb-4">
          <Link href="https://github.com/blalterman" target="_blank" rel="noopener noreferrer" aria-label="GitHub" className="text-muted-foreground hover:text-foreground transition-colors">
            <Github className="h-6 w-6" />
          </Link>
          <Link href="https://orcid.org/0000-0001-6673-3432" target="_blank" rel="noopener noreferrer" aria-label="ORCID" className="text-muted-foreground hover:text-foreground transition-colors">
            <OrcidIcon className="h-6 w-6" />
          </Link>
          <Link href="https://ui.adsabs.harvard.edu/search/p_=0&q=orcid%3A0000-0001-6673-3432&sort=date%20desc%2C%20bibcode%20desc" target="_blank" rel="noopener noreferrer" aria-label="NASA ADS" className="text-muted-foreground hover:text-foreground transition-colors">
            <NasaAdsIcon className="h-6 w-6" />
          </Link>
          <Link href="https://scholar.google.com/citations?user=yF0j6J8AAAAJ" target="_blank" rel="noopener noreferrer" aria-label="Google Scholar" className="text-muted-foreground hover:text-foreground transition-colors">
            <GoogleScholarIcon className="h-6 w-6" />
          </Link>
          <Link href="https://arxiv.org/a/alterman_b_1.html" target="_blank" rel="noopener noreferrer" aria-label="arXiv" className="text-muted-foreground hover:text-foreground transition-colors">
            <ArxivIcon className="h-6 w-6" />
          </Link>
          <Link href="https://www.linkedin.com/in/blalterman" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" className="text-muted-foreground hover:text-foreground transition-colors">
            <LinkedinIcon className="h-6 w-6" />
          </Link>
        </div>
        <p className="text-sm text-muted-foreground">
          &copy; {currentYear} B. L. Alterman. All Rights Reserved.
        </p>
        <div className="flex flex-col md:flex-row justify-center items-center gap-2 md:gap-4 mt-4 text-sm text-muted-foreground">
            <span className="flex items-center">
                Built with
                <a href="https://firebase.google.com/" target="_blank" rel="noopener noreferrer" className="ml-2 flex items-center hover:text-foreground transition-colors">
                    <FirebaseIcon className="h-5 w-5 mr-1" />
                    Firebase.
                </a>
            </span>
            <span className="flex items-center">
                Maintained with
                <a href="https://claude.ai" target="_blank" rel="noopener noreferrer" className="ml-2 flex items-center hover:text-foreground transition-colors">
                    <ClaudeIcon className="h-5 w-5 mr-1" />
                    Claude
                </a>
                <span className="mx-1">and</span>
                <a href="https://chatgpt.com" target="_blank" rel="noopener noreferrer" className="flex items-center hover:text-foreground transition-colors">
                    <ChatGptIcon className="h-5 w-5 mr-1" />
                    ChatGPT.
                </a>
            </span>
            <span className="flex items-center">
                Hosted on
                <a href="https://github.com/blalterman/blalterman.github.io" target="_blank" rel="noopener noreferrer" className="ml-2 flex items-center hover:text-foreground transition-colors">
                    <GithubMarkIcon className="h-5 w-5 mr-1" />
                    GitHub.
                </a>
            </span>
        </div>
      </div>
    </footer>
  );
}
