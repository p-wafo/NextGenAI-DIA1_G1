--C04
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON p.product_id = o.product_id
WHERE o.date >= '2026-01-01 00:00:00'
  AND o.date <  '2026-10-01 00:00:00';

--C05
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON p.product_id = o.product_id
WHERE o.date >= '2026-06-01 00:00:00'
  AND o.date <  '2026-06-02 00:00:00';

--C06
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN product p ON p.product_id = o.product_id
WHERE o.date >= '2025-01-01 00:00:00'
  AND o.date <  '2026-01-01 00:00:00';