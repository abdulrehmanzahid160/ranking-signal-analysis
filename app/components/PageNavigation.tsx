import Link from "next/link";
import { paperSections, sectionHref } from "../paper-meta";

export function PageNavigation({ slug }: { slug: string }) {
  const index = paperSections.findIndex((section) => section.slug === slug);
  const previous = index > 0 ? paperSections[index - 1] : null;
  const next = index < paperSections.length - 1 ? paperSections[index + 1] : null;

  return (
    <nav className="page-navigation" aria-label="Previous and next paper sections">
      <div>
        {previous && <Link href={sectionHref(previous.slug)}><span>Previous</span>{previous.label}</Link>}
      </div>
      <div>
        {next && <Link href={sectionHref(next.slug)}><span>Next</span>{next.label}</Link>}
      </div>
    </nav>
  );
}
