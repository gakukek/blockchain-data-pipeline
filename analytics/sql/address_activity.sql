WITH all_addresses AS (
    SELECT address FROM outputs
    UNION ALL
    SELECT address FROM inputs
)
SELECT address, COUNT(*) AS appearances
FROM all_addresses
WHERE address IS NOT NULL
GROUP BY address
ORDER BY appearances DESC, address
LIMIT 10;