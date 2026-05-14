SELECT
    order_id,
    customer_id,
    product_id,
    CAST(order_date AS DATE) AS order_date,
    quantity,
    total_amount
FROM {{ source('retail_analytics', 'raw_orders') }}
