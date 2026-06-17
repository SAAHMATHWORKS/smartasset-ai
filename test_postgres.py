import os
import psycopg2
from dotenv import load_dotenv

# Charger .env.local
load_dotenv('.env.local')

# Récupérer l'URL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL non trouvé")
    print("Vérifie que .env.local existe et contient DATABASE_URL")
    exit(1)

print(f"🔗 Connexion à PostgreSQL...")

try:
    # Se connecter avec SSL
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    print("✅ Connexion réussie !")
    
    # Afficher les infos
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"📦 PostgreSQL: {version[:60]}...")
    
    cursor.execute("SELECT current_database();")
    db_name = cursor.fetchone()[0]
    print(f"📁 Base de données: {db_name}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")