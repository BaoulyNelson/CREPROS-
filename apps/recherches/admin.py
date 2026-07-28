from django.contrib import admin

from .models import CategorieRecherche, Recherche


@admin.register(CategorieRecherche)
class CategorieRechercheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom',)


@admin.register(Recherche)
class RechercheAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'date_publication', 'nombre_telechargements', 'est_mise_en_avant')
    list_filter = ('categorie', 'est_mise_en_avant', 'date_publication')
    search_fields = ('titre', 'auteur', 'resume')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
    list_editable = ('est_mise_en_avant',)
    readonly_fields = ('nombre_telechargements',)
    actions = ['marquer_mise_en_avant', 'retirer_mise_en_avant']

    @admin.action(description="Mettre en avant les recherches sélectionnées")
    def marquer_mise_en_avant(self, request, queryset):
        queryset.update(est_mise_en_avant=True)

    @admin.action(description="Retirer de la mise en avant")
    def retirer_mise_en_avant(self, request, queryset):
        queryset.update(est_mise_en_avant=False)
