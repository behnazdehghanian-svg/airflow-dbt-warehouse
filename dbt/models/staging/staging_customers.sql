SELECT
    customer_id,
    name,
    email,
    city,
    country
FROM {{ source('retail_analytics', 'raw_customers') }}
