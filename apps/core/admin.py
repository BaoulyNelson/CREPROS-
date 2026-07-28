"""Administration des modèles de contenu institutionnel général."""
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ParametresSite,
    ObjectifSpecifique,
    ValeurOrganisation,
    Statistique,
    Partenaire,
)


@admin.register(ParametresSite)
class ParametresSiteAdmin(admin.ModelAdmin):
    """
    Administration du singleton ParametresSite.
    Empêche la création de plusieurs enregistrements et la suppression
    de l'unique enregistrement existant.
    """

    list_display = ('nom_organisation', 'sigle', 'devise', 'date_modification')
    readonly_fields = ('date_creation', 'date_modification', 'apercu_logo', 'apercu_hero')

    fieldsets = (
        ("Identité", {
            'fields': ('nom_organisation', 'sigle', 'devise', 'logo', 'apercu_logo')
        }),
        ("Présentation institutionnelle", {
            'fields': ('histoire', 'mission', 'vision', 'objectif_general')
        }),
        ("Section d'accueil (Hero)", {
            'fields': ('image_hero', 'apercu_hero', 'texte_hero', 'texte_appel_action')
        }),
        ("Métadonnées", {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',),
        }),
    )

    def apercu_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:80px;" />', obj.logo.url)
        return "—"
    apercu_logo.short_description = "Aperçu du logo"

    def apercu_hero(self, obj):
        if obj.image_hero:
            return format_html('<img src="{}" style="max-height:120px;" />', obj.image_hero.url)
        return "—"
    apercu_hero.short_description = "Aperçu de l'image Hero"

    def has_add_permission(self, request):
        # Un seul enregistrement autorisé
        return not ParametresSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # On évite de laisser le site sans paramètres
        return False


@admin.register(ObjectifSpecifique)
class ObjectifSpecifiqueAdmin(admin.ModelAdmin):
    list_display = ('titre', 'icone', 'ordre_affichage')
    list_editable = ('ordre_affichage',)
    search_fields = ('titre', 'description')
    ordering = ('ordre_affichage',)


@admin.register(ValeurOrganisation)
class ValeurOrganisationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'icone', 'ordre_affichage')
    list_editable = ('ordre_affichage',)
    search_fields = ('nom', 'description')
    ordering = ('ordre_affichage',)


@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'valeur', 'suffixe', 'icone', 'ordre_affichage')
    list_editable = ('valeur', 'suffixe', 'ordre_affichage')
    search_fields = ('libelle',)
    ordering = ('ordre_affichage',)


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site_web', 'apercu_logo', 'ordre_affichage')
    list_editable = ('ordre_affichage',)
    search_fields = ('nom',)
    ordering = ('ordre_affichage',)
    readonly_fields = ('apercu_logo',)

    def apercu_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:60px;" />', obj.logo.url)
        return "—"
    apercu_logo.short_description = "Aperçu du logo"