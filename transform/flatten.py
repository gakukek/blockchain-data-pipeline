"""
Transform layer.

Takes the nested raw blocks (blocks -> transactions -> inputs[]/outputs[])
and flattens them into 4 flat tables, matching the shape the reference
repo builds with a Spark/Dataproc job -- just done here with pandas on a
small local slice, which is all you need while you're learning the logic.
"""

import pandas as pd


def flatten_blocks(raw_blocks: list[dict]) -> dict[str, pd.DataFrame]:
    block_rows = []
    tx_rows = []
    input_rows = []
    output_rows = []

    for block in raw_blocks:
        block_rows.append({
            "block_hash": block["hash"],
            "height": block["height"],
            "timestamp": block["timestamp"],
            "transaction_count": block["transaction_count"],
        })

        for tx in block["transactions"]:
            tx_rows.append({
                "tx_hash": tx["hash"],
                "block_hash": block["hash"],
                "is_coinbase": tx["is_coinbase"],
                "input_count": tx["input_count"],
                "output_count": tx["output_count"],
            })

            for inp in tx["inputs"]:
                input_rows.append({
                    "tx_hash": tx["hash"],
                    "input_index": inp["index"],
                    "spent_transaction_hash": inp["spent_transaction_hash"],
                    "spent_output_index": inp["spent_output_index"],
                    "address": inp["addresses"][0] if inp["addresses"] else None,
                    "value_satoshis": inp["value"],
                })

            for out in tx["outputs"]:
                output_rows.append({
                    "tx_hash": tx["hash"],
                    "output_index": out["index"],
                    "address": out["addresses"][0] if out["addresses"] else None,
                    "value_satoshis": out["value"],
                })

    return {
        "blocks": pd.DataFrame(block_rows),
        "transactions": pd.DataFrame(tx_rows),
        "inputs": pd.DataFrame(input_rows),
        "outputs": pd.DataFrame(output_rows),
    }


if __name__ == "__main__":
    from extract.fetch import get_raw_blocks

    tables = flatten_blocks(get_raw_blocks())
    for name, df in tables.items():
        print(f"{name}: {len(df)} rows")
        print(df.head(3), "\n")
