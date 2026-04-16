from django.db import models
from uuid import uuid4

class SalleFournisseur(models.Model):
    STATUT_CHOICES = [
        ('actif',     'Actif'),
        ('inactif',   'Inactif'),
        ('transfere', 'Transféré'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    salle = models.ForeignKey('salles.Salle', on_delete=models.CASCADE, related_name='fournisseurs')
    fournisseur = models.ForeignKey('users.Fournisseur', on_delete=models.CASCADE, related_name='salles')
    taux_commission = models.DecimalField(max_digits=5, decimal_places=2)
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['salle', 'fournisseur', 'statut']]

    def __str__(self):
        return f"{self.salle} - {self.fournisseur}"
