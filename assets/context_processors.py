from .models import Equipment, MaintenanceLog, ChatMessage

def global_stats(request):
    """
    Context processor qui fournit des statistiques globales
    disponibles sur toutes les pages du site.
    """
    # Compter les équipements actifs
    total_equipments = Equipment.objects.filter(is_active=True).count()
    total_equipments_all = Equipment.objects.count()
    
    # Compter les maintenances
    total_maintenances = MaintenanceLog.objects.count()
    
    # Compter par statut pour le badge
    maintenance_count = MaintenanceLog.objects.filter(
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    
    # Compter les messages de chat
    chat_count = ChatMessage.objects.count()
    
    # Compter les maintenances par statut (pour le dashboard)
    completed_count = MaintenanceLog.objects.filter(status='COMPLETED').count()
    in_progress_count = MaintenanceLog.objects.filter(status='IN_PROGRESS').count()
    failed_count = MaintenanceLog.objects.filter(status='FAILED').count()
    pending_count = MaintenanceLog.objects.filter(status='PENDING').count()
    
    # Compter les équipements par type
    ac_count = Equipment.objects.filter(equipment_type='AC', is_active=True).count()
    fr_count = Equipment.objects.filter(equipment_type='FR', is_active=True).count()
    el_count = Equipment.objects.filter(equipment_type='EL', is_active=True).count()
    
    # Dernières alertes (simulées pour le moment)
    # Tu pourras plus tard les remplacer par de vraies alertes
    alerts = [
        {
            'id': 1,
            'level': 'crit',
            'title': 'Climatiseur Chambre 312',
            'message': 'Non nettoyé depuis 7 mois — risque de panne élevé.',
            'time': '2h'
        },
        {
            'id': 2,
            'level': 'crit',
            'title': 'Groupe électrogène',
            'message': 'Vidange moteur recommandée immédiatement.',
            'time': '5h'
        },
        {
            'id': 3,
            'level': 'warn',
            'title': 'Ascenseur Bât. A',
            'message': 'Révision annuelle due dans 12 jours.',
            'time': 'hier'
        },
        {
            'id': 4,
            'level': 'warn',
            'title': 'Clim. Salle Conférence',
            'message': 'Filtre encrassé — baisse de 18% de performance.',
            'time': 'hier'
        },
        {
            'id': 5,
            'level': 'info',
            'title': 'Caméra — Parking',
            'message': 'Mise à jour firmware disponible.',
            'time': '2j'
        },
    ]
    
    # Planning de la semaine
    planning = [
        {
            'title': 'Clim. Ch.312 — Nettoyage urgent',
            'day': 'Lun. 1 juin',
            'tech': 'Tech. Mbarga',
            'level': 'crit'
        },
        {
            'title': 'Groupe électrogène — Vidange',
            'day': 'Mar. 2 juin',
            'tech': 'Tech. Essama',
            'level': 'warn'
        },
        {
            'title': 'Ascenseur — Contrôle annuel',
            'day': 'Jeu. 4 juin',
            'tech': 'Prestataire',
            'level': 'info'
        },
        {
            'title': 'Caméras — Mise à jour',
            'day': 'Ven. 5 juin',
            'tech': 'Tech. Mbarga',
            'level': 'ok'
        },
    ]
    
    return {
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
        
        # Stats par type d'équipement
        'ac_count': ac_count,
        'fr_count': fr_count,
        'el_count': el_count,
        
        # Alertes et planning
        'alerts': alerts,
        'planning': planning,
        
        # Pourcentage de santé du parc (simulé)
        'health_percent': 78,
        'health_change': '+5%',
    }