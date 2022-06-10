release: python manage.py migrate
web: gunicorn planeks_fakecsv.wsgi
worker: celery -A planeks_fakecsv worker