
    

    create  table
      "bitcoin"."main"."daily_blocks_transactions__dbt_tmp"
  
    
    as (
      SELECT
    block_date,
    count(*) as block_count,
    sum(transaction_count) as total_transactions
FROM "bitcoin"."main"."stg_blocks"
GROUP BY block_date
ORDER BY block_date
    );
    
  