import uuid
from django.db import models
from config.managers import TenantManager, AllSallesManager


class Produit(models.Model):
    # Managers
    objects = TenantManager()
    all_salles = AllSallesManager()

    TYPE_CHOICES = [
        ('complement', 'Complément alimentaire'),
        ('pre_workout', 'Pre-Workout'),
        ('dose',        'Dose'),
        ('autre',       'Autre'),
    ]

    id = models.UUIDField(
        primary_key = True,
        default     = uuid.uuid4,
        editable    = False
    )

    nom           = models.CharField(max_length=100)
    type = models.CharField(
    max_length = 20,
    choices    = TYPE_CHOICES,
    default    = 'complement'
)
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2)
    stock         = models.PositiveIntegerField(default=0)
    seuil_alerte  = models.PositiveIntegerField(default=2)
    est_actif     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    salle = models.ForeignKey(
        'salles.Salle',
        on_delete=models.CASCADE,
        related_name='produits'
    )

    class Meta:
        verbose_name        = 'Produit'
        verbose_name_plural = 'Produits'
        ordering            = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.stock} en stock)"

    @property
    def stock_faible(self):
        return self.stock <= self.seuil_alerte