from ..models import Salle

class SalleService:
    """
    Logique métier pour la gestion des salles
    """
    
    @staticmethod
    def get_config(salle_id):
        try:
            salle = Salle.objects.get(id=salle_id)
            return {
                'nom': salle.nom,
                'couleur_primaire': salle.couleur_primaire,
                'couleur_secondaire': salle.couleur_secondaire,
                'logo': salle.logo.url if salle.logo else None
            }
        except Salle.DoesNotExist:
            raise ValueError("Salle non trouvée")
