import type { Metadata } from 'next';

interface BuildPageMetadataArgs {
  path: string;
  title: string;
  description: string;
}

const SITE_NAME = "B. L. Alterman | Research Astrophysicist";

const SITE_IMAGE = {
  url: "https://blalterman.github.io/images/headshot.jpg",
  width: 256,
  height: 256,
  alt: "B. L. Alterman Headshot",
};

export function buildPageMetadata({
  path,
  title,
  description,
}: BuildPageMetadataArgs): Metadata {
  return {
    title,
    description,
    alternates: {
      canonical: path,
    },
    openGraph: {
      title,
      description,
      url: path,
      siteName: SITE_NAME,
      images: [SITE_IMAGE],
      locale: "en_US",
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [SITE_IMAGE.url],
    },
  };
}
