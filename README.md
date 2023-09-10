# Task Manager

- Предоставляет базовые CRUD операции(Создание, чтение, обновление, удаление) для тасков
- Включает real-time(WebSocket) обновления для статуса тасков.

## Features

- Регистрация/Логин юзера.
- Получение информации о себе.

- CRUD операции для тасков - Create, Read, Update, Delete.
- Получение всех тасков.
- Используется OAuth2 authentication для доступа к API.
- Используется Middleware для логирования запросов к серверу.

## Запуск приложения
Для запуска FastAPI используется веб-сервер uvicorn. Команда для запуска выглядит так:  
```
uvicorn main:app --reload
```

### Документация
```
- http://IP/docs#/
```

### Стек
```
Python 3.8, FastApi, PostgreSQL, Sqlalchemy, Alembic, WebSocket, Middleware
```
