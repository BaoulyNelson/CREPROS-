from django.contrib import admin

from .models import Formation, InscriptionFormation


class InscriptionFormationInline(admin.TabularInline):
    model = InscriptionFormation
    extra = 0
    readonly_fields = ('date_inscription',)


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'intervenant', 'date_debut', 'date_fin', 'statut', 'inscriptions_ouvertes', 'nombre_inscrits')
    list_filter = ('statut', 'inscriptions_ouvertes', 'date_debut')
    search_fields = ('titre', 'intervenant', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_debut'
    list_editable = ('inscriptions_ouvertes',)
    inlines = [InscriptionFormationInline]

    @admin.display(description="Inscrits")
    def nombre_inscrits(self, obj):
        return obj.inscriptions.count()


@admin.register(InscriptionFormation)
class InscriptionFormationAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'formation', 'date_inscription')
    list_filter = ('formation',)
    search_fields = ('nom_complet', 'email', 'organisation')
