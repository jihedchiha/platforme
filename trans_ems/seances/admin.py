from django.contrib import admin
from .models import Seance, Reservation


class ReservationInline(admin.TabularInline):
	model = Reservation
	extra = 0


@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
	list_display = ('date', 'heure_debut', 'heure_fin', 'places_disponibles', 'salle')
	list_filter = ('date', 'salle')
	search_fields = ('date',)
	inlines = [ReservationInline]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
	list_display = ('abonnement', 'seance', 'personnel', 'statut', 'created_at')
	list_filter = ('statut', 'seance', 'personnel')
	search_fields = ('abonnement__client__prenom', 'abonnement__client__nom')
