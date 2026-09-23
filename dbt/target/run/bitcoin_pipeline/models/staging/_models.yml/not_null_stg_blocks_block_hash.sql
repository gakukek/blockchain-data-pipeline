
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select block_hash
from "bitcoin"."main"."stg_blocks"
where block_hash is null



  
  
      
    ) dbt_internal_test