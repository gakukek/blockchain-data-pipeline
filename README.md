# Bitcoin Data Pipeline (local-first)

A Bitcoin blockchain ETL pipeline, built local-first and free before adding
any cloud infra. See [PLAN.md](PLAN.md) for the day-by-day build plan and
current progress.

## Structure
```
extract/     raw data in (mempool.space API, cached locally; synthetic sample in mock_data.py)
transform/   flatten nested blocks -> transactions -> inputs/outputs, then validate them
load/        write flat tables into a local DuckDB warehouse
analytics/   SQL queries (analytics/sql/*.sql) run against the warehouse
run_pipeline.py   ties extract -> transform -> validate -> load together, end to end
```

## Run it
```
pip install -r requirements.txt
python run_pipeline.py        # build the warehouse
python -m analytics.query     # run every SQL file in analytics/sql/
```

The analytics step prints one table per query: blocks and transactions per
day, miner revenue per block, and the most active addresses.