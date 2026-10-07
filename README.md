# My Library API

Асинхронный REST API на FastAPI для управления списком книг. Данные сохраняются в SQLite-файле `library.db`.

## Запуск

Требуется Python 3.11 или новее.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

После запуска:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Файл `library.db` создаётся автоматически при первом запуске.

## Эндпоинты

| Метод | Путь | Назначение |
|---|---|---|
| POST | `/books` | Добавить книгу |
| GET | `/books` | Получить все книги |
| GET | `/books/{id}` | Получить одну книгу |
| PUT | `/books/{id}` | Полностью обновить книгу |
| DELETE | `/books/{id}` | Удалить книгу |

## Пример тела запроса

```json
{
  "title": "1984",
  "author": "Джордж Оруэлл",
  "year": 1949,
  "pages": 328,
  "is_read": false
}
```

`pages` должно быть больше 10. Поле `is_read` по умолчанию равно `false`.

## Архитектура

- `main.py` — запуск приложения и подключение роутера;
- `database.py` — асинхронное подключение к SQLite и сессии;
- `models/` — SQLAlchemy-модели таблиц;
- `schemas/` — Pydantic-валидация;
- `routers/` — HTTP-эндпоинты;
- `repository.py` — весь SQL-код и операции с БД.
