import os
import sys
import site

# Добавляем путь к виртуальному окружению
# (это нужно, чтобы Django работал на хостинге)

# Путь к твоему проекту
project_home = '/home/ваш_логин/adagency/'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Указываем настройки Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'ad_agency_project.settings'

# Функция для WSGI-сервера Passenger
def application(environ, start_response):
    from django.core.wsgi import get_wsgi_application
    return get_wsgi_application()(environ, start_response)