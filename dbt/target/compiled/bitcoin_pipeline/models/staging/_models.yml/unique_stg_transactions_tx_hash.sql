
    
    

select
    tx_hash as unique_field,
    count(*) as n_records

from "bitcoin"."main"."stg_transactions"
where tx_hash is not null
group by tx_hash
having count(*) > 1


