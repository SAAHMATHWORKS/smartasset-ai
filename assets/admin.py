from django.contrib import admin
from .models import Equipment, MaintenanceLog, ChatMessage

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'equipment_type', 'is_active', 'installation_date')
    list_filter = ('equipment_type', 'is_active')
    search_fields = ('name', 'reference', 'description')
    ordering = ('-created_at',)

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'maintenance_type', 'status', 'technician_name', 'intervention_date')
    list_filter = ('maintenance_type', 'status')
    search_fields = ('equipment__name', 'technician_name', 'description')
    ordering = ('-intervention_date',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message_preview', 'context_equipment', 'created_at')
    list_filter = ('sender', 'session_id')
    ordering = ('-created_at',)
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Aperçu du message'