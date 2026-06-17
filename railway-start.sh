#!/bin/bash

echo "🚀 Démarrage de SmartAsset AI sur Railway"

# Création des dossiers
mkdir -p staticfiles static

echo "🔄 Application des migrations..."
python manage.py migrate --noinput || echo "⚠️  Migration skipped or failed"

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear --verbosity=2

echo "✅ Démarrage de Gunicorn..."
gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file - --access-logfile -