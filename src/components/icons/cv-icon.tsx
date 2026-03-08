import type { SVGProps } from 'react';

export function CvIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="currentColor"
      stroke="none"
      {...props}
    >
      {/* C — filled letterform */}
      <path d="M 9.5 2 C 5.4 2, 1 5.5, 1 12 C 1 18.5, 5.4 22, 9.5 22 L 9.5 19.2 C 6.8 19.2, 3.8 16.8, 3.8 12 C 3.8 7.2, 6.8 4.8, 9.5 4.8 Z" />
      {/* V — filled letterform */}
      <path d="M 11.5 2 L 16.5 18 L 21.5 2 L 23 2 L 17.2 22 L 15.8 22 L 10 2 Z" />
    </svg>
  );
}
