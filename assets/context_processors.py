from django.core.cache import cache
from .models import Equipment, MaintenanceLog, ChatMessage

def global_stats(request):
    """
    Context processor fournissant des stats globales sur toutes les pages.
    Version optimisée avec cache et gestion d'erreurs.
    """
    # Clé de cache (valable 5 minutes)
    cache_key = 'global_stats'
    stats = cache.get(cache_key)

    if stats is None:
        try:
            # Stats équipements
            total_equipments = Equipment.objects.filter(is_active=True).count()
            total_equipments_all = Equipment.objects.count()

            # Stats maintenances
            total_maintenances = MaintenanceLog.objects.count()
            maintenance_count = MaintenanceLog.objects.filter(
                status__in=['PENDING', 'IN_PROGRESS']
            ).count()

            completed_count = MaintenanceLog.objects.filter(status='COMPLETED').count()
            in_progress_count = MaintenanceLog.objects.filter(status='IN_PROGRESS').count()
            failed_count = MaintenanceLog.objects.filter(status='FAILED').count()
            pending_count = MaintenanceLog.objects.filter(status='PENDING').count()

            # Stats par type
            ac_count = Equipment.objects.filter(equipment_type='AC', is_active=True).count()
            fr_count = Equipment.objects.filter(equipment_type='FR', is_active=True).count()
            el_count = Equipment.objects.filter(equipment_type='EL', is_active=True).count()

            # Messages chat
            chat_count = ChatMessage.objects.count()

            stats = {
                # Stats globales
                'total_equipments': total_equipments,
                'total_equipments_all': total_equipments_all,
                'total_maintenances': total_maintenances,
                'maintenance_count': maintenance_count,
                'chat_count': chat_count,

                # Stats par statut
                'completed_count': completed_count,
                'in_progress_count': in_progress_count,
                'failed_count': failed_count,
                'pending_count': pending_count,

                # Stats par type
                'ac_count': ac_count,
                'fr_count': fr_count,
                'el_count': el_count,

                # Données simulées (à remplacer plus tard par des vraies alertes)
                'alerts': [
                    {'id': 1, 'level': 'crit', 'title': 'Climatiseur Chambre 312', 'message': 'Non nettoyé depuis 7 mois — risque de panne élevé.', 'time': '2h'},
                    {'id': 2, 'level': 'crit', 'title': 'Groupe électrogène', 'message': 'Vidange moteur recommandée immédiatement.', 'time': '5h'},
                    {'id': 3, 'level': 'warn', 'title': 'Ascenseur Bât. A', 'message': 'Révision annuelle due dans 12 jours.', 'time': 'hier'},
                ],
                'planning': [
                    {'title': 'Clim. Ch.312 — Nettoyage urgent', 'day': 'Lun. 1 juin', 'tech': 'Tech. Mbarga', 'level': 'crit'},
                    {'title': 'Groupe électrogène — Vidange', 'day': 'Mar. 2 juin', 'tech': 'Tech. Essama', 'level': 'warn'},
                ],

                'health_percent': 78,
                'health_change': '+5%',
            }

            # Mettre en cache pendant 5 minutes
            cache.set(cache_key, stats, timeout=300)

        except Exception as e:
            # En cas d'erreur (DB indisponible, etc.), on retourne des valeurs par défaut
            print(f"⚠️ Erreur dans global_stats: {e}")
            stats = {
                'total_equipments': 0,
                'total_equipments_all': 0,
                'total_maintenances': 0,
                'maintenance_count': 0,
                'chat_count': 0,
                'completed_count': 0,
                'in_progress_count': 0,
                'failed_count': 0,
                'pending_count': 0,
                'ac_count': 0,
                'fr_count': 0,
                'el_count': 0,
                'alerts': [],
                'planning': [],
                'health_percent': 0,
                'health_change': '0%',
            }

    return stats