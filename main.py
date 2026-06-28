"""Entry point — запускает Django через gunicorn."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ad_agency_project.settings')

    # применяем миграции при старте
    from django.core.management import execute_from_command_line
    execute_from_command_line(['main.py', 'migrate', '--noinput'])
    execute_from_command_line(['main.py', 'collectstatic', '--noinput'])

    # запускаем gunicorn
    from gunicorn.app.wsgiapp import run
    sys.argv = [
        'gunicorn',
        'ad_agency_project.wsgi:application',
        '--bind', '0.0.0.0:8000',
        '--workers', '3',
    ]
    run()


if __name__ == '__main__':
    main()