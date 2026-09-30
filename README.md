# Movies Loader

## Возможности

- Просмотр списка фильмов в виде таблицы
- Добавление фильма через HTML-форму
- Импорт фильмов из JSON-файла
- Экспорт текущего списка в JSON
- Валидация данных через MovieForm (как при ручном вводе, так и при импорте)
- Сообщения об успехе и ошибках через django.contrib.messages

## Стек

- Python 3.10+
- Django
- JSON (файловое хранилище, без базы данных)
- HTML / CSS

## Установка

### 1. Клонировать репозиторий

    git clone <url-репозитория>
    cd <папка-проекта>

### 2. Создать виртуальное окружение

Linux / macOS:

    python3 -m venv .venv
    source .venv/bin/activate

Windows (cmd):

    python -m venv .venv
    .venv\Scripts\activate

Windows (PowerShell):

    python -m venv .venv
    .venv\Scripts\Activate.ps1

После активации в начале строки терминала появится (.venv).

### 3. Установить зависимости

    pip install -r requirements.txt

Содержимое requirements.txt:

    Django>=4.2

### 4. Применить миграции

    python manage.py migrate

### 5. Запустить сервер разработки

    python manage.py runserver

Открыть в браузере: http://127.0.0.1:8000/

### Деактивация окружения

    deactivate

## Формат импорта

Файл должен быть в кодировке UTF-8 и содержать массив объектов с обязательными полями:

- title — строка
- year — целое число
- director — строка
- genre — строка
- rating — число

Лишние поля не допускаются. Каждый элемент проходит валидацию через MovieForm.

## Требования к настройкам

В settings.py должны быть подключены:

- django.contrib.messages в INSTALLED_APPS
- MessageMiddleware в MIDDLEWARE (после SessionMiddleware)
- django.contrib.messages.context_processors.messages в TEMPLATES

