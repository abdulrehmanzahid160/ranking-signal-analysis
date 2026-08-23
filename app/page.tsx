import { PageNavigation } from "./components/PageNavigation";
import { PaperSection } from "./components/PaperSection";
import { SectionDirectory } from "./components/SectionDirectory";
import { SiteHeader } from "./components/SiteHeader";
import Link from "next/link";

export default function PaperHome() {
  return (
    <>
      <SiteHeader />
      <main>
        <PaperSection number="01" label="Title + Abstract" id="abstract">
          <p className="kicker">SignalRank research paper · August 2026</p>
          <h1 id="abstract-heading">Signals before movement</h1>
          <p className="subtitle">A grouped study of content-level indicators and subsequent organic position change</p>
          <p className="byline">Abdul Rehman · Machine Learning Internship Capstone</p>
          <div className="hero-actions" aria-label="Paper shortcuts">
            <Link className="primary-action" href="/introduction">Read the paper <span aria-hidden="true">→</span></Link>
            <Link href="/results">View results</Link>
            <a href="https://github.com/abdulrehmanzahid160/ranking-signal-analysis" target="_blank" rel="noreferrer">
              Source on GitHub <span aria-hidden="true">↗</span>
            </a>
          </div>

          <aside className="evidence-summary" aria-labelledby="evidence-summary-title">
            <div className="evidence-summary-heading">
              <p id="evidence-summary-title">Headline evidence</p>
              <span>Held-out evaluation</span>
            </div>
            <dl>
              <div>
                <dt>0.165</dt>
                <dd>Ridge Spearman ρ</dd>
              </div>
              <div>
                <dt>0.117</dt>
                <dd>Random forest ρ</dd>
              </div>
              <div>
                <dt>−0.096</dt>
                <dd>Baseline ρ</dd>
              </div>
              <div>
                <dt>9</dt>
                <dd>Unseen clients</dd>
              </div>
            </dl>
            <p className="evidence-caveat">
              Directional associations for review prioritization—not causal estimates. Absolute model fit remained weak.
            </p>
          </aside>

          <div className="abstract-copy">
            <p className="abstract-label">Abstract</p>
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
