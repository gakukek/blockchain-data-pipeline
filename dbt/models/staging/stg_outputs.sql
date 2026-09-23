SELECT tx_hash, output_index, address, value_satoshis
FROM {{source('bitcoin', 'outputs')}}