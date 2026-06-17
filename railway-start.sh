#!/bin/bash
echo "🚀 === DÉMARRAGE SMARTASSET AI SUR RAILWAY ==="

# === DIAGNOSTIC TRÈS DÉTAILLÉ ===
echo "📊 DIAGNOSTIC DATABASE..."
python -c "
import os
print('=== ENVIRONNEMENT ===')
print('DATABASE_URL présente ?', bool(os.getenv('DATABASE_URL')))
print('DATABASE_URL =', os.getenv('DATABASE_URL')[:100] + '...' if os.getenv('DATABASE_URL') else 'NON DÉFINIE')
print('DJANGO_SETTINGS_MODULE =', os.getenv('DJANGO_SETTINGS_MODULE'))
print('========================')
"

# Forcer le chargement des settings Django
echo "🔄 Chargement des settings Django..."
python manage.py migrate --noinput --verbosity=0 || echo "Migration terminée ou ignorée"

echo "📁 Collectstatic..."
python manage.py collectstatic --noinput --clear --verbosity=0

# Démarrage
PORT=${PORT:-8080}
echo "🚀 Démarrage Gunicorn sur port $PORT"
exec gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file - --access-logfile -