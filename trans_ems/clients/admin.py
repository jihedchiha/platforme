from django.contrib import admin
from .models import Client, Abonnement, Pack


class AbonnementInline(admin.TabularInline):
	model = Abonnement
	extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = ('prenom', 'nom', 'cin', 'telephone_1', 'email', 'salle', 'created_at')
	list_filter = ('statut', 'salle')
	search_fields = ('prenom', 'nom', 'cin', 'telephone_1', 'email')
	inlines = [AbonnementInline]


@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
	list_display = ('client', 'pack', 'statut', 'prix_paye', 'salle', 'created_at')
	list_filter = ('statut', 'salle', 'mode_paiement')
	search_fields = ('client__prenom', 'client__nom', 'pack__nom')


class PackAdmin(admin.ModelAdmin):
	list_display = ('nom', 'nb_seances', 'prix', 'est_actif', 'salle')
	list_filter = ('est_actif', 'salle')
	search_fields = ('nom',)


admin.site.register(Pack, PackAdmin)
