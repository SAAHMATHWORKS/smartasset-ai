#!/bin/bash

echo "🚀 === DÉMARRAGE SMARTASSET AI SUR RAILWAY ==="

# Création des dossiers
mkdir -p staticfiles static
echo "✅ Dossiers créés"

# Migrations
echo "🔄 Application des migrations..."
python manage.py migrate --noinput || echo "⚠️ Migration a rencontré un problème"

# Collectstatic (avec plus de visibilité)
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear --verbosity=1 || echo "⚠️ Collectstatic a rencontré un problème"

echo "✅ Collectstatic terminé"
ls -la staticfiles/ || echo "Dossier staticfiles vide ou inexistant"

# Démarrage Gunicorn
echo "🚀 Lancement de Gunicorn sur le port $PORT..."
gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file - --access-logfile -