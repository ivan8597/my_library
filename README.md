# Library API

Асинхронный REST API для управления списком книг.

## Возможности

- `POST /books` — добавить книгу;
- `GET /books` — получить все книги;
- `GET /books/{id}` — получить одну книгу;
- `PUT /books/{id}` — полностью обновить книгу;
- `DELETE /books/{id}` — удалить книгу.

Данные хранятся в SQLite-файле `library.db`. Документация Swagger доступна по адресу `/docs`.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

После запуска откройте <http://127.0.0.1:8000/docs>.

## Тесты

```bash
pytest -q
```

## Пример запроса

```bash
curl -X POST http://127.0.0.1:8000/books \\
  -H 'Content-Type: application/json' \\
  -d '{"title":"1984","author":"Джордж Оруэлл","year":1949,"pages":328}'
```
