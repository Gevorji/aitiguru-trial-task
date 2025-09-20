WITH RECURSIVE categories_paths(id, name, parent_category_id, path) AS (
    SELECT id, name, parent_category_id, name AS path
    FROM categories
    WHERE parent_category_id IS NULL
    UNION ALL
    SELECT cat.id, cat.name, cat.parent_category_id, pathed_cat.path || '.' || cat.name
    FROM categories_paths pathed_cat
    JOIN categories cat ON cat.parent_category_id = pathed_cat.id
)
SELECT goods.name AS "Наименование товара",
       (string_to_array(path, '.'))[1] AS "Категория",
       SUM(amount) AS "Количество продаж"
FROM goods
JOIN orders_goods ON orders_goods.goods_id = goods.id
JOIN categories_paths ON categories_paths.id = goods.category_id
GROUP BY goods_id, goods.name, path
ORDER BY "Количество продаж" DESC
LIMIT 5;