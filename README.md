# Ranking Signal Analysis

An observational FlyRank ML Internship capstone about content and search measures associated with subsequent organic position movement. The repository contains a reproducible analysis and a multi-page research paper built with Next.js 16, TypeScript, and Tailwind CSS v4.

## Paper site

The `/` route contains the title, abstract, and linked table of contents. The remaining eight paper sections have dedicated routes with previous/next navigation. Every route is a Server Component with no data fetching, API routes, browser state, trackers, or runtime chart libraries. Next.js prerenders the complete publication during the default Vercel build. Figures under `public/figures/` are analysis exports rendered through `next/image`.

```powershell
npm install
npm run dev
npm run build
npm run lint
```

## Analysis reproduction

Create a Python environment, install `requirements.txt`, and provide a gated Hugging Face read token through `HF_TOKEN`. Never store the token in a project file.

```powershell
python work/notebooks/00_schema_discovery.py
python work/notebooks/01_signal_features_audited.py --cutoff 2026-04-30
python work/notebooks/01_signal_features_audited.py --cutoff 2026-05-31
python work/notebooks/02_modeling.py
python work/notebooks/03_query_associations.py
python work/notebooks/04_analysis_outputs.py
```

Content-level Parquet files stay in ignored `outputs/data/`. The public site contains only aggregate records and non-identifying figure exports.

## Deploy on Vercel

1. Push the repository to GitHub.
2. In Vercel, choose **Add New → Project** and import the repository.
3. Keep the detected Next.js build settings and leave environment variables empty.
4. Deploy the production branch.
5. Replace `[[PLACEHOLDER]]` in `submission/paper_url.txt` with the production URL. The file must contain that URL and one newline only.

The analysis reports observed, directional associations for review prioritization. It does not establish causality or disclose private warehouse records.
