
  
  create view "bitcoin"."main"."stg_outputs__dbt_tmp" as (
    SELECT tx_hash, output_index, address, value_satoshis
FROM "bitcoin"."main"."outputs"
  );
