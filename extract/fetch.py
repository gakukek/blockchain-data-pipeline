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

from extract.mock_data import RAW_PATH, write_sample_blocks



def fetch_blocks_raw() -> list[dict]:
    x = requests.get("https://mempool.space/api/blocks")
    return x.json()

def fetch_blocks(block_id: str) -> list[dict]:
    # Placeholder for fetching a specific block by hash
    # This would typically involve a different API endpoint or query
    x = requests.get(f"https://mempool.space/api/block/{block_id}/txs")
    return x.json()

def normalize_blocks(raw_blocks: list[dict]) -> list[dict]:
    # Placeholder for normalizing the raw blocks data
    # This function would transform the raw API response into the expected format
    return raw_blocks

def get_raw_blocks() -> list[dict]:
    """
    Return a list of blocks, each with a "transactions" list.
    """
    if not RAW_PATH.exists():
        print(f"Fetching raw blocks from mempool.space and writing to {RAW_PATH}...")
        raw_blocks = fetch_blocks_raw()

    else:
        print(f"Loading raw blocks from {RAW_PATH}...")
        with open(RAW_PATH) as f:
            raw_blocks = json.load(f)

    return normalize_blocks(raw_blocks)


if __name__ == "__main__":
    blocks = get_raw_blocks()
    print(f"Loaded {len(blocks)} blocks, "
          f"{sum(b['transaction_count'] for b in blocks)} transactions")
