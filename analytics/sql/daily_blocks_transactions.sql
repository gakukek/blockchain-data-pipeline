SELECT to_timestamp(timestamp)::DATE AS block_date, COUNT(*) AS block_count, SUM(transaction_count)::BIGINT AS total_transactions
FROM blocks
GROUP BY block_date
ORDER BY block_date;