SELECT
    tx_hash,
    block_hash,
    is_coinbase,
    input_count,
    output_count
FROM {{ source('bitcoin', 'transactions') }}