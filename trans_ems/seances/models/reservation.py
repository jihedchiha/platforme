from django.db import models
from django.db.models import F
from django.db import transaction
import uuid
from .seance import Seance
from clients.models import Abonnement
from users.models import Utilisateur
from config.managers import TenantManager, AllSallesManager


class Reservation(models.Model):
    # Managers
    objects = TenantManager()
    all_salles = AllSallesManager()

    STATUT_CHOICES = [
        ('en_attente', 'En Attente'),
        ('present',    'Présent'),
        ('absent',     'Absent'),
        ('annule',     'Annulé'),
    ]

    TYPE_APPAREIL_CHOICES = [
        ('i-motion', 'i-Motion'),
        ('i-model',  'i-Model'),
    ]

    TAILLE_GILET_CHOICES = [
        
        
        ('M',  'M'),
        ('L',  'L'),
        ('XL',  'XL'),
        
    ]

    # ── Clé primaire ─────────────────────────
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # ── Relations ────────────────────────────
    abonnement = models.ForeignKey(
        Abonnement,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    seance = models.ForeignKey(
        Seance,
        on_delete=models.PROTECT,
        related_name='reservations'
    )

    personnel = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name='reservations_creees'
    )

    salle = models.ForeignKey(
        'salles.Salle',
        on_delete=models.CASCADE,
        related_name='reservations'
    )


    # ── Détails ───────────────────────────────
    type_appareil = models.CharField(
        max_length=10,
        choices=TYPE_APPAREIL_CHOICES
    )

    taille_gilet = models.CharField(
        max_length=3,
        choices=TAILLE_GILET_CHOICES,
        null=True,
        blank=True,
        default=None,
    )

    statut = models.CharField(
        max_length=15,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    # ── Rattrapage ────────────────────────────
    est_rattrapage = models.BooleanField(default=False)

    # ── Dates ────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Réservation'
        verbose_name_plural = 'Réservations'
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.abonnement.client} — {self.seance} ({self.statut})"

    