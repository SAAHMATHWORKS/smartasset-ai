#!/bin/bash

echo "🚀 === DÉMARRAGE SMARTASSET AI SUR RAILWAY ==="

# Création des dossiers
mkdir -p staticfiles static
echo "✅ Dossiers créés"

# Migrations
echo "🔄 Application des migrations..."
python manage.py migrate --noinput || echo "⚠️ Problème lors des migrations"

# Collect static
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear --verbosity=1 || echo "⚠️ Problème lors de collectstatic"

echo "✅ Collectstatic terminé"
ls -la staticfiles/ 2>/dev/null || echo "Dossier staticfiles vide"

# Lancement du serveur
echo "🚀 Démarrage de Gunicorn..."
gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file - --access-logfile -