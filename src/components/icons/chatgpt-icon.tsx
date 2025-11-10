import Image from 'next/image';

export function ChatGptIcon(props: Omit<React.ComponentProps<typeof Image>, 'src' | 'alt'>) {
  return (
    <Image src="/icons/OpenAI-black-monoblossom.svg" alt="ChatGPT Icon" width={24} height={24} {...props} />
  );
}
