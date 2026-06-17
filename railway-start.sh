#!/bin/bash
echo "🚀 === DÉMARRAGE SMARTASSET AI SUR RAILWAY ==="

# === DIAGNOSTIC BASE DE DONNÉES ===
echo "🔍 DIAGNOSTIC DATABASE..."
python -c "
import os
from django.conf import settings
print('DATABASE_URL présente ?', 'DATABASE_URL' in os.environ)
print('Engine utilisé :', settings.DATABASES['default']['ENGINE'])
print('Nom de la DB :', settings.DATABASES['default'].get('NAME', 'Non défini'))
" 2>&1 || echo "Erreur lors du diagnostic DB"

echo "🔄 Application des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "✅ Lancement de Gunicorn..."
exec gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:\$PORT --log-file - --access-logfile -