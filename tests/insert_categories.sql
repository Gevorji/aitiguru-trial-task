INSERT INTO categories(name)
VALUES
    ('Бытовая техника'),
    ('Компьютеры');


INSERT INTO categories(name, parent_category_id)
SELECT vals.name, (SELECT id FROM categories c WHERE c.name='Бытовая техника')
FROM (
    VALUES
        ('Стиральные машины'),
        ('Холодильники'),
        ('Телевизоры')
) AS vals(name);

INSERT INTO categories(name, parent_category_id)
SELECT vals.name, (SELECT id FROM categories c WHERE c.name='Холодильники')
FROM (
    VALUES
        ('однокамерные'),
        ('двухкамерные')
) AS vals(name);

INSERT INTO categories(name, parent_category_id)
SELECT vals.name, (SELECT id FROM categories c WHERE c.name='Компьютеры')
FROM (
    VALUES
        ('Ноутбуки'),
        ('Моноблоки')
) AS vals(name);

INSERT INTO categories(name, parent_category_id)
SELECT vals.name, (SELECT id FROM categories c WHERE c.name='Ноутбуки')
FROM (
    VALUES
        ('17″'),
        ('19″')
) AS vals(name);