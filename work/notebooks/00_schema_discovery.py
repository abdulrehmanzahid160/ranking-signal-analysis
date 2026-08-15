"""Discover public-safe warehouse metadata without printing raw records."""

from __future__ import annotations

import getpass
import os
from pathlib import Path

import duckdb
import certifi


BASE = "hf://datasets/FlyRank/internship-warehouse"
TABLES = {
    "dim_clients": f"{BASE}/dim_clients.parquet",
    "dim_content": f"{BASE}/dim_content.parquet",
    "fact_content_daily_performance": f"{BASE}/fact_content_daily_performance/month=*/data_0.parquet",
    "fact_content_daily_performance_sample": f"{BASE}/fact_content_daily_performance_sample.parquet",
    "fact_content_query_90d": f"{BASE}/fact_content_query_90d.parquet",
}


def token() -> str:
    value = os.getenv("HF_TOKEN") or os.getenv("HF_READ_TOKEN")
    return value or getpass.getpass("Hugging Face read token: ")


def connect() -> duckdb.DuckDBPyConnection:
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    os.environ.setdefault("CURL_CA_BUNDLE", certifi.where())
    con = duckdb.connect()
    con.execute("LOAD httpfs")
    con.execute("SET ca_cert_file = ?", [certifi.where()])
    con.execute("SET enable_server_cert_verification = true")
    con.execute("SET http_retries = 12")
    con.execute("SET http_timeout = 120")
    con.execute("CREATE SECRET (TYPE huggingface, TOKEN ?)", [token()])
    return con


def main() -> None:
    con = connect()
    blocks = [
        "# Schema discovery notes\n",
        "Generated from DuckDB metadata only. No raw rows, identifiers, queries, URLs, or credentials are included.\n",
    ]
    for name, path in TABLES.items():
        schema = con.sql(f"DESCRIBE SELECT * FROM read_parquet('{path}')").df()
        count = con.sql(f"SELECT COUNT(*) AS n FROM read_parquet('{path}')").fetchone()[0]
        blocks.extend([f"## {name}\n", schema.to_markdown(index=False), f"\nRow count: {count:,}\n"])

    output = Path(__file__).resolve().parents[2] / "docs" / "schema_notes.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(blocks), encoding="utf-8")
    print(f"Wrote public-safe metadata to {output}")


if __name__ == "__main__":
    main()
