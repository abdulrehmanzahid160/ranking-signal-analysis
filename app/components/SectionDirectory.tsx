import Link from "next/link";
import { paperSections, sectionHref } from "../paper-meta";

export function SectionDirectory() {
  return (
    <nav className="section-directory" aria-label="Complete paper contents">
      <p>Read by section</p>
      <ol>
        {paperSections.slice(1).map((section) => (
          <li key={section.number}>
            <Link href={sectionHref(section.slug)}>
              <span>{section.number}</span>
              <strong>{section.label}</strong>
              <small>{section.title}</small>
            </Link>
          </li>
        ))}
      </ol>
    </nav>
  );
}
