"""Vues publiques de la galerie photos et vidéos."""
from django.views.generic import DetailView, ListView

from .models import Album, Video


class AlbumListView(ListView):
    """Liste des albums photo (galerie principale)."""
    model = Album
    template_name = 'galerie/liste.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_queryset(self):
        return Album.objects.prefetch_related('photos')

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['videos'] = Video.objects.all()[:6]
        return contexte


class AlbumDetailView(DetailView):
    """Détail d'un album avec toutes ses photos."""
    model = Album
    template_name = 'galerie/detail.html'
    context_object_name = 'album'
