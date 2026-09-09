"""
Day 1 pipeline run: extract -> transform -> load -> a sanity query.

Usage:
    python run_pipeline.py
"""

import duckdb

from extract.fetch import get_raw_blocks
from load.warehouse import DB_PATH, load_tables
from transform.flatten import flatten_blocks


def main():
    print("1/3 extract: loading raw blocks...")
    raw_blocks = get_raw_blocks()
    print(f"    -> {len(raw_blocks)} blocks, "
          f"{sum(b['transaction_count'] for b in raw_blocks)} transactions")

    print("2/3 transform: flattening nested inputs/outputs...")
    tables = flatten_blocks(raw_blocks)
    for name, df in tables.items():
        print(f"    -> {name}: {len(df)} rows")

    print("3/3 load: writing to local DuckDB warehouse...")
    load_tables(tables)
    print(f"    -> wrote {DB_PATH}")

    print("\nSanity query -- total output value (BTC) per block:")
    con = duckdb.connect(str(DB_PATH))
    result = con.execute("""
        SELECT
            b.height,
            b.transaction_count,
            ROUND(SUM(o.value_satoshis) / 1e8, 4) AS total_output_btc
        FROM blocks b
        JOIN transactions t ON t.block_hash = b.block_hash
        JOIN outputs o ON o.tx_hash = t.tx_hash
        GROUP BY b.height, b.transaction_count
        ORDER BY b.height
    """).fetchdf()
    print(result.to_string(index=False))
    con.close()


if __name__ == "__main__":
    main()
