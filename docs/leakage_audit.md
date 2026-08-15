# Leakage audit

Primary outcome: change from the trailing 28-day average position at the feature cutoff to the average position during the following 28 days. Positive values mean position numerically increased (visibility worsened).

| Signal family | Window | Primary model | Decision |
|---|---|---:|---|
| Position dynamics | 90 days ending at cutoff | Yes | Pre-outcome |
| CTR and CTR gap | 28/90 days ending at cutoff | Yes | Pre-outcome |
| Content/client controls | Known at cutoff or static | Yes | Control variables |
| Query entropy and momentum | Fixed 2026-04-02 to 2026-06-30 snapshot | No | Overlaps June outcome; descriptive only |
| Target position movement | 28 days after cutoff | Label | No feature rows overlap |

The same deterministic client-hash rule assigns roughly 20% of clients to the held-out set in every month. Identifiers are used only for joins/grouping and never appear in public results.
