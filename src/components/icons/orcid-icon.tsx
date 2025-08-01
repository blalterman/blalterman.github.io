import { SVGProps } from "react";

export function OrcidIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
      <path fill="#A6CE39" d="M256 128c0 70.7-57.3 128-128 128S0 198.7 0 128 57.3 0 128 0s128 57.3 128 128z"/>
      <path fill="#FFF" d="M86.3 186.2H70.9V79.1h15.4v107.1zM78.6 73.8c-5.3 0-9.6-4.3-9.6-9.6s4.3-9.6 9.6-9.6 9.6 4.3 9.6 9.6-4.3 9.6-9.6 9.6zM170.4 186.2h-15.4V138.8c0-9.9-2-19.5-14.1-19.5-12.1 0-16.4 8.8-16.4 19.5v47.4H109V79.1h15.4v14.1h.2c4.2-7.7 14.8-16.4 30.6-16.4 32.8 0 38.6 21.6 38.6 49.6v60.8z"/>
    </svg>
  );
}
