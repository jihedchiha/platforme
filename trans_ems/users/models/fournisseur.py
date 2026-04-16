from django.db import models
from uuid import uuid4

class Fournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField('users.Utilisateur', on_delete=models.CASCADE, related_name='fournisseur')
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, default='')
    taux_commission_defaut = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
