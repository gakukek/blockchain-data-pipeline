
  
  create view "bitcoin"."main"."stg_transactions__dbt_tmp" as (
    SELECT
    tx_hash,
    block_hash,
    is_coinbase,
    input_count,
    output_count
FROM "bitcoin"."main"."transactions"
  );
