from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    # Page d'accueil
    path('', views.index, name='index'),
    
    # Gestion des équipements
    path('equipments/', views.equipment_list, name='equipment_list'),
    path('equipments/add/', views.equipment_add, name='equipment_add'),
    path('equipments/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),
    
    # Gestion des maintenances
    path('maintenances/', views.maintenance_list, name='maintenance_list'),
    # Gestion des maintenances
    path('maintenances/<int:maintenance_id>/update-status/', views.update_maintenance_status, name='update_maintenance_status'),
    path('equipments/<int:equipment_id>/maintenance/add/', views.maintenance_add, name='maintenance_add'),
    
    # Chat avec l'IA
    path('chat/', views.chat_view, name='chat_view'),
    path('chat/<int:equipment_id>/', views.chat_view, name='chat_view_equipment'),
    path('api/chat/', views.chat_api, name='chat_api'),

    # Gestion des maintenances
    path('maintenances/<int:maintenance_id>/update-status/', views.update_maintenance_status, name='update_maintenance_status'),
    
    # Test
    path('test/', views.test_view, name='test_view'),
]