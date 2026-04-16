from django.db import models
from config.thread_local import get_current_salle_id

class TenantManager(models.Manager):
    """
    Manager qui filtre automatiquement les QuerySets selon la salle active du Thread Local.
    C'est la barrière de sécurité principale.
    """
    def get_queryset(self):
        salle_id = get_current_salle_id()
        queryset = super().get_queryset()
        
        # Si on est dans le contexte d'une salle (Personnel ou Fournisseur sélectionnant une salle)
        if salle_id:
            return queryset.filter(salle_id=salle_id)
            
        # Sinon (SuperAdmin global ou script de maintenance), on voit tout
        return queryset

class AllSallesManager(models.Manager):
    """
    Manager qui permet d'accéder à l'ensemble des données de toutes les salles.
    À utiliser explicitement pour l'administration globale.
    """
    pass
