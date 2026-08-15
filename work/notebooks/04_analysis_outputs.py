"""Generate public-safe aggregate artifacts used by the paper."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "outputs/data/features_2026_05_31.parquet"
RESULTS = ROOT / "docs/results"
ASSETS = ROOT / "docs/assets"


def weighted_log_odds(frame: pd.DataFrame) -> pd.DataFrame:
    low, high = frame.label_position_change.quantile([0.2, 0.8])
    rows = []
    for column in ["content_type", "main_intent", "competition_level"]:
        values = frame[column].astype("string").fillna("missing")
        improved = values[frame.label_position_change <= low].value_counts()
        worsened = values[frame.label_position_change >= high].value_counts()
        total = values.value_counts()
        vocab = total.index
        prior = (total / total.sum() * 10).clip(lower=0.1)
        ni, nw = improved.sum(), worsened.sum()
        for value in vocab:
            ai, aw = improved.get(value, 0), worsened.get(value, 0)
            alpha = prior[value]
            di = np.log((ai + alpha) / (ni - ai + prior.sum() - alpha))
            dw = np.log((aw + alpha) / (nw - aw + prior.sum() - alpha))
            variance = 1 / (ai + alpha) + 1 / (aw + alpha)
            rows.append({"attribute": column, "value": value, "improved_count": int(ai),
                         "worsened_count": int(aw), "log_odds_z_improved": float((di - dw) / np.sqrt(variance))})
    return pd.DataFrame(rows).sort_values("log_odds_z_improved", ascending=False)


def archetype(frame: pd.DataFrame, name: str, mask: pd.Series, reason: str) -> dict:
    part = frame.loc[mask]
    return {"name": name, "reason_code": reason, "count": int(len(part)),
            "share_pct": round(100 * len(part) / len(frame), 1),
            "median_position_change": round(float(part.label_position_change.median()), 2)}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True); ASSETS.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(DATA)
    curve = (df.groupby("position_bucket", observed=True)
               .agg(expected_ctr=("expected_ctr", "median"), content_count=("content_hash_id", "size"))
               .reindex(["1-3", "4-6", "7-10", "11-20", "21+"]).reset_index())
    curve.to_csv(RESULTS / "expected_ctr_curve.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    fig.patch.set_facecolor("#f6f3ec"); ax.set_facecolor("#f6f3ec")
    ax.plot(curve.position_bucket, curve.expected_ctr * 100, color="#1f5b45", marker="o", linewidth=2.2)
    for x, y in zip(curve.position_bucket, curve.expected_ctr * 100): ax.text(x, y + .012, f"{y:.1f}%", ha="center", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color="#d9d4c8", linewidth=.7)
    ax.set(title="Expected click-through rate falls sharply with position", xlabel="Average position bucket", ylabel="Median CTR")
    fig.tight_layout(); fig.savefig(ASSETS / "expected_ctr_curve.png", dpi=180, facecolor=fig.get_facecolor()); plt.close(fig)

    archetypes = [
        archetype(df, "CTR opportunity", df.ctr_gap <= df.ctr_gap.quantile(.1), "CTR-GAP-LOW"),
        archetype(df, "Volatile visibility", df.position_volatility_90d >= df.position_volatility_90d.quantile(.9), "POS-VOL-HIGH"),
        archetype(df, "Deteriorating trend", df.position_trend_slope_90d >= df.position_trend_slope_90d.quantile(.9), "POS-TREND-DOWN"),
    ]
    summary = {"rows": int(len(df)), "clients": int(df.client_hash_id.nunique()),
               "feature_window_days": 90, "outcome_window_days": 28,
               "median_position_change": round(float(df.label_position_change.median()), 3),
               "archetypes": archetypes}
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    weighted_log_odds(df).to_csv(RESULTS / "contrastive_log_odds.csv", index=False)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
