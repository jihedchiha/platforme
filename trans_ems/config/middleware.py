from django.http import JsonResponse
from salles.models import SalleFournisseur
from config.thread_local import set_current_salle_id, clear_current_salle_id

class TenantMiddleware:
    """
    Middleware pour la gestion du Multi-Tenancy.
    Il identifie la salle (tenant) active pour chaque requête et l'attache à l'objet request.
    Il stocke également cette salle dans le Thread Local pour un filtrage automatique via les Managers.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # On ne traite que les utilisateurs authentifiés
        if not request.user.is_authenticated:
            return self.get_response(request)

        user = request.user
        salle_id = None  # Par défaut, pas de salle spécifique (ex: SuperAdmin global)

        # 1. Profil PERSONNEL : Salle fixe liée au profil
        if user.role == 'personnel':
            salle_id = user.salle_id

        # 2. Profil FOURNISSEUR : Doit fournir un X-Tenant-ID
        elif hasattr(user, 'fournisseur'):
            tenant_id = request.headers.get('X-Tenant-ID')

            if not tenant_id:
                return JsonResponse(
                    {'error': 'Contexte manquant. Veuillez sélectionner une salle (X-Tenant-ID manquant).'},
                    status=400
                )

            # Vérification que le fournisseur est bien autorisé pour cette salle
            est_autorise = SalleFournisseur.objects.filter(
                fournisseur=user.fournisseur,
                salle_id=tenant_id,
                statut='actif'
            ).exists()

            if not est_autorise:
                return JsonResponse(
                    {'error': 'Accès refusé. Vous n\'êtes pas autorisé à gérer cette salle.'},
                    status=403
                )

            salle_id = tenant_id

        # 3. Profil ADMIN (SuperAdmin) : Choix optionnel
        elif user.role == 'admin':
            tenant_id = request.headers.get('X-Tenant-ID')
            if tenant_id:
                salle_id = tenant_id

        # Montage du contexte pour la requête actuelle
        request.salle_id = salle_id
        set_current_salle_id(salle_id)

        try:
            response = self.get_response(request)
        finally:
            # Très important : vider le contexte à la fin de la requête
            clear_current_salle_id()
        
        return response
