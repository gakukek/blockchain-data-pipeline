"""
Load layer.

Writes the flattened tables into a local DuckDB file -- this stands in
for BigQuery from the reference repo. Same idea (a real SQL warehouse),
zero cost, no server to run.
"""

from pathlib import Path

import duckdb
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "warehouse" / "bitcoin.duckdb"


def load_tables(tables: dict[str, pd.DataFrame], db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    for name, df in tables.items():
        con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM df")
    con.close()


if __name__ == "__main__":
    from extract.fetch import get_raw_blocks
    from transform.flatten import flatten_blocks
    from transform.validate import validate_tables

    tables = flatten_blocks(get_raw_blocks())
    validate_tables(tables)
    load_tables(tables)
    print(f"Loaded {list(tables.keys())} into {DB_PATH}")
