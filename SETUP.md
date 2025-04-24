# Установка и настройка проекта Bubble

## Необходимые компоненты:
- Python 3.8 или выше
- Pip (менеджер пакетов Python)
- Виртуальное окружение (рекомендуется)

## Шаги установки:

### 1. Клонирование репозитория (если используется Git):
```bash
git clone <url-репозитория>
cd bubble
```

### 2. Создание виртуального окружения:
```bash
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux/macOS:
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей:
```bash
pip install -r requirements.txt
```

### 4. Применение миграций базы данных:
```bash
python manage.py makemigrations accounts
python manage.py makemigrations chemistry
python manage.py migrate
```

### 5. Создание суперпользователя (администратора):
```bash
python manage.py createsuperuser
```

### 6. Сбор статических файлов:
```bash
python manage.py collectstatic
```

### 7. Запуск сервера для разработки:
```bash
python manage.py runserver
```

После этого сайт будет доступен по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Наполнение базы данных

1. Войдите в административную панель, используя созданные учетные данные суперпользователя: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

2. Добавьте категории химических элементов через раздел "ElementCategory"

3. Добавьте химические элементы в таблицу через раздел "Element"

4. Добавьте дополнительную информацию о каждом элементе через раздел "ElementDetail"

5. Создайте химические реакции между элементами через раздел "ChemicalReaction"

6. Подготовьте викторины и тесты через раздел "Quiz"

## Локализация

Для генерации файлов переводов:

```bash
# Создание файлов для перевода
python manage.py makemessages -l ru

# Компиляция переводов
python manage.py compilemessages
```

## Развертывание на сервере

Для развертывания на production-сервере рекомендуется:

1. Изменить настройки в `bubble/settings.py`:
   - Установить `DEBUG = False`
   - Настроить `ALLOWED_HOSTS`
   - Настроить базу данных (например, PostgreSQL)
   - Настроить статические файлы и медиа-файлы

2. Использовать WSGI-сервер, например, Gunicorn:
```bash
gunicorn bubble.wsgi:application
```

3. Настроить веб-сервер (Nginx или Apache) в качестве прокси перед Gunicorn

4. Настроить SSL-сертификат для безопасного соединения

## Резервное копирование данных

Для создания резервной копии базы данных:

```bash
python manage.py dumpdata > backup.json
```

Для восстановления базы данных из резервной копии:

```bash
python manage.py loaddata backup.json
``` 