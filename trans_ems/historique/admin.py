from django.contrib import admin
from .models import Historique


@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
	list_display = ('personnel', 'action', 'salle', 'created_at')
	list_filter = ('action', 'salle')
	search_fields = ('personnel__username', 'details')
