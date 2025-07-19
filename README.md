# Telegram-бот для блога с API-админкой

Telegram-бот и API админка на FastAPI

## Как запустить проект

Скачать удаленный репозиторий выполнив команду

```
git clone https://github.com/AlekseiTolchin/tg_blog_api_admin
```

Python3.11 должен быть уже установлен. Затем используйте `pip `
(или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

В корневой директории проекта создать файл `src.env` со следующими настройками:

- `API_URL` - задано значение по умолчанию `http://localhost:8000/api/posts/`
- `DATABASE_URL` - задано значение по умолчанию `sqlite+aiosqlite:///posts.db`
- `SYNC_DATABASE_URL` - задано значение по умолчанию `sqlite:///posts.db` (для alembic миграций)

В корневой директории проекта создать файл `bot.env` со следующими настройками:

- `API_URL` - задано значение по умолчанию `http://localhost:8000/api/posts/`
- `TG_BOT_TOKEN` - токен Telegram-бота (получить у BotFather)

- Применить миграции:

```
alembic upgrade head
```

Из корневой директории проекта выполнить команду для запуска сервиса:

```
uvicorn src.main:app --reload
```

Открыть второй терминал и также из корневой директории проекта выполнить команду для запуска бота:

```
python -m bot.run
```

## Запуск с помощью Docker-Compose

Обязательно в `src.env` прописать:

- `API_URL` - `http://api:8000/api/posts/`

Так как имя у сервиса в сети Docker - `api`

Выполнить команды:

```
docker compose build
```

```
docker compose up
```

Ссылка для тестирования API:

http://127.0.0.1:8000/docs/ - `документация API` 
