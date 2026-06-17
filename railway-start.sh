#!/bin/bash
echo "🚀 === DÉMARRAGE SMARTASSET AI SUR RAILWAY ==="

# Diagnostic base de données
echo "📊 DIAGNOSTIC BASE DE DONNÉES :"
python -c "
import os
print('DATABASE_URL présente ?', bool(os.getenv('DATABASE_URL')))
if os.getenv('DATABASE_URL'):
    print('DATABASE_URL commence par :', os.getenv('DATABASE_URL')[:70] + '...')
else:
    print('⚠️  DATABASE_URL NON DÉFINIE → Utilisation de SQLite (données perdues à chaque déploiement)')
"

# Création des dossiers
mkdir -p staticfiles static

# Migrations
echo "🔄 Application des migrations..."
python manage.py migrate --noinput

# Collectstatic
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Démarrage Gunicorn avec gestion du PORT
PORT=${PORT:-8080}
echo "🚀 Démarrage de Gunicorn sur le port : $PORT"
exec gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file - --access-logfile -