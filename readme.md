# Тестовый DRF проект

Описание:

- ДБ - postgres
- OpenAPI - swagger
- docker
- Для разнообразия авторизация не дефолтный через username, а через email.

Чтобы запустить проект, запускаете

```bash
docker-compose up
```

### Если не хотите докера, то --->>

## Установка

1. Создайте и активируйте виртуальное окружение (рекомендуется):

```bash
python -m venv venv
source venv/bin/activate
```

2. Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

3. Настройте подключение к базе данных PostgreSQL в файле settings.py:

```
DATABASES = PSQL_CONF 
```

или

```
DATABASES = SQLITE_CONF
```

<h6> (Есть sqlite3 файл c тестовыми данными. Логин, пароль: i, string)</h6>

5. Примените миграции для создания таблиц в базе данных:

```
python manage.py migrate
```

6. Запустите сервер:

```
python manage.py runserver
```

Теперь вы можете перейти по адресу http://127.0.0.1:8000/docs/ в веб-браузере и
увидеть интерактивную документацию Swagger для API.
