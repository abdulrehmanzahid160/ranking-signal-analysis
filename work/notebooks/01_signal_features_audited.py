"""Leakage-safe feature builder. Streams remote Parquet and emits one row/content."""

from __future__ import annotations

import argparse, getpass, os
from datetime import date, timedelta
from pathlib import Path
import duckdb
import certifi

ROOT = Path(__file__).resolve().parents[2]
BASE = "hf://datasets/FlyRank/internship-warehouse"
QUERY = f"{BASE}/fact_content_query_90d.parquet"
CONTENT = f"{BASE}/dim_content.parquet"
CLIENTS = f"{BASE}/dim_clients.parquet"

def read_token() -> str:
    return os.getenv("HF_TOKEN") or os.getenv("HF_READ_TOKEN") or getpass.getpass("Hugging Face read token: ")

def build(cutoff: date, output: Path) -> None:
    start90, start28 = cutoff - timedelta(days=89), cutoff - timedelta(days=27)
    out_start, out_end = cutoff + timedelta(days=1), cutoff + timedelta(days=28)
    # Explicit files avoid a remote directory-listing call and enable month pruning.
    cursor = date(start90.year, start90.month, 1)
    paths = []
    while cursor <= out_end:
        paths.append(f"'{BASE}/fact_content_daily_performance/month={cursor:%Y-%m}/data_0.parquet'")
        cursor = date(cursor.year + (cursor.month == 12), cursor.month % 12 + 1, 1)
    daily_files = "[" + ",".join(paths) + "]"
    # DuckDB/httpfs needs an explicit CA bundle on some Windows installations.
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    os.environ.setdefault("CURL_CA_BUNDLE", certifi.where())
    con = duckdb.connect()
    con.execute("LOAD httpfs")
    con.execute("SET ca_cert_file = ?", [certifi.where()])
    con.execute("SET enable_server_cert_verification = true")
    con.execute("SET http_retries = 12")
    con.execute("SET http_retry_wait_ms = 500")
    con.execute("SET http_retry_backoff = 2")
    con.execute("SET http_timeout = 120")
    con.execute("SET http_keep_alive = false")
    con.execute("CREATE SECRET (TYPE huggingface, TOKEN ?)", [read_token()])
    con.execute("SET threads=4"); con.execute("SET preserve_insertion_order=false")
    output.parent.mkdir(parents=True, exist_ok=True)
    sql = f"""
    COPY (
    WITH daily AS (
      SELECT report_date,client_hash_id,content_hash_id,gsc_impressions,gsc_clicks,gsc_avg_position
      FROM read_parquet({daily_files},hive_partitioning=true)
      WHERE report_date BETWEEN DATE '{start90}' AND DATE '{out_end}'
        AND gsc_data_available AND gsc_impressions>0
    ), hist AS (
      SELECT client_hash_id,content_hash_id,COUNT(*) history_observed_days,
        SUM(gsc_impressions) history_impressions_90d,SUM(gsc_clicks) history_clicks_90d,
        SUM(gsc_clicks)::DOUBLE/NULLIF(SUM(gsc_impressions),0) history_ctr_90d,
        AVG(gsc_avg_position) history_avg_position_90d,STDDEV_SAMP(gsc_avg_position) position_volatility_90d,
        REGR_SLOPE(gsc_avg_position,DATE_DIFF('day',DATE '{start90}',report_date)) position_trend_slope_90d
      FROM daily WHERE report_date<=DATE '{cutoff}' GROUP BY 1,2
    ), recent AS (
      SELECT client_hash_id,content_hash_id,COUNT(*) recent_observed_days,
        SUM(gsc_impressions) history_impressions_28d,SUM(gsc_clicks) history_clicks_28d,
        SUM(gsc_clicks)::DOUBLE/NULLIF(SUM(gsc_impressions),0) history_ctr_28d,
        AVG(gsc_avg_position) avg_position_28d,
        CASE WHEN AVG(gsc_avg_position)<4 THEN '1-3' WHEN AVG(gsc_avg_position)<7 THEN '4-6'
             WHEN AVG(gsc_avg_position)<11 THEN '7-10' WHEN AVG(gsc_avg_position)<21 THEN '11-20' ELSE '21+' END position_bucket
      FROM daily WHERE report_date BETWEEN DATE '{start28}' AND DATE '{cutoff}' GROUP BY 1,2
    ), curve AS (
      SELECT position_bucket,MEDIAN(history_ctr_28d) expected_ctr FROM recent
      WHERE recent_observed_days>=7 GROUP BY 1
    ), outcome AS (
      SELECT client_hash_id,content_hash_id,COUNT(*) target_observed_days,SUM(gsc_impressions) target_impressions_28d,
        AVG(gsc_avg_position) target_avg_position_28d
      FROM daily WHERE report_date BETWEEN DATE '{out_start}' AND DATE '{out_end}' GROUP BY 1,2
    ), q0 AS (
      SELECT *,impressions_90d::DOUBLE/NULLIF(content_total_impressions_90d,0) visible_share
      FROM read_parquet('{QUERY}')
    ), qs AS (
      SELECT client_hash_id,content_hash_id,MAX(window_start) query_window_start,MAX(window_end) query_window_end,
        MAX(content_visible_query_count) visible_query_count,MAX(rare_query_count) rare_query_count,
        MAX(rare_impressions_share) rare_impressions_share,MAX(anonymized_impressions_share) anonymized_impressions_share,
        -SUM(CASE WHEN visible_share>0 THEN visible_share*LOG2(visible_share) ELSE 0 END)
        -MAX(CASE WHEN rare_impressions_share>0 THEN rare_impressions_share*LOG2(rare_impressions_share) ELSE 0 END)
        -MAX(CASE WHEN anonymized_impressions_share>0 THEN anonymized_impressions_share*LOG2(anonymized_impressions_share) ELSE 0 END)
          query_impression_entropy_90d,
        SUM(clicks_last30)-SUM(clicks_prev30) visible_query_click_momentum,
        SUM(impressions_last30)-SUM(impressions_prev30) visible_query_impression_momentum
      FROM q0 GROUP BY 1,2
    )
    SELECT h.client_hash_id,h.content_hash_id,DATE '{cutoff}' feature_cutoff,DATE '{out_start}' target_start,DATE '{out_end}' target_end,
      h.history_observed_days,r.recent_observed_days,o.target_observed_days,h.history_impressions_90d,h.history_clicks_90d,
      h.history_ctr_90d,h.history_avg_position_90d,h.position_volatility_90d,h.position_trend_slope_90d,
      r.history_impressions_28d,r.history_clicks_28d,r.history_ctr_28d,r.avg_position_28d,r.position_bucket,
      cv.expected_ctr,r.history_ctr_28d-cv.expected_ctr ctr_gap,o.target_impressions_28d,o.target_avg_position_28d,
      o.target_avg_position_28d-r.avg_position_28d label_position_change,
      q.query_window_start,q.query_window_end,q.visible_query_count,q.rare_query_count,q.rare_impressions_share,
      q.anonymized_impressions_share,q.query_impression_entropy_90d,q.visible_query_click_momentum,q.visible_query_impression_momentum,
      d.keyword_char_count,d.keyword_token_count,d.url_char_count,d.content_type,d.search_volume,d.competition,
      d.competition_level,d.cpc,d.main_intent,d.backlinks,d.category_count,d.char_count,d.word_count,d.is_published,d.is_deleted,
      DATE_DIFF('day',cl.gsc_data_start,DATE '{cutoff}') client_tenure_days
    FROM hist h JOIN recent r USING(client_hash_id,content_hash_id) JOIN outcome o USING(client_hash_id,content_hash_id)
    JOIN curve cv USING(position_bucket) LEFT JOIN qs q USING(client_hash_id,content_hash_id)
    LEFT JOIN read_parquet('{CONTENT}') d USING(client_hash_id,content_hash_id)
    LEFT JOIN read_parquet('{CLIENTS}') cl USING(client_hash_id)
    WHERE h.history_observed_days>=14 AND r.recent_observed_days>=7 AND o.target_observed_days>=7 AND o.target_impressions_28d>=10
    ) TO '{output.as_posix()}' (FORMAT PARQUET,COMPRESSION ZSTD)
    """
    con.execute(sql)
    n, clients, duplicates = con.sql(f"SELECT COUNT(*),COUNT(DISTINCT client_hash_id),COUNT(*)-COUNT(DISTINCT client_hash_id||':'||content_hash_id) FROM read_parquet('{output.as_posix()}')").fetchone()
    if duplicates: raise RuntimeError(f"Non-unique content keys: {duplicates}")
    print({"output":str(output),"rows":n,"clients":clients,"duplicate_keys":duplicates})

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--cutoff",type=date.fromisoformat,default=date(2026,5,31)); p.add_argument("--output",type=Path)
    a=p.parse_args(); out=a.output or ROOT/"outputs/data"/f"features_{a.cutoff:%Y_%m_%d}.parquet"; build(a.cutoff,out.resolve())
