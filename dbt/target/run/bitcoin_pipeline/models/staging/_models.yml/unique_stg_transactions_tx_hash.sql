
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    tx_hash as unique_field,
    count(*) as n_records

from "bitcoin"."main"."stg_transactions"
where tx_hash is not null
group by tx_hash
having count(*) > 1



  
  
      
    ) dbt_internal_test