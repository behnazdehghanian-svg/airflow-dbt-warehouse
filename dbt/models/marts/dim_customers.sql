SELECT
    c.customer_id,      -- customer ID
    c.name,             -- customer name
    c.email,            -- customer email
    c.city,             -- customer city
    c.country,          -- customer country
    COUNT(o.order_id)   AS total_orders,    -- how many orders?
    SUM(o.total_amount) AS total_spent,     -- how much spent?
    MIN(o.order_date)   AS first_order_date, -- first order date
    MAX(o.order_date)   AS last_order_date   -- last order date
FROM {{ ref('staging_customers') }} c   -- customer table
LEFT JOIN {{ ref('staging_orders') }} o -- join with orders
    ON c.customer_id = o.customer_id    -- match by customer_id
GROUP BY
    c.customer_id, c.name, c.email, c.city, c.country