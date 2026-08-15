import Link from "next/link";
import { paperSections, sectionHref } from "../paper-meta";

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link className="site-title" href="/">Ranking Signal Analysis</Link>
        <nav aria-label="Paper sections">
          {paperSections.map((section) => (
            <Link key={section.number} href={sectionHref(section.slug)}>
              <span>{section.number}</span> {section.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
