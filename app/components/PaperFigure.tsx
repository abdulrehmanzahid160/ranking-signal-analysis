import Image from "next/image";

type PaperFigureProps = {
  number: number;
  src: string;
  alt: string;
  children: React.ReactNode;
  width?: number;
  height?: number;
};

export function PaperFigure({ number, src, alt, children, width = 1440, height = 900 }: PaperFigureProps) {
  return (
    <figure className="paper-figure" id={`figure-${number}`}>
      <Image src={src} alt={alt} width={width} height={height} sizes="(max-width: 760px) 100vw, 760px" />
      <figcaption>
        <span>Figure {number}.</span> {children}
      </figcaption>
    </figure>
  );
}
