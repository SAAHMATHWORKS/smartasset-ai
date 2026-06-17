from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import Equipment, MaintenanceLog, ChatMessage
from .services import ClaudeService

# Vue pour la page d'accueil
def index(request):
    """Page d'accueil avec le dashboard"""
    equipments = Equipment.objects.filter(is_active=True).order_by('-created_at')
    total_maintenances = MaintenanceLog.objects.count()
    
    context = {
        'equipments': equipments,
        'total_equipments': equipments.count(),
        'total_maintenances': total_maintenances,
        'maintenance_count': total_maintenances,  # Pour le badge
    }
    return render(request, 'assets/index.html', context)

# Vue pour la liste des équipements
def equipment_list(request):
    """Liste de tous les équipements"""
    equipments = Equipment.objects.all().order_by('-created_at')
    return render(request, 'assets/equipment_list.html', {'equipments': equipments})

# Vue pour les détails d'un équipement
def equipment_detail(request, equipment_id):
    """Détails d'un équipement avec son historique de maintenance"""
    equipment = get_object_or_404(Equipment, id=equipment_id)
    maintenance_logs = equipment.maintenance_logs.all().order_by('-intervention_date')
    chat_messages = ChatMessage.objects.filter(context_equipment=equipment).order_by('created_at')[:20]
    
    context = {
        'equipment': equipment,
        'maintenance_logs': maintenance_logs,
        'chat_messages': chat_messages,
    }
    return render(request, 'assets/equipment_detail.html', context)

# Vue pour le chat avec l'IA
def chat_view(request, equipment_id=None):
    """Page de chat avec l'assistant IA"""
    equipment = None
    if equipment_id:
        equipment = get_object_or_404(Equipment, id=equipment_id)
    
    # Récupérer l'historique du chat pour cet équipement
    if equipment:
        chat_messages = ChatMessage.objects.filter(
            context_equipment=equipment
        ).order_by('created_at')[:50]
    else:
        chat_messages = ChatMessage.objects.filter(
            context_equipment__isnull=True
        ).order_by('created_at')[:50]
    
    context = {
        'equipment': equipment,
        'chat_messages': chat_messages,
        'equipments': Equipment.objects.filter(is_active=True),
    }
    return render(request, 'assets/chat.html', context)

# API endpoint pour envoyer un message au chat
@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """Endpoint API pour envoyer un message et recevoir une réponse de Claude"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        equipment_id = data.get('equipment_id')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return JsonResponse({'error': 'Le message ne peut pas être vide'}, status=400)
        
        # Vérifier si l'équipement existe
        if equipment_id:
            try:
                equipment = Equipment.objects.get(id=equipment_id)
            except Equipment.DoesNotExist:
                return JsonResponse({'error': 'Équipement non trouvé'}, status=404)
        
        # Appeler le service Claude
        claude_service = ClaudeService()
        ai_response = claude_service.ask_claude(
            user_message=user_message,
            equipment_id=equipment_id,
            session_id=session_id
        )
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'session_id': session_id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Format JSON invalide'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Vue pour ajouter un équipement
def equipment_add(request):
    """Ajouter un nouvel équipement"""
    if request.method == 'POST':
        name = request.POST.get('name')
        reference = request.POST.get('reference')
        equipment_type = request.POST.get('equipment_type')
        installation_date = request.POST.get('installation_date')
        description = request.POST.get('description', '')
        
        # Vérifier si la référence existe déjà
        if Equipment.objects.filter(reference=reference).exists():
            messages.error(request, f'Un équipement avec la référence "{reference}" existe déjà.')
            return render(request, 'assets/equipment_add.html', {
                'name': name,
                'reference': reference,
                'equipment_type': equipment_type,
                'installation_date': installation_date,
                'description': description,
            })
        
        if name and reference and equipment_type and installation_date:
            Equipment.objects.create(
                name=name,
                reference=reference,
                equipment_type=equipment_type,
                installation_date=installation_date,
                description=description
            )
            messages.success(request, f'Équipement {name} ajouté avec succès !')
            return redirect('assets:equipment_list')
        else:
            messages.error(request, 'Tous les champs obligatoires doivent être remplis.')
    
    return render(request, 'assets/equipment_add.html')

# Vue pour ajouter un log de maintenance
def maintenance_add(request, equipment_id):
    """Ajouter un log de maintenance pour un équipement"""
    equipment = get_object_or_404(Equipment, id=equipment_id)
    
    if request.method == 'POST':
        maintenance_type = request.POST.get('maintenance_type')
        description = request.POST.get('description')
        technician_name = request.POST.get('technician_name')
        intervention_date = request.POST.get('intervention_date')
        duration_hours = request.POST.get('duration_hours', 1.0)
        status = request.POST.get('status', 'PENDING')
        parts_used = request.POST.get('parts_used', '')
        notes = request.POST.get('notes', '')
        
        if description and technician_name and intervention_date:
            MaintenanceLog.objects.create(
                equipment=equipment,
                maintenance_type=maintenance_type,
                description=description,
                technician_name=technician_name,
                intervention_date=intervention_date,
                duration_hours=duration_hours,
                status=status,
                parts_used=parts_used,
                notes=notes
            )
            messages.success(request, 'Log de maintenance ajouté avec succès !')
            return redirect('assets:equipment_detail', equipment_id=equipment.id)
        else:
            messages.error(request, 'Les champs obligatoires doivent être remplis.')
    
    context = {
        'equipment': equipment,
        'maintenance_types': MaintenanceLog.MAINTENANCE_TYPES,
        'status_choices': MaintenanceLog.STATUS_CHOICES,
    }
    return render(request, 'assets/maintenance_add.html', context)

# Vue de test
def test_view(request):
    """Vue de test pour vérifier que les templates fonctionnent"""
    return render(request, 'assets/test.html')


def maintenance_list(request):
    """Liste de toutes les maintenances avec filtres"""
    maintenance_logs = MaintenanceLog.objects.all().order_by('-intervention_date')
    equipments = Equipment.objects.filter(is_active=True)
    
    # Compter par statut
    completed_count = maintenance_logs.filter(status='COMPLETED').count()
    in_progress_count = maintenance_logs.filter(status='IN_PROGRESS').count()
    failed_count = maintenance_logs.filter(status='FAILED').count()
    
    context = {
        'maintenance_logs': maintenance_logs,
        'equipments': equipments,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'failed_count': failed_count,
    }
    return render(request, 'assets/maintenance_list.html', context)