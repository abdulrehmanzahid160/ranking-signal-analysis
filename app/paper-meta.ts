export const paperSections = [
  { number: "01", label: "Title + Abstract", slug: "", title: "Signals before movement" },
  { number: "02", label: "Introduction", slug: "introduction", title: "Choosing what to review" },
  { number: "03", label: "Data", slug: "data", title: "Data and study sample" },
  { number: "04", label: "Methodology", slug: "methodology", title: "Separated windows and held-out clients" },
  { number: "05", label: "Results", slug: "results", title: "Ordering improved; absolute fit remained weak" },
  { number: "06", label: "Limitations", slug: "limitations", title: "What the estimates leave unresolved" },
  { number: "07", label: "Recommendations", slug: "recommendations", title: "A reason-coded review order" },
  { number: "08", label: "Reproducibility", slug: "reproducibility", title: "From warehouse schema to paper figures" },
  { number: "09", label: "Acknowledgments", slug: "acknowledgments", title: "Acknowledgments and data credit" },
] as const;

export type PaperSectionMeta = (typeof paperSections)[number];

export function sectionHref(slug: string) {
  return slug ? `/${slug}` : "/";
}
