# Redis + FastAPI + PostgreSQL

Простенький REST API на FastAPI с PostgreSQL и Redis-кэширования.

## Возможности
- CRUD для items
- Кэширование списка items в Redis
- Docker Compose для запуска

## Быстрый старт

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```sh
   git clone https://github.com/omeraen/Redis_FastAPI_PostgreSQL.git
   ```
2. Создайте файл `.env` (пример ниже).
   ```
   DATABASE_URL=postgresql+psycopg2://postgres:example@db:5432/yourdbname
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

4. Запустите сервисы:
   ```sh
   docker-compose up -d --build
   ```
5. Приложение будет доступно на [http://localhost:8000](http://localhost:8000)

## Пример .env
```
DATABASE_URL=postgresql+psycopg2://postgres:example@db:5432/yourdbname
REDIS_HOST=redis
REDIS_PORT=6379
```

## Описание API
- `GET /items/nocache` — получить список items напрямую из БД
- `GET /items/cache` — получить список items с кэшированием через Redis
- `POST /items?name=...` — добавить новый item (инвалидирует кэш)

## Документация
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Остановка
```sh
docker-compose down
```
