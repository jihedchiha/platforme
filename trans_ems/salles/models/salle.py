import uuid
from django.db import models
from django.utils.text import slugify

class Salle(models.Model):
    PACK_SAAS_CHOICES = [
        ('starter', 'Starter'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='salles/logos/', null=True, blank=True)
    couleur_primaire = models.CharField(max_length=7, default='#0066FF')
    couleur_secondaire = models.CharField(max_length=7, default='#FF6600')
    pack_saas = models.CharField(max_length=20, choices=PACK_SAAS_CHOICES, default='starter')
    features_actives = models.JSONField(default=list)
    actif = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
