# Schema discovery notes

This file contains the verified public-safe schema output from the first successful DuckDB inspection of the FlyRank HF warehouse tables.

## dim_clients

| column_name | column_type | null | key | default | extra |
|---|---|---|---|---|---|
| client_hash_id | VARCHAR | YES | None | None | None |
| is_active | BOOLEAN | YES | None | None | None |
| has_gsc_access | BOOLEAN | YES | None | None | None |
| has_ga4_access | BOOLEAN | YES | None | None | None |
| access_profile | VARCHAR | YES | None | None | None |
| client_created_date | DATE | YES | None | None | None |
| client_updated_date | DATE | YES | None | None | None |
| gsc_data_start | DATE | YES | None | None | None |
| ga4_data_start | DATE | YES | None | None | None |

Row count: 104

## dim_content

| column_name | column_type | null | key | default | extra |
|---|---|---|---|---|---|
| client_hash_id | VARCHAR | YES | None | None | None |
| content_hash_id | VARCHAR | YES | None | None | None |
| keyword_hash_id | VARCHAR | YES | None | None | None |
| url_hash_id | VARCHAR | YES | None | None | None |
| keyword_char_count | BIGINT | YES | None | None | None |
| keyword_token_count | BIGINT | YES | None | None | None |
| url_char_count | BIGINT | YES | None | None | None |
| content_created_date | DATE | YES | None | None | None |
| content_updated_date | DATE | YES | None | None | None |
| content_type | VARCHAR | YES | None | None | None |
| search_volume | BIGINT | YES | None | None | None |
| competition | DOUBLE | YES | None | None | None |
| competition_level | VARCHAR | YES | None | None | None |
| cpc | DOUBLE | YES | None | None | None |
| main_intent | VARCHAR | YES | None | None | None |
| backlinks | BIGINT | YES | None | None | None |
| category_count | BIGINT | YES | None | None | None |
| keyword_created_date | DATE | YES | None | None | None |
| provider_used | VARCHAR | YES | None | None | None |
| model_used | VARCHAR | YES | None | None | None |
| char_count | BIGINT | YES | None | None | None |
| word_count | BIGINT | YES | None | None | None |
| last_optimized_date | DATE | YES | None | None | None |
| optimization_eligible_date | DATE | YES | None | None | None |
| is_published | BOOLEAN | YES | None | None | None |
| is_deleted | BOOLEAN | YES | None | None | None |

Row count: 519606

## fact_content_daily_performance

| column_name | column_type | null | key | default | extra |
|---|---|---|---|---|---|
| report_date | DATE | YES | None | None | None |
| client_hash_id | VARCHAR | YES | None | None | None |
| content_hash_id | VARCHAR | YES | None | None | None |
| client_has_gsc | BOOLEAN | YES | None | None | None |
| client_has_ga4 | BOOLEAN | YES | None | None | None |
| gsc_data_available | BOOLEAN | YES | None | None | None |
| ga4_data_available | BOOLEAN | YES | None | None | None |
| gsc_impressions | BIGINT | YES | None | None | None |
| gsc_clicks | BIGINT | YES | None | None | None |
| gsc_sum_position | BIGINT | YES | None | None | None |
| gsc_avg_position | DOUBLE | YES | None | None | None |
| ga4_pageviews | BIGINT | YES | None | None | None |
| ga4_sessions | BIGINT | YES | None | None | None |
| ga4_users | BIGINT | YES | None | None | None |
| ga4_engaged_sessions | BIGINT | YES | None | None | None |
| ga4_total_engagement_sec | BIGINT | YES | None | None | None |
| sessions_organic | BIGINT | YES | None | None | None |
| sessions_direct | BIGINT | YES | None | None | None |
| sessions_referral | BIGINT | YES | None | None | None |
| sessions_social | BIGINT | YES | None | None | None |
| sessions_paid | BIGINT | YES | None | None | None |
| sessions_ai | BIGINT | YES | None | None | None |
| ai_chatgpt | BIGINT | YES | None | None | None |
| ai_perplexity | BIGINT | YES | None | None | None |
| ai_gemini | BIGINT | YES | None | None | None |
| ai_copilot | BIGINT | YES | None | None | None |
| ai_claude | BIGINT | YES | None | None | None |
| ai_meta | BIGINT | YES | None | None | None |
| ai_other | BIGINT | YES | None | None | None |
| scroll_events | BIGINT | YES | None | None | None |
| month | VARCHAR | YES | None | None | None |

Row count: 78,835,655

## fact_content_daily_performance_sample

This is the latest full month sample file and was used as the starting point for feature engineering in the analysis repo.

Same schema as `fact_content_daily_performance`. Row count: 11,694,072

## fact_content_query_90d

| column_name | column_type | null | key | default | extra |
|---|---|---|---|---|---|
| client_hash_id | VARCHAR | YES | None | None | None |
| content_hash_id | VARCHAR | YES | None | None | None |
| query_hash_id | VARCHAR | YES | None | None | None |
| query_char_count | BIGINT | YES | None | None | None |
| query_token_count | BIGINT | YES | None | None | None |
| window_start | DATE | YES | None | None | None |
| window_end | DATE | YES | None | None | None |
| impressions_90d | BIGINT | YES | None | None | None |
| clicks_90d | BIGINT | YES | None | None | None |
| impressions_last30 | BIGINT | YES | None | None | None |
| clicks_last30 | BIGINT | YES | None | None | None |
| impressions_prev30 | BIGINT | YES | None | None | None |
| clicks_prev30 | BIGINT | YES | None | None | None |
| avg_position_90d | DOUBLE | YES | None | None | None |
| avg_position_last30 | DOUBLE | YES | None | None | None |
| avg_position_prev30 | DOUBLE | YES | None | None | None |
| content_total_impressions_90d | BIGINT | YES | None | None | None |
| content_visible_query_count | BIGINT | YES | None | None | None |
| rare_query_count | BIGINT | YES | None | None | None |
| rare_impressions_share | DOUBLE | YES | None | None | None |
| anonymized_impressions_share | DOUBLE | YES | None | None | None |

Row count: 2,414,248

Public-safe rule: this file only records schema metadata and row counts. No raw client IDs, domains, URLs, credentials, or identifying query examples are included.
