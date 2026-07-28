from django.contrib import admin

from .models import Album, Photo, Video


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_creation', 'nombre_photos')
    search_fields = ('titre', 'description')
    prepopulated_fields = {'slug': ('titre',)}
    inlines = [PhotoInline]

    @admin.display(description="Nombre de photos")
    def nombre_photos(self, obj):
        return obj.photos.count()


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_creation')
    search_fields = ('titre', 'description')
