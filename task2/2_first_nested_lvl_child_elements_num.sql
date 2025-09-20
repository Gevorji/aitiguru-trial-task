SELECT count(*)
FROM categories child
JOIN categories parent ON parent.id = child.parent_category_id
WHERE parent.parent_category_id IS NULL
