"""
Extract layer.

get_raw_blocks() is the one function the rest of the pipeline depends on.
Today it reads the local synthetic sample (extract/mock_data.py) so the
whole pipeline runs for free with no cloud account needed.

Keep the return shape (list[dict] of blocks, each with a "transactions"
list) the same, and transform.py / load.py won't need to change at all.
"""

import json
import requests
from pathlib import Path



write_path = Path("data/raw/mempool_cache.json")

def fetch_blocks_raw() -> list[dict]:
    x = requests.get("https://mempool.space/api/blocks")
    return x.json()

def fetch_txs(block_hash: str) -> list[dict]:
    x = requests.get(f"https://mempool.space/api/block/{block_hash}/txs")
    return x.json()

def normalize_blocks(raw_blocks: list[dict]) -> list[dict]:
    normalized_blocks = []
    for block in raw_blocks:
        block_hash = block["id"]
        transactions = fetch_txs(block_hash)
        normalized_txs = []

        for tx in transactions:
            vin = tx.get("vin", [])
            vout = tx.get("vout", [])

            inputs = []
            for i, inp in enumerate(vin):
                prevout = inp.get("prevout") or {}
                inputs.append({
                    "index": i,
                    "spent_transaction_hash": inp.get("txid"),
                    "spent_output_index": inp.get("vout"),
                    "addresses": [prevout["scriptpubkey_address"]] if prevout.get("scriptpubkey_address") else [],
                    "value": prevout.get("value"),
                })

            outputs = []
            for i, out in enumerate(vout):
                outputs.append({
                    "index": i,
                    "addresses": [out["scriptpubkey_address"]] 
                        if out.get("scriptpubkey_address") else [],
                    "value": out.get("value"),
                })
            normalized_txs.append({
                "hash": tx["txid"],
                "is_coinbase": vin[0].get("is_coinbase", False) if vin else False,
                "input_count": len(vin),
                "output_count": len(vout),
                "inputs": inputs,
                "outputs": outputs,
            })

        normalized_blocks.append({
            "hash": block_hash,
            "height": block["height"],
            "timestamp": block["timestamp"],
            "transaction_count": block["tx_count"],
            "transactions": normalized_txs,
        })
    return normalized_blocks

def get_raw_blocks() -> list[dict]:
    """
    Return a list of blocks, each with a "transactions" list.
    """
    if not write_path.exists():
        print(f"Fetching raw blocks from mempool.space and writing to {write_path}...")
        raw_blocks = fetch_blocks_raw()
        write_path.write_text(json.dumps(raw_blocks, indent=2))
    else:
        print(f"Loading raw blocks from {write_path}...")
        with open(write_path) as f:
            raw_blocks = json.load(f)

    return normalize_blocks(raw_blocks)


if __name__ == "__main__":
    blocks = get_raw_blocks()
    print(f"Loaded {len(blocks)} blocks, "
          f"{sum(b['transaction_count'] for b in blocks)} transactions")
