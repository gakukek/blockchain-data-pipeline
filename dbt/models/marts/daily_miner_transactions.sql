SELECT b.height, ROUND(SUM(o.value_satoshis) / 1e8, 4) AS miner_revenue_btc
FROM {{ ref('stg_transactions') }} AS t
JOIN {{ref('stg_outputs') }} AS o ON t.tx_hash = o.tx_hash
JOIN {{ ref('stg_blocks') }} AS b ON t.block_hash = b.block_hash
WHERE t.is_coinbase = TRUE
GROUP BY b.height
ORdeR BY b.height