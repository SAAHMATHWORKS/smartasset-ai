#!/bin/bash

echo "🚀 Démarrage de SmartAsset AI sur Railway"

# Créer les dossiers nécessaires
mkdir -p staticfiles

# Appliquer les migrations
echo "🔄 Application des migrations..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Démarrage du serveur Gunicorn
echo "✅ Démarrage du serveur sur le port $PORT"
gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file -