#!/bin/bash
echo "🚀 Démarrage SmartAsset AI sur Railway"

mkdir -p staticfiles static

echo "🔄 Migrations..."
python manage.py migrate --noinput || echo "⚠️ Migration warning"

echo "📁 Collectstatic..."
python manage.py collectstatic --noinput --clear || echo "⚠️ Collectstatic warning"

echo "✅ Tout est prêt - Lancement Gunicorn"
exec gunicorn smartasset_ai.wsgi:application --bind 0.0.0.0:$PORT --log-file - --access-logfile -