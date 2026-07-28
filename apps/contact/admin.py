from django.contrib import admin

from .models import MessageContact


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'sujet', 'est_lu', 'date_envoi')
    list_filter = ('est_lu', 'date_envoi')
    search_fields = ('nom_complet', 'email', 'sujet', 'message')
    list_editable = ('est_lu',)
    date_hierarchy = 'date_envoi'
    readonly_fields = ('nom_complet', 'email', 'telephone', 'sujet', 'message', 'date_envoi')
    actions = ['marquer_comme_lu', 'marquer_comme_non_lu']

    @admin.action(description="Marquer comme lu")
    def marquer_comme_lu(self, request, queryset):
        queryset.update(est_lu=True)

    @admin.action(description="Marquer comme non lu")
    def marquer_comme_non_lu(self, request, queryset):
        queryset.update(est_lu=False)

    def has_add_permission(self, request):
        return False
