import type { ReactNode } from "react";

type PaperSectionProps = {
  number: string;
  label: string;
  id: string;
  children: ReactNode;
};

export function PaperSection({ number, label, id, children }: PaperSectionProps) {
  return (
    <section className="paper-section" id={id} aria-labelledby={`${id}-heading`}>
      <header className="section-marker" aria-hidden="true">
        <span>{number}</span>
        <span>{label}</span>
      </header>
      <div className="section-copy">{children}</div>
    </section>
  );
}
