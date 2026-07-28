from django.contrib import admin

from .models import CategorieDocument, Document


@admin.register(CategorieDocument)
class CategorieDocumentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_publication', 'taille_fichier', 'nombre_telechargements')
    list_filter = ('categorie', 'date_publication')
    search_fields = ('titre', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
    readonly_fields = ('taille_fichier', 'nombre_telechargements')
