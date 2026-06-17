import os
from anthropic import Anthropic
from django.conf import settings
from .models import Equipment, ChatMessage

# Manuel technique du climatiseur Daikin FTXS35K (prompt système)
TECHNICAL_MANUAL = """
MANUEL DE PANNE - CLIMATISEUR DAIKIN FTXS35K

INFORMATIONS GÉNÉRALES :
- Modèle : Daikin FTXS35K
- Type : Climatiseur split système
- Puissance : 3.5 kW (12000 BTU)
- Alimentation : 220-240V, 50Hz
- Réfrigérant : R-32

CODES D'ERREUR COURANTS :
- A1 : Erreur de communication avec la carte de commande
- A3 : Anomalie du ventilateur intérieur
- A5 : Anomalie du moteur du volet
- A6 : Anomalie du ventilateur extérieur
- C4 : Anomalie du thermistor d'évaporateur (T1)
- C5 : Anomalie du thermistor de condensation (T3)
- C9 : Anomalie du thermistor du compresseur (T6)
- E1 : Anomalie du PCB principal
- E5 : Anomalie du moteur du ventilateur
- F3 : Anomalie du système de dégivrage
- F6 : Anomalie du ventilateur extérieur (haute pression)
- H6 : Anomalie du capteur de position du moteur
- H8 : Anomalie du thermistor du liquide
- J6 : Anomalie du thermistor du tuyau d'aspiration
- J9 : Anomalie du thermistor de décharge (TS)
- L3 : Anomalie du compresseur (blocage)
- L5 : Anomalie du compresseur (surchauffe)
- L8 : Anomalie du compresseur (sous-tension)
- P1 : Anomalie du capteur de pression haute
- P3 : Anomalie du capteur de pression basse
- P4 : Anomalie du capteur de température de l'eau
- P7 : Anomalie du capteur de température de l'air
- R1 : Anomalie de la carte de communication
- R3 : Anomalie de la carte de commande
- R5 : Anomalie de la carte de puissance
- R8 : Anomalie de la carte de détection
- U0 : Anomalie de la valve électronique
- U1 : Anomalie du capteur de haute pression
- U2 : Anomalie du capteur de basse pression
- U3 : Anomalie du capteur de température extérieure
- U4 : Anomalie du capteur de température intérieure
- U5 : Anomalie du ventilateur

PROCÉDURE DE DIAGNOSTIC :
1. Vérifier l'affichage du code d'erreur sur l'unité intérieure
2. Couper l'alimentation pendant 5 minutes puis remettre sous tension
3. Vérifier si le code d'erreur persiste
4. Inspecter visuellement les connexions électriques
5. Vérifier l'état du filtre à air
6. Contrôler la pression du réfrigérant

SOLUTIONS COURANTES :
- Code A1 : Vérifier la communication entre l'unité intérieure et extérieure. Vérifier le câble de liaison.
- Code A3/A5 : Vérifier le moteur du ventilateur, nettoyer ou remplacer si nécessaire.
- Code C4/C5/C9 : Tester les thermistors avec un multimètre, remplacer si valeur hors spécification (10kΩ à 25°C).
- Code E1/E5 : Vérifier le PCB, rechercher des signes de brûlure ou de composants endommagés.
- Code F3 : Vérifier le système de dégivrage, le capteur de température.
- Code H8 : Vérifier le capteur de température du liquide.
- Code L3/L5 : Vérifier le compresseur, les condensateurs, la pression du système.
- Code P1/P3 : Vérifier les capteurs de pression, rechercher des fuites.
- Code U0/U1/U2 : Vérifier les valves électroniques et les capteurs de pression.

RECOMMANDATIONS DE SÉCURITÉ :
- Toujours couper l'alimentation avant toute intervention
- Utiliser des équipements de protection individuelle
- Ne pas intervenir si l'installation est sous garantie sans autorisation
- Si le problème persiste après les vérifications de base, contacter l'assistance technique Daikin

RAPPEL : Ce manuel est à usage informatif. Certaines interventions nécessitent des compétences techniques avancées.
"""

class ClaudeService:
    """Service pour interagir avec l'API Claude d'Anthropic"""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("La clé API Anthropic n'est pas configurée dans le fichier .env")
        
        self.client = Anthropic(api_key=self.api_key)
        self.system_prompt = TECHNICAL_MANUAL
    
    def get_equipment_context(self, equipment_id=None):
        """Récupère le contexte d'un équipement pour enrichir le prompt"""
        if not equipment_id:
            return ""
        
        try:
            equipment = Equipment.objects.get(id=equipment_id)
            context = f"""
ÉQUIPEMENT CONCERNÉ :
- Nom : {equipment.name}
- Référence : {equipment.reference}
- Type : {equipment.get_equipment_type_display()}
- Date d'installation : {equipment.installation_date}
- Description : {equipment.description}
"""
            
            # Ajouter les dernières maintenances
            latest_logs = equipment.maintenance_logs.order_by('-intervention_date')[:3]
            if latest_logs:
                context += "\nDERNIÈRES MAINTENANCES :\n"
                for log in latest_logs:
                    context += f"- {log.intervention_date.strftime('%d/%m/%Y')} : {log.get_maintenance_type_display()} - {log.status} - {log.technician_name}\n"
                    context += f"  Description : {log.description[:100]}...\n"
            
            return context
        except Equipment.DoesNotExist:
            return ""
    
    def ask_claude(self, user_message, equipment_id=None, session_id='default'):
        """Envoie un message à Claude et retourne la réponse"""
        
        # Récupérer l'historique des messages de la session
        history_messages = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')[:10]
        
        # Construire le contexte de l'équipement
        equipment_context = self.get_equipment_context(equipment_id)
        
        # Construire le message utilisateur avec contexte
        if equipment_context:
            full_user_message = f"""
{equipment_context}

QUESTION DU TECHNICIEN :
{user_message}
"""
        else:
            full_user_message = user_message
        
        # Sauvegarder le message utilisateur
        ChatMessage.objects.create(
            session_id=session_id,
            sender='USER',
            message=user_message,
            context_equipment_id=equipment_id
        )
        
        try:
            # Préparer la conversation pour l'API
            messages = []
            
            # Ajouter l'historique des messages pour le contexte
            for msg in history_messages:
                role = 'user' if msg.sender == 'USER' else 'assistant'
                messages.append({
                    'role': role,
                    'content': msg.message
                })
            
            # Ajouter le nouveau message
            messages.append({
                'role': 'user',
                'content': full_user_message
            })
            
            # Appeler l'API Claude
            response = self.client.messages.create(
                model='claude-haiku-4-5-20251001',  # remplace claude-3-5-haiku-20241022
                max_tokens=1000,
                temperature=0.7,
                system=self.system_prompt,
                messages=messages
            )
            
            # Extraire la réponse
            ai_response = response.content[0].text
            
            # Sauvegarder la réponse
            ChatMessage.objects.create(
                session_id=session_id,
                sender='AI',
                message=ai_response,
                context_equipment_id=equipment_id
            )
            
            return ai_response
            
        except Exception as e:
            error_message = f"Erreur lors de l'appel à l'API Claude : {str(e)}"
            # Sauvegarder l'erreur
            ChatMessage.objects.create(
                session_id=session_id,
                sender='AI',
                message=error_message,
                context_equipment_id=equipment_id
            )
            return error_message