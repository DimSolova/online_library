# Library Backend

Бэкенд для системы управления библиотекой (FastAPI + SQLAlchemy 2.0 + PostgreSQL).

## Текущий статус

- Настроена структура проекта
- Добавлены базовые модели: `User` и `Role`
- Подготовлена конфигурация через Pydantic Settings
- Готовится настройка Alembic для миграций

## Технологии

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL + asyncpg
- Pydantic v2
- Alembic (миграции)

## Вспомогательные команды

docker network create libraryNetwork

docker run --name library_db \
-p 6432:5432 \
-e POSTGRES_USER=abcde \
-e POSTGRES_PASSWORD=abcde \
-e POSTGRES_DB=library \
--network=libraryNetwork \
-d postgres:16

docker run --name library \
-p 8888:8000 \
--network=libraryNetwork \
library_image
