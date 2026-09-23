
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    block_hash as unique_field,
    count(*) as n_records

from "bitcoin"."main"."stg_blocks"
where block_hash is not null
group by block_hash
having count(*) > 1



  
  
      
    ) dbt_internal_test