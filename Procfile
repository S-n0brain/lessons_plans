release: python manage.py makemigrations && python manage.py migrate
web: gunicorn lessons.wsgi:application --bind 0.0.0.0:$PORT
