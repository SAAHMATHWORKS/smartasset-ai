from django.db import models
from django.utils import timezone

class Equipment(models.Model):
    """Modèle représentant un équipement technique"""
    
    EQUIPMENT_TYPES = [
        ('AC', 'Climatiseur'),
        ('FR', 'Réfrigérateur'),
        ('EL', 'Équipement électrique'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom")
    reference = models.CharField(max_length=100, verbose_name="Référence", unique=True)
    equipment_type = models.CharField(max_length=2, choices=EQUIPMENT_TYPES, default='AC', verbose_name="Type")
    installation_date = models.DateField(verbose_name="Date d'installation")
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.reference})"
    
    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"
        ordering = ['-created_at']


class MaintenanceLog(models.Model):
    """Modèle représentant un historique de maintenance"""
    
    MAINTENANCE_TYPES = [
        ('PREVENTIVE', 'Maintenance préventive'),
        ('CORRECTIVE', 'Maintenance corrective'),
        ('URGENT', 'Intervention urgente'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('IN_PROGRESS', 'En cours'),
        ('COMPLETED', 'Terminé'),
        ('FAILED', 'Échec'),
    ]
    
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_logs', verbose_name="Équipement")
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES, default='PREVENTIVE', verbose_name="Type")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Statut")
    description = models.TextField(verbose_name="Description de l'intervention")
    technician_name = models.CharField(max_length=100, verbose_name="Nom du technicien")
    intervention_date = models.DateTimeField(default=timezone.now, verbose_name="Date d'intervention")
    duration_hours = models.FloatField(default=1.0, verbose_name="Durée (heures)")
    parts_used = models.TextField(blank=True, verbose_name="Pièces utilisées")
    notes = models.TextField(blank=True, verbose_name="Notes supplémentaires")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.equipment.name} - {self.get_maintenance_type_display()} - {self.intervention_date.strftime('%Y-%m-%d')}"
    
    class Meta:
        verbose_name = "Journal de maintenance"
        verbose_name_plural = "Journaux de maintenance"
        ordering = ['-intervention_date']


class ChatMessage(models.Model):
    """Modèle représentant un message échangé avec l'IA"""
    
    SENDER_CHOICES = [
        ('USER', 'Technicien'),
        ('AI', 'Assistant IA'),
    ]
    
    session_id = models.CharField(max_length=100, default='default', verbose_name="ID de session")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Expéditeur")
    message = models.TextField(verbose_name="Message")
    context_equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Équipement concerné", related_name='chat_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_sender_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "Message de chat"
        verbose_name_plural = "Messages de chat"
        ordering = ['created_at']