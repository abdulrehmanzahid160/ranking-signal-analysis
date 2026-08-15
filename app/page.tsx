import { PageNavigation } from "./components/PageNavigation";
import { PaperSection } from "./components/PaperSection";
import { SectionDirectory } from "./components/SectionDirectory";
import { SiteHeader } from "./components/SiteHeader";

export default function PaperHome() {
  return (
    <>
      <SiteHeader />
      <main>
        <PaperSection number="01" label="Title + Abstract" id="abstract">
          <p className="kicker">FlyRank ML Internship · Capstone paper · August 2026</p>
          <h1 id="abstract-heading">Signals before movement</h1>
          <p className="subtitle">A grouped study of content-level indicators and subsequent organic position change</p>
          <p className="byline">Abdul Rehman · Machine Learning Internship Capstone</p>
          <div className="abstract-copy">
            <p>
              This study asks which public-safe content and search measures are associated with subsequent organic position movement. It constructs 90-day position, volatility, trend, click-through-rate, content, and client-tenure features, then evaluates position change during a separate 28-day outcome window. On nine unseen clients, Ridge reached a Spearman correlation of 0.165, compared with −0.096 for the baseline and 0.117 for the random forest (Figure 2). The observed ordering supports analyst triage based on position level and volatility while leaving final content decisions to human review (Figures 3 and 4). As an observational study with weak absolute fit, the work cannot establish causation or account for every source of temporal change.
            </p>
          </div>
          <SectionDirectory />
        </PaperSection>
        <PageNavigation slug="" />
      </main>
    </>
  );
}
