import type { Publication } from "@/types/publication";

function formatDatePublished(year: string): string {
  const parts = year.split('-');
  if (parts.length >= 2 && parts[1] !== '00') {
    return `${parts[0]}-${parts[1]}`;
  }
  return parts[0];
}

function formatAuthorName(author: string): string {
  const commaIdx = author.indexOf(',');
  if (commaIdx === -1) return author;
  const lastName = author.slice(0, commaIdx).trim();
  const firstInitials = author.slice(commaIdx + 1).trim();
  return `${firstInitials} ${lastName}`;
}

export function buildScholarlyArticleJsonLd(publication: Publication): string {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ScholarlyArticle",
    "headline": publication.title,
    "author": publication.authors.map((author) => ({
      "@type": "Person",
      "name": formatAuthorName(author),
    })),
    "datePublished": formatDatePublished(publication.year),
    "mainEntityOfPage": publication.url,
  };
  return JSON.stringify(jsonLd);
}
