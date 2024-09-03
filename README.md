# coursework_6_django

Сервис рассылок

Настройте проект в соответствии с файлом: .env.sample

Команды
Создание суперпользователя (почта: admin@example.ru, пароль: 123456):
python manage.py csu

Наполнение сервиса рассылок:  python manage.py loaddata mailing.json

Наполнение блога статьями: python manage.py blog_fill

Наполнение пользователями: python manage.py loaddata users.json

Добавление групп  с правами доступа: python manage.py add_groups
