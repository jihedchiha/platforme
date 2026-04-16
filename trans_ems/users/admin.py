from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Fournisseur

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'user', 'taux_commission_defaut', 'actif', 'created_at')
    search_fields = ('nom', 'user__username')
    list_filter = ('actif',)



@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
		('Profil', {'fields': ('cin', 'telephone', 'photo', 'role', 'shift', 'date_embauche', 'salle')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2', 'email', 'role'),
		}),
	)
	list_display = ('username', 'email', 'cin', 'role', 'is_staff', 'salle')
	search_fields = ('username', 'email', 'cin')
	list_filter = ('role', 'salle')
