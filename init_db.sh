poetry run python -m task3.create_db_tables && \
poetry run python -m task3.exec_sql_script insert_categories.sql && \
poetry run python -m task3.exec_sql_script test_data_fill_in.sql