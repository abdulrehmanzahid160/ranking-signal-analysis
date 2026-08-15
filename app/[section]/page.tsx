import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { PageNavigation } from "../components/PageNavigation";
import { PaperSection } from "../components/PaperSection";
import { SiteHeader } from "../components/SiteHeader";
import { paperContent } from "../paper-content";
import { paperSections } from "../paper-meta";

type SectionPageProps = { params: Promise<{ section: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return paperSections.slice(1).map(({ slug }) => ({ section: slug }));
}

export async function generateMetadata({ params }: SectionPageProps): Promise<Metadata> {
  const { section: slug } = await params;
  const section = paperSections.find((item) => item.slug === slug);
  return section
    ? { title: `${section.label} | Ranking Signal Analysis`, description: section.title }
    : {};
}

export default async function SectionPage({ params }: SectionPageProps) {
  const { section: slug } = await params;
  const section = paperSections.find((item) => item.slug === slug);
  if (!section || !paperContent[slug]) notFound();

  return (
    <>
      <SiteHeader />
      <main>
        <PaperSection number={section.number} label={section.label} id={section.slug}>
          {paperContent[slug]}
        </PaperSection>
        <PageNavigation slug={slug} />
      </main>
    </>
  );
}
