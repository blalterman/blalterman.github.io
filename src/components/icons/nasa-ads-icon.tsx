import Image from 'next/image';

export function NasaAdsIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/ads.svg" alt="NASA ADS Icon" width={24} height={24} {...props} />
  );
}
