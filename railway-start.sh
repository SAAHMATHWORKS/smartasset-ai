#!/bin/bash

echo "🔧 Installation des dépendances..."
pip install -r requirements.txt

echo "🔧 Migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🔧 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Démarrage du serveur..."
gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT