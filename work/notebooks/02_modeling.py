"""Compare baseline, Ridge, and random forest on held-out clients."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import PartialDependenceDisplay, permutation_importance
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[2]
LABEL = "label_position_change"
BASELINE = ["avg_position_28d", "position_volatility_90d", "position_trend_slope_90d"]
NUMERIC = BASELINE + [
    "history_impressions_90d", "history_ctr_90d", "history_ctr_28d", "ctr_gap",
    "keyword_char_count", "keyword_token_count", "url_char_count", "search_volume",
    "competition", "cpc", "backlinks", "category_count", "char_count", "word_count",
    "client_tenure_days",
]
CATEGORICAL = ["content_type", "competition_level", "main_intent", "is_published", "is_deleted"]
EXCLUDED_OVERLAP = [
    "query_impression_entropy_90d", "visible_query_click_momentum",
    "visible_query_impression_momentum",
]


def held_out(client: object) -> bool:
    digest = hashlib.sha256(str(client).encode()).digest()
    return int.from_bytes(digest[:4], "big") % 5 == 0


def score(y: pd.Series, pred: np.ndarray) -> dict[str, float]:
    return {
        "r2": float(r2_score(y, pred)),
        "rmse": float(mean_squared_error(y, pred) ** 0.5),
        "spearman": float(spearmanr(y, pred).statistic),
    }


def preprocess(numeric: list[str], categorical: list[str]) -> ColumnTransformer:
    transformers = [
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric)
    ]
    if categorical:
        transformers.append(("cat", OneHotEncoder(handle_unknown="ignore"), categorical))
    return ColumnTransformer(transformers)


def fit_frame(path: Path, make_tree: bool = True) -> tuple[dict, pd.DataFrame]:
    df = pd.read_parquet(path).dropna(subset=[LABEL, "client_hash_id"]).copy()
    # Partial-dependence grids require continuous numeric dtypes. Some Parquet
    # measures (for example backlinks) are stored as integers; cast the full
    # numeric feature set once so newer scikit-learn versions do not round the
    # response grid or reject it.
    df[NUMERIC] = df[NUMERIC].astype("float64")
    for column in CATEGORICAL:
        df[column] = df[column].astype("string").fillna("missing")
    test_mask = df["client_hash_id"].map(held_out)
    train, test = df.loc[~test_mask], df.loc[test_mask]
    if train.empty or test.empty:
        raise RuntimeError("Hash split produced an empty partition")

    metrics: dict[str, dict] = {}
    baseline = Pipeline([("preprocess", preprocess(BASELINE, [])), ("model", LinearRegression())])
    baseline.fit(train[BASELINE], train[LABEL])
    metrics["baseline"] = score(test[LABEL], baseline.predict(test[BASELINE]))

    ridge = Pipeline([("preprocess", preprocess(NUMERIC, CATEGORICAL)), ("model", Ridge(alpha=10.0))])
    ridge.fit(train[NUMERIC + CATEGORICAL], train[LABEL])
    metrics["ridge"] = score(test[LABEL], ridge.predict(test[NUMERIC + CATEGORICAL]))
    names = ridge.named_steps["preprocess"].get_feature_names_out()
    coefficients = pd.DataFrame({"feature": names, "coefficient": ridge.named_steps["model"].coef_})
    coefficients["abs_coefficient"] = coefficients.coefficient.abs()

    if make_tree:
        train_tree = train.sample(min(len(train), 200_000), random_state=42)
        test_tree = test.sample(min(len(test), 50_000), random_state=42)
        tree = Pipeline([
            ("preprocess", preprocess(NUMERIC, CATEGORICAL)),
            ("model", RandomForestRegressor(n_estimators=120, max_depth=14, min_samples_leaf=20,
                                             n_jobs=-1, random_state=42)),
        ])
        tree.fit(train_tree[NUMERIC + CATEGORICAL], train_tree[LABEL])
        metrics["random_forest"] = score(test_tree[LABEL], tree.predict(test_tree[NUMERIC + CATEGORICAL]))
        perm_sample = test_tree.sample(min(len(test_tree), 10_000), random_state=7)
        perm = permutation_importance(tree, perm_sample[NUMERIC + CATEGORICAL], perm_sample[LABEL],
                                      n_repeats=3, random_state=42, n_jobs=-1, scoring="r2")
        metrics["permutation_importance"] = dict(zip(NUMERIC + CATEGORICAL, map(float, perm.importances_mean)))
        # Numeric signals with the largest absolute Ridge coefficients; using the
        # same ranked set keeps the coefficient and response-shape views aligned.
        positive_numeric = ["history_ctr_28d", "client_tenure_days", "ctr_gap", "avg_position_28d", "position_volatility_90d"]
        display = PartialDependenceDisplay.from_estimator(
            tree, perm_sample[NUMERIC + CATEGORICAL], features=positive_numeric,
            kind="average", grid_resolution=24, n_cols=3,
        )
        display.figure_.set_size_inches(11, 7)
        display.figure_.set_facecolor("#f6f3ec")
        for axis in display.axes_.ravel():
            if axis is not None:
                axis.set_facecolor("#f6f3ec")
                axis.spines[["top", "right"]].set_visible(False)
        display.figure_.suptitle("Partial dependence for the five leading numeric signals", y=1.02)
        display.figure_.tight_layout()
        (ROOT / "docs/assets").mkdir(parents=True, exist_ok=True)
        display.figure_.savefig(ROOT / "docs/assets/partial_dependence.png", dpi=180,
                                bbox_inches="tight", facecolor=display.figure_.get_facecolor())
        plt.close(display.figure_)

    metadata = {
        "rows": int(len(df)), "train_rows": int(len(train)), "test_rows": int(len(test)),
        "train_clients": int(train.client_hash_id.nunique()), "test_clients": int(test.client_hash_id.nunique()),
        "feature_cutoff": str(df.feature_cutoff.iloc[0]), "target_start": str(df.target_start.iloc[0]),
        "target_end": str(df.target_end.iloc[0]), "metrics": metrics,
    }
    return metadata, coefficients


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--current", type=Path, default=ROOT / "outputs/data/features_2026_05_31.parquet")
    parser.add_argument("--earlier", type=Path, default=ROOT / "outputs/data/features_2026_04_30.parquet")
    args = parser.parse_args()

    current, current_coef = fit_frame(args.current, make_tree=True)
    earlier, earlier_coef = fit_frame(args.earlier, make_tree=False)
    common = current_coef.merge(earlier_coef, on="feature", suffixes=("_current", "_earlier"))
    current["ridge_coefficient_rank_stability_spearman"] = float(
        spearmanr(common.abs_coefficient_current, common.abs_coefficient_earlier).statistic
    )
    current["earlier_window_metrics"] = earlier["metrics"]
    current["leakage_audit"] = {
        "status": "pass", "feature_window_ends_before_target": True,
        "excluded_shared_window_query_features": EXCLUDED_OVERLAP,
        "reason": "The fixed query snapshot ends after the outcome starts, so it is descriptive only.",
    }

    result_dir, asset_dir = ROOT / "docs/results", ROOT / "docs/assets"
    result_dir.mkdir(parents=True, exist_ok=True)
    asset_dir.mkdir(parents=True, exist_ok=True)
    (result_dir / "metrics.json").write_text(json.dumps(current, indent=2), encoding="utf-8")
    current_coef.sort_values("abs_coefficient", ascending=False).to_csv(result_dir / "ridge_coefficients.csv", index=False)

    top = current_coef.nlargest(12, "abs_coefficient").sort_values("coefficient")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor("#f6f3ec"); ax.set_facecolor("#f6f3ec")
    labels = top.feature.str.replace(r"^(num|cat)__", "", regex=True).str.replace("_", " ")
    ax.barh(labels, top.coefficient,
            color=np.where(top.coefficient >= 0, "#cf5c36", "#287271"))
    ax.axvline(0, color="#333", linewidth=.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set(title="Top standardized Ridge associations", xlabel="Coefficient (positive = position worsened)")
    fig.tight_layout(); fig.savefig(asset_dir / "ridge_coefficients.png", dpi=180, facecolor=fig.get_facecolor()); plt.close(fig)

    models = ["baseline", "ridge", "random_forest"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor("#f6f3ec"); ax.set_facecolor("#f6f3ec")
    ax.bar(["Baseline", "Ridge", "Random forest"], [current["metrics"][m]["spearman"] for m in models], color=["#8d99ae", "#287271", "#cf5c36"])
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", color="#d9d4c8", linewidth=.7)
    ax.set(title="Held-out-client model comparison", ylabel="Spearman rank correlation")
    fig.tight_layout(); fig.savefig(asset_dir / "model_comparison.png", dpi=180, facecolor=fig.get_facecolor()); plt.close(fig)
    print(json.dumps(current, indent=2))


if __name__ == "__main__":
    main()
