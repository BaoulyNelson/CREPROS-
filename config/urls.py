"""Routes URL principales du projet."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from apps.core.sitemaps import SITEMAPS

admin.site.site_header = f"Administration — {settings.SIGLE_ORGANISATION}"
admin.site.site_title = settings.SIGLE_ORGANISATION
admin.site.index_title = "Panneau de gestion du contenu"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', include('apps.core.urls', namespace='core')),
    path('comptes/', include('apps.comptes.urls', namespace='comptes')),
    path('recherches/', include('apps.recherches.urls', namespace='recherches')),
    path('formations/', include('apps.formations.urls', namespace='formations')),
    path('actualites/', include('apps.actualites.urls', namespace='actualites')),
    path('documents/', include('apps.documents_app.urls', namespace='documents_app')),
    path('galerie/', include('apps.galerie.urls', namespace='galerie')),
    path('contact/', include('apps.contact.urls', namespace='contact')),
    path('commentaires/', include('apps.comments.urls', namespace='comments')),


    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'apps.core.views.erreur_404'
handler500 = 'apps.core.views.erreur_500'
