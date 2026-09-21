# Bitcoin Data Pipeline — Day-by-Day Plan

Reference architecture: https://github.com/fenniez2334/blockchain-data-pipeline
Approach: build the real extract → transform → load → analyze logic locally
and free first; only add cloud infra (Terraform/VM/Dataproc/Kestra) once the
logic is proven. All tools below are free at this scale.

- [x] **Day 1 — Project skeleton + working pipeline on synthetic data**
  Built extract/transform/load as separate modules, generated a small
  synthetic sample shaped like the real blocks→transactions→inputs/outputs
  schema, and ran the full loop into a local DuckDB file. Goal was just
  to prove the *shape* of the pipeline works, no real data yet.

- [x] **Day 2 — Swap in real data**
  Setting up a GCP billing account for the BigQuery public Bitcoin dataset
  kept failing, so the real-data source is the free mempool.space REST API
  instead. `extract/fetch.py` pulls a small batch of recent blocks (10) and
  each block's transactions, normalizes them into the same
  blocks → transactions → inputs/outputs shape as the synthetic sample, and
  caches the raw blocks in `data/raw/mempool_cache.json` so reruns don't
  hit the API.

- [x] **Day 3 — Harden the transform logic**
  Real data has coinbase transactions with no real inputs and outputs with
  no address; `transform/flatten.py` stores a missing address as NULL.
  Added `transform/validate.py` with `validate_tables()`: null checks on key
  columns, duplicate checks on primary keys, and foreign-key checks
  (transactions → blocks, inputs/outputs → transactions). It runs in
  `run_pipeline.py` between transform and load and raises one error listing
  every failed check.

- [x] **Day 4 — Warehouse + real questions**
  Added `analytics/query.py`, which opens the DuckDB warehouse read-only and
  runs every `.sql` file in `analytics/sql/`, printing each result:
  - `daily_blocks_transactions.sql` — blocks and transactions per day
  - `daily_miner_metrics.sql` — miner revenue (coinbase outputs) per block
  - `address_activity.sql` — most active addresses across inputs and outputs

  Run with `python -m analytics.query`. Note: the `transactions` table only
  holds a sample per block (25), so transaction *volume* comes from
  `blocks.transaction_count`, not from counting rows in `transactions`.
  This is the "daily_blocks_transactions" / "daily_miner_metrics" logic from
  the reference repo's dbt models, written as plain SQL first.

- [ ] **Day 5 — Add dbt-core**
  Install `dbt-duckdb` locally (dbt Cloud not required). Turn the Day 4
  queries into dbt models: `stg_blocks`, `stg_transactions`, then a mart
  model like `daily_blocks_transactions`.

- [ ] **Day 6 — One more mart model + basic dbt tests**
  Add `daily_miner_metrics` or `address_activity`. Add `not_null`/`unique`
  dbt tests on primary keys (tx_hash, block_hash).

- [ ] **Day 7 — Visualize + wrap up**
  Query the dbt mart tables and plot something (Jupyter notebook or a
  small Streamlit app) — block counts over time, miner revenue. Write a
  proper README covering what the pipeline does and why.

- [ ] **Later (optional) — Layer cloud infra back in**
  Once the logic above is solid: Terraform for a GCP VM, Kestra for
  orchestration, Dataproc/Spark if you want to practice at the scale the
  reference repo targets. Infra around logic you understand, not before.