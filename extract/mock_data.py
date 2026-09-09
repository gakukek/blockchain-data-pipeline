"""
Generates a small SYNTHETIC sample of Bitcoin block/transaction data.

This is not real chain data. It's shaped to loosely mirror the nested
structure of the public bigquery-public-data.crypto_bitcoin dataset
(blocks -> transactions -> inputs[] / outputs[]), so the transform step
you write against it is the same transform step you'll later point at
real data. Swap `load_raw_blocks()` in extract/fetch.py for a real
BigQuery query later without touching transform.py or load.py at all.
"""

import json
import random
from pathlib import Path

RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "sample_blocks.json"


def _fake_address(seed: int) -> str:
    return f"bc1q{seed:0>8x}fakeaddr"


def generate_sample_blocks(n_blocks: int = 3, seed: int = 42) -> list[dict]:
    rng = random.Random(seed)
    blocks = []
    base_height = 900_000
    base_ts = 1_735_000_000  # arbitrary unix ts

    tx_counter = 0
    for b in range(n_blocks):
        height = base_height + b
        block_hash = f"00000000000000000{b:016x}"
        block_ts = base_ts + b * 600  # ~10 min per block

        n_tx = rng.randint(2, 4)
        transactions = []
        for t in range(n_tx):
            tx_counter += 1
            tx_hash = f"tx{tx_counter:010x}"

            is_coinbase = t == 0  # first tx in a block is the miner reward
            n_inputs = 0 if is_coinbase else rng.randint(1, 2)
            n_outputs = rng.randint(1, 3)

            inputs = []
            for i in range(n_inputs):
                inputs.append({
                    "index": i,
                    "spent_transaction_hash": f"tx{rng.randint(1, max(tx_counter - 1, 1)):010x}",
                    "spent_output_index": rng.randint(0, 2),
                    "addresses": [_fake_address(rng.randint(1, 50))],
                    "value": rng.randint(1000, 500_000_000),  # satoshis
                })

            outputs = []
            for o in range(n_outputs):
                outputs.append({
                    "index": o,
                    "addresses": [_fake_address(rng.randint(1, 50))],
                    "value": rng.randint(1000, 500_000_000),  # satoshis
                })

            transactions.append({
                "hash": tx_hash,
                "is_coinbase": is_coinbase,
                "input_count": n_inputs,
                "output_count": n_outputs,
                "inputs": inputs,
                "outputs": outputs,
            })

        blocks.append({
            "hash": block_hash,
            "height": height,
            "timestamp": block_ts,
            "transaction_count": n_tx,
            "transactions": transactions,
        })

    return blocks


def write_sample_blocks(n_blocks: int = 3, seed: int = 42) -> Path:
    blocks = generate_sample_blocks(n_blocks=n_blocks, seed=seed)
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(blocks, indent=2))
    return RAW_PATH


if __name__ == "__main__":
    path = write_sample_blocks()
    print(f"Wrote synthetic sample blocks to {path}")
