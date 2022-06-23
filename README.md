# Тестовое задание

Использовался Linux

Должен быть установлен Redis (запускалось на версии 5.0.7)

Ссылка на Google Sheet https://docs.google.com/spreadsheets/d/1UDh6xIR9k_Dt6dKpdnqY7hZ7YQe6zD0Dmv9-s9gHJyg/

Для установки нужных пакетов в систему
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
```
____
Создадим пользователя для postgres
```
sudo -u postgres psql

postgres=# CREATE USER username WITH PASSWORD 'pass';
postgres=# ALTER ROLE username SET client_encoding TO 'utf8';
postgres=# ALTER ROLE username SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE username SET timezone TO 'Europe/Moscow';
postgres=# GRANT ALL PRIVILEGES ON DATABASE test_task_numbers_DB TO username;
postgres=# \q

createdb test_task_numbers_DB
```
В settings.py нужно прописать пароль от созданного пользователя
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_task_numbers_DB',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}
```
___
Активируем виртуальное окружение, установим пакеты
```
python3 -m venv venv
pip3 install -r requirements.txt 
```
```
python3 manage.py makemigrations
python3 manage.py migrate
```
___
В папке /static следует добавить credentials.json с ключами для работы с Google Sheets Api. Доступ был предоставлен почте sales@numbersss.com
___
Запускаем в разные процессы:
```
python3 manage.py runserver
```
```
celery -A djangoProject beat -l info
```
```
celery -A djangoProject worker -l INFO
```
