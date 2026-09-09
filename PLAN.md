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

- [ ] **Day 2 — Swap in real data**
  Set up a free GCP project (BigQuery sandbox mode needs no credit card).
  Replace `extract/fetch.py`'s body with a real query against
  `bigquery-public-data.crypto_bitcoin.blocks`/`transactions`, scoped to
  ONE day of blocks with a hard `LIMIT` (the real tables are huge — always
  filter by date, never `SELECT *` unbounded). transform.py and load.py
  should need zero changes if the raw shape matches.

- [ ] **Day 3 — Harden the transform logic**
  Real data will break the synthetic assumptions: coinbase transactions
  with no inputs, transactions with multiple addresses per output,
  missing/null address arrays. Add a few `assert`/test cases in
  `transform/flatten.py` for these edge cases.

- [ ] **Day 4 — Warehouse + real questions**
  Add a couple more SQL queries against the DuckDB tables: transaction
  volume per day, miner revenue trend, most active addresses. This is the
  "daily_blocks_transactions" / "daily_miner_metrics" logic from the
  reference repo's dbt models, written as plain SQL first.

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
