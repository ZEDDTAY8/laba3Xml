# Sales XML App

Django-приложение для работы с данными о продажах в XML.

## Установка
1. Клонируйте репо: `git clone https://github.com/ZEDDTAY8/laba3Xml`
2. Создайте venv: `python -m venv venv`
3. Активируйте: `venv\Scripts\activate` (Windows) или `source venv/bin/activate` (Linux)
4. Установите зависимости: `pip install -r requirements.txt`
5. Создайте папку для файлов: `mkdir media\xml_files`
6. Запустите: `python manage.py runserver`

## Функционал
- Ввод данных о продажах через форму с валидацией.
- Сохранение в XML-файл.
- Загрузка XML-файлов с валидацией и удалением невалидных.
- Отображение содержимого всех XML-файлов из папки media/xml_files.
- Сообщение, если файлов нет.
