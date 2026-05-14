SELECT
    product_id,
    name AS product_name,
    category,
    price
FROM {{ source('retail_analytics', 'raw_products') }}
