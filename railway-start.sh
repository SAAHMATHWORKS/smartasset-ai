#!/bin/bash
echo "🚀 === DÉMARRAGE SMARTASSET AI SUR RAILWAY ==="

echo "📊 BASE UTILISÉE :"
python -c "
import os, dj_database_url
from django.conf import settings
print('DATABASE_URL présente ?', bool(os.getenv('DATABASE_URL')))
print('Engine utilisé :', settings.DATABASES['default']['ENGINE'])
"

mkdir -p staticfiles static

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file -