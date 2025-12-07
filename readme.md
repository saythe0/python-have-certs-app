```bash
# Клонировать репозиторий
git clone https://github.com/saythe0/python-have-certs-app.git korochki_site
cd korochki_site

# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```