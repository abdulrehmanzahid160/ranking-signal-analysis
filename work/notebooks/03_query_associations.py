"""Public-safe descriptive query-signal summaries (not primary model inputs)."""

from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
df = pd.read_parquet(ROOT / "outputs/data/features_2026_05_31.parquet")
signals = ["query_impression_entropy_90d", "visible_query_click_momentum", "visible_query_impression_momentum"]
rows = []
for signal in signals:
    pair = df[[signal, "label_position_change"]].dropna()
    rows.append({"signal": signal, "n": len(pair),
                 "spearman_with_position_change": spearmanr(pair[signal], pair.label_position_change).statistic,
                 "interpretation": "descriptive_shared_window_not_model_input"})
out = pd.DataFrame(rows)
(ROOT / "docs/results").mkdir(parents=True, exist_ok=True)
out.to_csv(ROOT / "docs/results/query_descriptive_associations.csv", index=False)
print(out.to_string(index=False))
