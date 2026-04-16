from django.contrib import admin
from .models import Produit, Vente, LigneVente


class LigneVenteInline(admin.TabularInline):
	model = LigneVente
	extra = 0


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
	list_display = ('nom', 'type', 'prix_unitaire', 'stock', 'est_actif', 'salle')
	list_filter = ('type', 'est_actif', 'salle')
	search_fields = ('nom',)


@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
	list_display = ('id', 'personnel', 'prix_total', 'salle', 'created_at')
	list_filter = ('created_at', 'salle')
	search_fields = ('personnel__username',)
	inlines = [LigneVenteInline]
