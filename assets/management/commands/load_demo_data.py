from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from assets.models import Equipment, MaintenanceLog, ChatMessage

class Command(BaseCommand):
    help = 'Charge des données de démonstration pour SmartAsset AI'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des données de démonstration...')

        # 1. Créer des équipements
        equipments_data = [
            {
                'name': 'Climatiseur Daikin FTXS35K',
                'reference': 'FTXS35K-001',
                'equipment_type': 'AC',
                'installation_date': datetime.now().date() - timedelta(days=180),
                'description': 'Climatiseur split Daikin FTXS35K - 3.5kW - R32 - Installation au salon'
            },
            {
                'name': 'Climatiseur Daikin FTXS25K',
                'reference': 'FTXS25K-002',
                'equipment_type': 'AC',
                'installation_date': datetime.now().date() - timedelta(days=120),
                'description': 'Climatiseur split Daikin FTXS25K - 2.5kW - R32 - Installation dans la chambre principale'
            },
            {
                'name': 'Réfrigérateur Samsung RB34',
                'reference': 'SAMS-RB34-001',
                'equipment_type': 'FR',
                'installation_date': datetime.now().date() - timedelta(days=365),
                'description': 'Réfrigérateur Samsung RB34 - 340L - Classe A++'
            },
            {
                'name': 'Groupe électrogène Caterpillar',
                'reference': 'CAT-200KVA-001',
                'equipment_type': 'EL',
                'installation_date': datetime.now().date() - timedelta(days=90),
                'description': 'Groupe électrogène Caterpillar 200KVA - Installation technique'
            },
        ]

        created_equipments = []
        for data in equipments_data:
            equipment, created = Equipment.objects.get_or_create(
                reference=data['reference'],
                defaults={
                    'name': data['name'],
                    'equipment_type': data['equipment_type'],
                    'installation_date': data['installation_date'],
                    'description': data['description'],
                    'is_active': True
                }
            )
            created_equipments.append(equipment)
            if created:
                self.stdout.write(f'✅ Équipement créé : {equipment.name}')
            else:
                self.stdout.write(f'ℹ️ Équipement existe déjà : {equipment.name}')

        # 2. Créer des logs de maintenance
        maintenance_logs_data = [
            {
                'equipment': created_equipments[0],  # Daikin FTXS35K
                'maintenance_type': 'PREVENTIVE',
                'status': 'COMPLETED',
                'description': 'Nettoyage complet du filtre à air et vérification du système de refroidissement',
                'technician_name': 'Jean-Pierre M.',
                'intervention_date': datetime.now() - timedelta(days=45),
                'duration_hours': 2.0,
                'parts_used': 'Filtre à air neuf',
                'notes': 'Système en bon état général'
            },
            {
                'equipment': created_equipments[0],  # Daikin FTXS35K
                'maintenance_type': 'CORRECTIVE',
                'status': 'COMPLETED',
                'description': 'Intervention sur code erreur C4 - Remplacement du thermistor d\'évaporateur',
                'technician_name': 'Marie L.',
                'intervention_date': datetime.now() - timedelta(days=15),
                'duration_hours': 1.5,
                'parts_used': 'Thermistor 10kΩ - Réf. DAIKIN-001',
                'notes': 'Problème résolu, température stabilisée'
            },
            {
                'equipment': created_equipments[1],  # Daikin FTXS25K
                'maintenance_type': 'URGENT',
                'status': 'IN_PROGRESS',
                'description': 'Climatiseur ne refroidit plus - Vérification du compresseur',
                'technician_name': 'Paul K.',
                'intervention_date': datetime.now() - timedelta(days=2),
                'duration_hours': 1.0,
                'parts_used': 'En attente de diagnostic',
                'notes': 'Intervention en cours - Attente pièces de rechange'
            },
            {
                'equipment': created_equipments[2],  # Samsung RB34
                'maintenance_type': 'PREVENTIVE',
                'status': 'COMPLETED',
                'description': 'Nettoyage des serpentins et vérification du système de dégivrage',
                'technician_name': 'Jean-Pierre M.',
                'intervention_date': datetime.now() - timedelta(days=60),
                'duration_hours': 1.5,
                'parts_used': 'Aucune',
                'notes': 'Réfrigérateur en parfait état'
            },
        ]

        for data in maintenance_logs_data:
            log, created = MaintenanceLog.objects.get_or_create(
                equipment=data['equipment'],
                description=data['description'][:50],
                defaults=data
            )
            if created:
                self.stdout.write(f'✅ Maintenance créée : {log.equipment.name} - {log.get_maintenance_type_display()}')
            else:
                self.stdout.write(f'ℹ️ Maintenance existe déjà')

        # 3. Créer des messages de chat de démonstration
        demo_messages = [
            {
                'session_id': 'demo_session_1',
                'sender': 'USER',
                'message': 'Bonjour, j\'ai un code d\'erreur A1 sur mon Daikin FTXS35K, que dois-je faire ?',
                'context_equipment': created_equipments[0]
            },
            {
                'session_id': 'demo_session_1',
                'sender': 'AI',
                'message': 'Le code A1 indique une erreur de communication entre la carte de commande interne et externe.\n\nProcédure recommandée :\n1. Vérifiez les câbles de liaison entre l\'unité intérieure et extérieure\n2. Assurez-vous que les connexions sont bien serrées\n3. Vérifiez l\'absence de coupure ou de dommage sur le câble\n4. Si tout est OK, essayez de couper l\'alimentation pendant 5 minutes puis de remettre en marche\n\nSi le problème persiste, contactez l\'assistance technique Daikin.',
                'context_equipment': created_equipments[0]
            },
            {
                'session_id': 'demo_session_2',
                'sender': 'USER',
                'message': 'Mon climatiseur ne refroidit plus, il fait 30°C dans la chambre.',
                'context_equipment': created_equipments[1]
            },
            {
                'session_id': 'demo_session_2',
                'sender': 'AI',
                'message': 'Si votre climatiseur ne refroidit pas, voici les vérifications à faire :\n\n1. Vérifiez les filtres à air - ils doivent être propres\n2. Vérifiez que la température programmée est inférieure à la température ambiante\n3. Vérifiez que l\'unité extérieure n\'est pas obstruée\n4. Écoutez si le compresseur se déclenche (un bruit caractéristique)\n\nSi tout semble normal, vérifiez les codes d\'erreur sur l\'affichage. Si le compresseur ne démarre pas, cela peut indiquer un problème de thermistor ou de carte de commande.',
                'context_equipment': created_equipments[1]
            },
        ]

        for data in demo_messages:
            msg, created = ChatMessage.objects.get_or_create(
                session_id=data['session_id'],
                sender=data['sender'],
                message=data['message'][:50],
                defaults=data
            )
            if created:
                self.stdout.write(f'✅ Message de chat créé')
            else:
                self.stdout.write(f'ℹ️ Message de chat existe déjà')

        self.stdout.write(self.style.SUCCESS('✅ Données de démonstration chargées avec succès !'))

        # Afficher un résumé
        self.stdout.write('\n📊 RÉSUMÉ :')
        self.stdout.write(f'  - Équipements : {Equipment.objects.count()}')
        self.stdout.write(f'  - Maintenances : {MaintenanceLog.objects.count()}')
        self.stdout.write(f'  - Messages de chat : {ChatMessage.objects.count()}')