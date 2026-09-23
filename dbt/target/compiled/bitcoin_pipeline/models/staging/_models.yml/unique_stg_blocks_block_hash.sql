
    
    

select
    block_hash as unique_field,
    count(*) as n_records

from "bitcoin"."main"."stg_blocks"
where block_hash is not null
group by block_hash
having count(*) > 1


