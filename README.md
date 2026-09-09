# Bitcoin Data Pipeline (local-first)

A Bitcoin blockchain ETL pipeline, built local-first and free before adding
any cloud infra. See [PLAN.md](PLAN.md) for the day-by-day build plan and
current progress.

## Structure
```
extract/     raw data in (today: synthetic sample; later: BigQuery)
transform/   flatten nested blocks -> transactions -> inputs/outputs
load/        write flat tables into a local DuckDB warehouse
run_pipeline.py   ties it all together, end to end
```

## Run it
```
pip install -r requirements.txt
python run_pipeline.py
```
