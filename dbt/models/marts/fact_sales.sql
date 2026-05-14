SELECT
    o.order_id,
    o.order_date,
    o.quantity,
    o.total_amount,
    c.customer_id,
    c.name          AS customer_name,
    c.city          AS customer_city,
    c.country       AS customer_country,
    p.product_id,
    p.product_name,
    p.category      AS product_category,
    p.price         AS unit_price
FROM {{ ref('staging_orders') }} o
LEFT JOIN {{ ref('staging_customers') }} c
    ON o.customer_id = c.customer_id
LEFT JOIN {{ ref('staging_products') }} p
    ON o.product_id = p.product_id