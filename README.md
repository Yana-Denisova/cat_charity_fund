# QRKot - приложение для Благотворительного фонда

## Возможности проекта QRKot

- Создание благотворительных проектов
- Внесение пожертвований пользователями
- Автоматическое поступление пожертвований в открытые проекты
- Регистрация пользователей на основе FastAPI Users

## Технологии

<p align="left"> 
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"> </a>
<a href="https://www.sqlalchemy.org/" target="_blank" rel="noreferrer"> <img src="https://github.com/devicons/devicon/blob/master/icons/sqlalchemy/sqlalchemy-original.svg" alt="sqlalchemy" width="40" height="40"> </a>
<a href="https://fastapi.tiangolo.com/" target="_blank" rel="noreferrer"><img src="https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original.svg" alt="fastapi" width="40" height="40"> </a>
<a href="https://github.com/sqlalchemy/alembic" target="_blank" rel="noreferrer"><img src="https://github.com/awkward/Alembic/blob/master/Docs/icon.png" alt="alembic" width="40" height="40"> </a>
<a href="https://github.com/fastapi-users/fastapi-users" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/fastapi-users/fastapi-users/master/logo.svg" alt="fastapi-users" width="120" height="40"> </a>
</p>

## Установка и запуск проекта

- В корневой папке создайте файл *.env* и добавьте в него свои данные (при необходимости):

```
APP_TITLE=         # Название приложения
APP_DESCRIPTION=   # Описание приложения
DATABASE_URL=      # Путь подключения к БД
```
- Установите зависимости

- Создайте миграции

```shell
alembic revision --autogenerate -m "First migration" 
```

- Установите миграции

```shell
alembic upgrade head
```

- Запустите проект

```shell
uvicorn main:app  --reload
```

## Документация проекта

После запуска проекта откройте одну из ссылкок в браузере:

```shell
http://127.0.0.1:8000/docs
```

```shell
http://127.0.0.1:8000/redoc
```

## Автор проекта:

- [GitHub](https://github.com/Yana-Denisova/)
