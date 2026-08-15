import { PaperFigure } from "./components/PaperFigure";
import { PaperSection } from "./components/PaperSection";
import { SourceNote } from "./components/SourceNote";

const notebook = "/work/notebooks/capstone_ranking_signal_analysis.ipynb";

export default function Paper() {
  return (
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
      </PaperSection>

      <PaperSection number="02" label="Introduction" id="introduction">
        <h2 id="introduction-heading">Choosing what to review</h2>
        <p className="opening">
          Large content portfolios create a queueing problem. Analysts can inspect only a fraction of pages in each cycle, yet a queue based only on raw traffic tends to favor already-visible content. The decision studied here is narrower: which pages merit closer inspection before their measured position changes?
        </p>
        <p>
          The analysis converts aggregate measures into reason-coded review cohorts. A reason code records why a page entered a queue. It does not prescribe a rewrite, refresh, or removal. The intended use is a documented review process in which an analyst checks search intent, measurement continuity, and business relevance before any intervention.
        </p>
      </PaperSection>

      <PaperSection number="03" label="Data" id="data">
        <h2 id="data-heading">Data and study sample</h2>
        <p>
          The source is the gated FlyRank internship warehouse release available in August 2026. Daily performance covers January 2025 through June 2026. The primary analysis uses a feature cutoff of 31 May 2026 and an outcome window of 1–28 June 2026. A second cutoff on 30 April supplies the May temporal check.
        </p>
        <table>
          <thead>
            <tr><th>Table</th><th>Use in the study</th><th>Public treatment</th></tr>
          </thead>
          <tbody>
            <tr><td>dim_clients</td><td>Access dates and tenure control</td><td>Identifiers used only for grouping</td></tr>
            <tr><td>dim_content</td><td>Type, intent, length, and competition controls</td><td>No URLs or hashes published</td></tr>
            <tr><td>fact_content_daily_performance</td><td>Position, impressions, clicks, and CTR</td><td>Aggregated to one row per content item</td></tr>
            <tr><td>fact_content_query_90d</td><td>Query entropy and momentum descriptors</td><td>No query text; overlapping measures excluded from models</td></tr>
          </tbody>
        </table>
        <p>
          The unit of analysis is a content item within a client. Inclusion required at least 14 observed history days, seven recent days, seven outcome days, and ten outcome impressions. The resulting primary sample contains 130,833 items from 48 clients. Client history is unbalanced, so tenure enters as a control rather than a published identity. <SourceNote href="/results/summary.json">Aggregate sample record</SourceNote>
        </p>
      </PaperSection>

      <PaperSection number="04" label="Methodology" id="methodology">
        <h2 id="methodology-heading">Separated windows and held-out clients</h2>
        <h3>Signals</h3>
        <p>
          Pre-outcome measures include trailing average position, 90-day position volatility, a linear position slope, impressions, clicks, CTR, and CTR relative to the median for five position buckets. Content length, content type, stated intent, competition measures, and client tenure enter as controls.
        </p>
        <PaperFigure number={1} src="/figures/expected-ctr-curve.png" alt="Median click-through rate by average organic position bucket">
          Median content-level CTR by trailing average-position bucket. Zero medians in the lower buckets reflect sparse clicks in the sample. <SourceNote href="/results/expected_ctr_curve.csv">Figure data</SourceNote>
        </PaperFigure>
        <h3>Outcome and baseline</h3>
        <p>
          The outcome is following-28-day average position minus trailing-28-day average position. Positive values indicate numerical position deterioration. The baseline is a linear model using trailing position, position volatility, and position trend. Ridge adds the full control set; a random forest supplies a nonlinear comparison.
        </p>
        <h3>Validation and leakage checks</h3>
        <p>
          A deterministic client-group split assigns 39 clients to training and nine to evaluation. A row-random split would place content from the same client on both sides, allowing client-specific measurement patterns to cross the boundary. All modeled performance features end before the outcome begins. The fixed query snapshot ends on 30 June and overlaps the primary outcome, so query entropy and momentum are retained only for descriptive analysis. The same split rule is applied at the earlier cutoff. Random seeds are fixed at 42 for sampling and model fitting. <SourceNote href="/results/metrics.json">Model and leakage record</SourceNote>
        </p>
      </PaperSection>

      <PaperSection number="05" label="Results" id="results">
        <h2 id="results-heading">Ordering improved; absolute fit remained weak</h2>
        <p>
          On the same nine held-out clients, Ridge produced the strongest rank ordering: Spearman ρ was 0.165, compared with −0.096 for the baseline and 0.117 for the random forest (Figure 2). Ridge RMSE was 9.883 position units and R² was −0.005, so it did not beat a constant-mean prediction in squared-error terms (<SourceNote href="/results/metrics.json">capstone notebook, cell 7 output</SourceNote>).
        </p>
        <PaperFigure number={2} src="/figures/model-comparison.png" alt="Held-out Spearman correlations for baseline, Ridge, and random forest models">
          Held-out-client rank correlation. Each model is evaluated on the same client partition. <SourceNote href="/results/metrics.json">Figure data</SourceNote>
        </PaperFigure>
        <p>
          The earlier May refit yielded Ridge R² of 0.068 and Spearman ρ of 0.217. The rank correlation between absolute Ridge coefficient lists across the two cutoffs was 0.624, indicating moderate month-to-month agreement (<SourceNote href="/results/metrics.json">capstone notebook, cell 7 output</SourceNote>).
        </p>
        <PaperFigure number={3} src="/figures/ridge-coefficients.png" alt="Largest standardized coefficients from the Ridge model">
          Largest standardized Ridge associations. Positive coefficients align with numerical position deterioration. Correlated measures can exchange coefficient magnitude. <SourceNote href="/results/ridge_coefficients.csv">Figure data</SourceNote>
        </PaperFigure>
        <p>
          Current position had the largest positive random-forest permutation contribution at 0.063, followed by position volatility at 0.020 (<SourceNote href="/results/metrics.json">capstone notebook, cell 7 output</SourceNote>). The fitted response shapes are steepest for current position, while the remaining curves are smaller or less regular (Figure 4). These are model summaries rather than treatment effects.
        </p>
        <PaperFigure number={4} src="/figures/partial-dependence.png" alt="Partial dependence plots for five numeric ranking signals">
          Random-forest partial dependence for five leading numeric signals, averaged over the evaluation sample. The curves describe fitted model behavior and are not causal response functions. <SourceNote href="/results/metrics.json">Model record</SourceNote>
        </PaperFigure>
        <p>
          In the descriptive query analysis, entropy correlated 0.145 with numerical position deterioration, while click and impression momentum correlations were −0.072 and −0.087 (<SourceNote href="/results/query_descriptive_associations.csv">capstone notebook, cell 9 output</SourceNote>). Because the query window overlaps the outcome, these values are hypothesis-generating and were excluded from all fitted comparisons.
        </p>
      </PaperSection>

      <PaperSection number="06" label="Limitations" id="limitations">
        <h2 id="limitations-heading">What the estimates leave unresolved</h2>
        <p className="opening">
          This is an observational study. It cannot establish causation, prove why a page ranks, or reverse-engineer or reveal Google&apos;s algorithm.
        </p>
        <dl className="limitations-list">
          <div><dt>Selection and sampling</dt><dd>Eligibility thresholds favor content with recurring impressions and enough observed days. Sparse and newly published content is less represented, which may make the results look more stable than a full portfolio.</dd></div>
          <div><dt>Unmeasured confounding</dt><dd>Demand, competitor changes, SERP composition, seasonality, and measurement changes can affect both the recorded signals and subsequent position. The bias direction may differ across clients and months.</dd></div>
          <div><dt>Proxy outcome</dt><dd>Average position combines query, device, geography, and impression mixes. A numerical change need not correspond to the same change in qualified traffic or business value.</dd></div>
          <div><dt>Temporal drift</dt><dd>May and June scores differ materially. The coefficient-order correlation of 0.624 suggests partial continuity, while the June R² near zero shows that continuity did not produce dependable absolute estimates.</dd></div>
          <div><dt>Sparse clicks</dt><dd>Many content windows record no clicks. This compresses the CTR reference curve at lower positions and limits separation among low-exposure items.</dd></div>
        </dl>
      </PaperSection>

      <PaperSection number="07" label="Ranked recommendations" id="recommendations">
        <h2 id="recommendations-heading">A reason-coded review order</h2>
        <ol className="recommendation-list">
          <li><h3>Inspect high-volatility items first.</h3><p>Position volatility was the second-largest positive permutation contribution in the fitted forest. Use it to order diagnosis of query mix, tracking continuity, and intent fit before editing (Figures 2 and 4).</p><span>POS-VOL-HIGH</span></li>
          <li><h3>Read CTR relative to position.</h3><p>The position-bucket curve shows sharp click sparsity outside the leading buckets, while CTR gap also appears among the largest Ridge coefficients. Review snippet and intent alignment as a testable hypothesis; raw CTR alone is a poor quality verdict (Figures 1 and 3).</p><span>CTR-GAP-LOW</span></li>
          <li><h3>Require a sustained movement pattern.</h3><p>Trend and volatility add temporal context to current position, but held-out absolute fit was weak. Escalate only when a pattern persists with adequate impressions, and keep the reason code attached to the review (Figures 2 and 4).</p><span>POS-TREND-DOWN</span></li>
          <li><h3>Keep query breadth descriptive.</h3><p>The query correlations use a window that overlaps the outcome. Use breadth to frame an analyst question about dependence on a narrow query set; do not include it in a forward score (<SourceNote href="/results/query_descriptive_associations.csv">capstone notebook, cell 9 output</SourceNote>).</p><span>QUERY-BREADTH-DESCRIPTIVE</span></li>
          <li><h3>Measure interventions prospectively.</h3><p>June R² was near zero even when rank ordering improved. Record eligibility, reason code, intervention date, and a predeclared follow-up period; compare reviewed items with an eligible holdout before attributing impact (Figure 2).</p><span>TEST-BEFORE-CLAIM</span></li>
        </ol>
      </PaperSection>

      <PaperSection number="08" label="Reproducibility" id="reproducibility">
        <h2 id="reproducibility-heading">From warehouse schema to paper figures</h2>
        <p>
          The capstone notebook calls five numbered Python modules for schema discovery, feature construction, grouped modeling, descriptive query analysis, and reporting. DuckDB streams gated Parquet files; content-level outputs remain under ignored <code>outputs/data/</code>. Public aggregate records and the four figure exports are versioned with the site.
        </p>
        <pre><code>{`python -m venv .venv
pip install -r requirements.txt
set HF_TOKEN=<read-token>
python work/notebooks/01_signal_features_audited.py --cutoff 2026-04-30
python work/notebooks/01_signal_features_audited.py --cutoff 2026-05-31
python work/notebooks/02_modeling.py
python work/notebooks/03_query_associations.py
python work/notebooks/04_analysis_outputs.py`}</code></pre>
        <p>
          The grouped split and model sampling use seed 42. <a href={notebook}>Download the capstone notebook</a>. <a href="https://github.com/abdulrehmanzahid160/ranking-signal-analysis">View the repository</a>.
        </p>
      </PaperSection>

      <PaperSection number="09" label="Acknowledgments" id="acknowledgments">
        <h2 id="acknowledgments-heading">Acknowledgments and data credit</h2>
        <p>
          <a href="https://flyrank.ai" target="_blank" rel="noopener noreferrer">Built on the FlyRank ML Internship dataset</a>.
        </p>
        <p>
          The public paper contains no client names, domains, URLs, private query text, credentials, or raw warehouse exports.
        </p>
      </PaperSection>
    </main>
  );
}
