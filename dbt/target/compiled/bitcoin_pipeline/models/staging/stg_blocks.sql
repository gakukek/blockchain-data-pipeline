SELECT
    block_hash,
    height,
    to_timestamp(timestamp) as block_timestamp,
    to_timestamp(timestamp)::date as block_date,
    transaction_count
FROM "bitcoin"."main"."blocks"