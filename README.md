# Схема данных

![](/data_scheme.jpg)

# Запуск проекта

Склонировать репозиторий к себе

Создать файл `.env` с переменными окружения [наподобие образца](https://github.com/Gevorji/aitiguru-trial-task/blob/8ac0a823fc740508e79190571c385423355bc48e/.env.example).

Находясь в корневой директории проекта, поднять docker-контейнеры и запустить приложение командой:

```bash
docker compose -f docker/docker-compose.yaml up
```

Далее необходимо создать таблицы и вставить в них данные:

```bash
docker compose -f docker/docker-compose.yaml exec task3_service sh init_db.sh 
```

Приложение работает по адресу 127.0.0.1:8080 :)

# Документация

Посмотреть документацию в Swagger UI можно на эндпоинте /docs сервиса.