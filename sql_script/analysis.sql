-- Average Sale Price Query
SELECT 
    AVG("lastSalePrice") AS average_price
FROM 
    zipco.dim_sales
WHERE 
    "lastSalePrice" > 0;

-- Property Count by State Query
SELECT 
    state,
    COUNT(*) AS property_count
FROM 
    zipco.fact_table
GROUP BY 
    state
ORDER BY 
    property_count DESC;
