SELECT
    clients.name,
    coalesce(sum(amount*price_per_unit), 0)
FROM orders
JOIN orders_goods ON orders_goods.order_id = orders.id
JOIN goods ON orders_goods.goods_id = goods.id
RIGHT JOIN clients ON orders.client_id = clients.id
GROUP BY orders.client_id, clients.name
