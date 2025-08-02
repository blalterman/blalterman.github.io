import type { Metadata } from 'next';
import './globals.css';
import { Toaster } from '@/components/ui/toaster';

export const metadata: Metadata = {
  metadataBase: new URL("https://blalterman.github.io"),
  title: "B. L. Alterman | Research Astrophysicist",
  description: "Research astrophysicist studying solar wind physics, heliophysics, and space weather. Explore publications, projects, and academic collaborations.",
  keywords: [
    "heliophysics", "solar wind", "Coulomb collisions", "Helium Abundance",
    "space weather", "solar physics", "composition", "proton beams",
    "kinetic physics", "astrophysics", "B. L. Alterman", "Ben Alterman"
  ],
  authors: [{ name: "B. L. Alterman", url: "https://blalterman.github.io" }],
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "B. L. Alterman | Research Astrophysicist",
    description: "Explore B. L. Alterman's research in heliophysics, solar wind physics, and space weather.",
    url: "https://blalterman.github.io",
    siteName: "B. L. Alterman | Research Astrophysicist",
    images: [
      {
        url: "https://blalterman.github.io/images/headshot.jpg",
        width: 256,
        height: 256,
        alt: "B. L. Alterman Headshot",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "B. L. Alterman | Research Astrophysicist",
    description: "Solar wind physicist exploring the heliosphere and its impact on Earth’s space environment.",
    images: ["https://blalterman.github.io/images/headshot.jpg"],
  },
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "B. L. Alterman",
    "url": "https://blalterman.github.io",
    "sameAs": [
      "https://orcid.org/0000-0001-6673-3432",
      "https://scholar.google.com/citations?user=yF0j6J8AAAAJ",
      "https://ui.adsabs.harvard.edu/search/p_=0&q=orcid%3A0000-0001-6673-3432&sort=date%20desc%2C%20bibcode%20desc",
      "https://github.com/blalterman",
      "https://arxiv.org/a/alterman_b_1.html"
    ],
    "jobTitle": "Research Astrophysicist",
    "affiliation": {
      "@type": "Organization",
      "name": "NASA Goddard Space Flight Center",
      "url": "https://www.nasa.gov/goddard"
    },
    "alumniOf": [
      {
        "@type": "EducationalOrganization",
        "name": "University of Michigan",
        "url": "https://www.umich.edu"
      },
      {
        "@type": "EducationalOrganization",
        "name": "Macalester College",
        "url": "https://www.macalester.edu"
      }
    ],
    "description": "Research astrophysicist specializing in heliophysics, solar wind physics, and space weather.",
  };

  return (
    <html lang="en" className="!scroll-smooth">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet" />
      </head>
      <body className="font-body antialiased">
        {children}
        <Toaster />
      </body>
    </html>
  );
}