#!/bin/bash

# Migrations
python manage.py makemigrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer un superutilisateur par défaut (optionnel)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Démarrer le serveur avec gunicorn
gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT