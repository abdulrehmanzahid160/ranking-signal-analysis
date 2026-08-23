import Link from "next/link";
import { paperSections, sectionHref } from "../paper-meta";

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header-inner">
        <div className="publication-bar">
          <Link className="site-title" href="/" aria-label="SignalRank home">
            <span className="site-mark" aria-hidden="true">SR</span>
            <span>
              <strong>SignalRank</strong>
              <small>Ranking Signal Analysis</small>
            </span>
          </Link>
          <div className="publication-links">
            <Link href="/reproducibility">Reproduce</Link>
            <a
              href="https://github.com/abdulrehmanzahid160/ranking-signal-analysis"
              target="_blank"
              rel="noreferrer"
            >
              GitHub <span aria-hidden="true">↗</span>
            </a>
          </div>
        </div>
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
