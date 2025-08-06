import Image from 'next/image';

export function FirebaseIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/firebase.svg" alt="Firebase Icon" width={24} height={24} {...props} />
  );
}
