#!/bin/bash

echo "🚀 Démarrage de SmartAsset AI sur Railway"

# Créer les dossiers nécessaires
mkdir -p static
mkdir -p staticfiles

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt

# Migrations
echo "🔄 Application des migrations..."
python manage.py makemigrations
python manage.py migrate

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superutilisateur par défaut (optionnel)
echo "👤 Création du superutilisateur..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Démarrer le serveur
echo "✅ Démarrage du serveur sur le port $PORT"
gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT
