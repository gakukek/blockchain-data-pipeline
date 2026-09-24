"""
Plot results from the warehouse.

Run from the project root:  python -m analytics.plot
Writes PNG charts into docs/ so the README can embed them.
"""

from pathlib import Path

import duckdb
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "warehouse" / "bitcoin.duckdb"
OUT_DIR = ROOT / "docs"


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    con = duckdb.connect(str(DB_PATH), read_only=True)

    # Per-block view: the daily mart only has 1 row (all 10 blocks share a date),
    # so a per-block chart is more informative than a per-day one.
    blocks = con.execute(
        "SELECT height, transaction_count FROM stg_blocks ORDER BY height"
    ).df()
    miner = con.execute(
        "SELECT height, miner_revenue_btc FROM daily_miner_transactions ORDER BY height"
    ).df()
    con.close()

    # Chart 1: transactions per block
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(blocks["height"].astype(str), blocks["transaction_count"])
    ax.set_title("Transactions per block")
    ax.set_xlabel("Block height")
    ax.set_ylabel("Transactions")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "transactions_per_block.png", dpi=150)
    plt.close(fig)

    # Chart 2: miner revenue per block
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(miner["height"].astype(str), miner["miner_revenue_btc"])
    ax.set_title("Miner revenue per block (coinbase outputs)")
    ax.set_xlabel("Block height")
    ax.set_ylabel("BTC")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "miner_revenue_per_block.png", dpi=150)
    plt.close(fig)

    print(f"Saved charts to {OUT_DIR}")


if __name__ == "__main__":
    main()