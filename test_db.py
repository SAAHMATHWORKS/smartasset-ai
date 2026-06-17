from dotenv import load_dotenv
import os

# Essayer de charger .env.local
env_file = '.env.local'
if os.path.exists(env_file):
    load_dotenv(env_file)
    print(f"✅ Fichier {env_file} chargé")
else:
    print(f"❌ Fichier {env_file} non trouvé")

# Afficher les variables
db_url = os.getenv('DATABASE_URL')
print(f"DATABASE_URL: {db_url}")

if db_url:
    print("✅ DATABASE_URL trouvé !")
else:
    print("❌ DATABASE_URL non trouvé")