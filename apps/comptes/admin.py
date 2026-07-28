from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MembreEquipe, Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    """Personnalisation de l'administration des utilisateurs."""

    list_display = ('username', 'get_full_name', 'email', 'role', 'is_staff', 'is_active', 'date_creation')
    list_filter = ('role', 'is_staff', 'is_active', 'date_creation')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ("Informations complémentaires", {'fields': ('telephone', 'photo', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations complémentaires", {'fields': ('email', 'telephone', 'role')}),
    )

    @admin.display(description="Nom complet")
    def get_full_name(self, obj):
        return obj.get_full_name() or "—"


@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'fonction', 'ordre_affichage', 'est_actif', 'date_modification')
    list_filter = ('est_actif',)
    search_fields = ('nom_complet', 'fonction')
    list_editable = ('ordre_affichage', 'est_actif')
    ordering = ('ordre_affichage',)
