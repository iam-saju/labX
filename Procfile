web: mkdir -p staticfiles && python manage.py collectstatic --noinput && DJANGO_SETTINGS_MODULE=backend.settings gunicorn backend.wsgi:application
