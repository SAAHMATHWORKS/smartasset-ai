#!/bin/bash
echo "🚀 === DÉMARRAGE SMARTASSET AI SUR RAILWAY ==="

mkdir -p staticfiles static

echo "🔍 DIAGNOSTIC DATABASE..."
python -c "
import os
print('DATABASE_URL présente ?', bool(os.getenv('DATABASE_URL')))
if os.getenv('DATABASE_URL'):
    print('DATABASE_URL commence par :', os.getenv('DATABASE_URL')[:60] + '...')
else:
    print('DATABASE_URL = NON DÉFINIE')
"

# Force l'utilisation de PostgreSQL si la variable existe
echo "🔄 Application des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "🚀 Lancement Gunicorn..."
exec gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:\$PORT --log-file - --access-logfile -