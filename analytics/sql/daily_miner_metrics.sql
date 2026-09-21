SELECT b.height, ROUND(SUM(o.value_satoshis) / 1e8, 4) AS miner_revenue_btc
FROM transactions t
JOIN outputs o ON t.tx_hash = o.tx_hash
JOIN blocks b ON t.block_hash = b.block_hash
WHERE t.is_coinbase = TRUE
GROUP BY b.height
ORDER BY b.height;