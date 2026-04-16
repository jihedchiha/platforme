from django.contrib import admin
from .models import Salle, SalleFournisseur

@admin.register(SalleFournisseur)
class SalleFournisseurAdmin(admin.ModelAdmin):
    list_display = ('salle', 'fournisseur', 'taux_commission', 'statut', 'date_debut')
    list_filter = ('statut', 'salle')


@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'pack_saas', 'actif', 'created_at')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom', 'slug')
    list_filter = ('pack_saas', 'actif')
