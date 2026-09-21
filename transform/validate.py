import pandas as pd

def validate_tables(tables: dict[str, pd.DataFrame]) -> None:
    errors = []

    transactions = tables["transactions"]
    inputs = tables["inputs"]
    outputs = tables["outputs"]

    print(f"Validating {len(tables.get('blocks', pd.DataFrame()))} blocks, "
          f"{len(transactions)} transactions, "
          f"{len(inputs)} inputs, "
          f"{len(outputs)} outputs")

    #null checks
    if transactions["tx_hash"].isnull().any():
        errors.append("Null tx_hash found in transactions")
    if tables["blocks"]["block_hash"].isnull().any():
        errors.append("Null block_hash found in blocks")
    if inputs["tx_hash"].isnull().any():
        errors.append("Null tx_hash found in inputs")
    if outputs["tx_hash"].isnull().any():
        errors.append("Null tx_hash found in outputs")

    #dupes check
    if transactions["tx_hash"].duplicated().any():
        errors.append("Duplicate tx_hash found in transactions")
    if tables["blocks"]["block_hash"].duplicated().any():
        errors.append("Duplicate block_hash found in blocks")
    if inputs[["tx_hash", "input_index"]].duplicated().any():
        errors.append("Duplicate (tx_hash, input_index) found in inputs")
    if outputs[["tx_hash", "output_index"]].duplicated().any():
        errors.append("Duplicate (tx_hash, output_index) found in outputs")

    # foreign key checks
    if not transactions["block_hash"].isin(tables["blocks"]["block_hash"]).all():
        errors.append("Some transactions have block_hash not found in blocks")
    if not inputs["tx_hash"].isin(transactions["tx_hash"]).all():
        errors.append("Some inputs have tx_hash not found in transactions")
    if not outputs["tx_hash"].isin(transactions["tx_hash"]).all():
        errors.append("Some outputs have tx_hash not found in transactions")

    if errors:
        raise ValueError("Validation errors found:\n" + "\n".join(errors))