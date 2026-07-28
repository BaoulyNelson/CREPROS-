"""Vues publiques de présentation des recherches."""
from django.http import FileResponse, Http404
from django.views.generic import DetailView, ListView

from .models import CategorieRecherche, Recherche


class RechercheListView(ListView):
    """Liste paginée des recherches, avec filtrage par catégorie et recherche textuelle."""

    model = Recherche
    template_name = 'recherches/liste.html'
    context_object_name = 'recherches'
    paginate_by = 9

    def get_queryset(self):
        queryset = Recherche.objects.select_related('categorie').all()
        terme = self.request.GET.get('q')
        categorie_slug = self.request.GET.get('categorie')
        if terme:
            from django.db.models import Q
            queryset = queryset.filter(Q(titre__icontains=terme) | Q(resume__icontains=terme) | Q(auteur__icontains=terme))
        if categorie_slug:
            queryset = queryset.filter(categorie__slug=categorie_slug)
        return queryset

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['categories'] = CategorieRecherche.objects.all()
        contexte['terme_recherche'] = self.request.GET.get('q', '')
        contexte['categorie_active'] = self.request.GET.get('categorie', '')
        return contexte


class RechercheDetailView(DetailView):
    """Détail d'une recherche."""

    model = Recherche
    template_name = 'recherches/detail.html'
    context_object_name = 'recherche'

    def get_queryset(self):
        return Recherche.objects.select_related('categorie')

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['recherches_similaires'] = Recherche.objects.filter(
            categorie=self.object.categorie
        ).exclude(pk=self.object.pk)[:3]
        return contexte


def telecharger_recherche(request, slug):
    """Incrémente le compteur de téléchargements et sert le fichier PDF."""
    try:
        recherche = Recherche.objects.get(slug=slug)
    except Recherche.DoesNotExist:
        raise Http404("Recherche introuvable.")
    recherche.nombre_telechargements = models_f_incr(recherche)
    return FileResponse(recherche.fichier_pdf.open('rb'), as_attachment=True,
                         filename=f"{recherche.slug}.pdf")


def models_f_incr(recherche):
    """Incrémente atomiquement le compteur de téléchargements."""
    from django.db.models import F
    Recherche.objects.filter(pk=recherche.pk).update(nombre_telechargements=F('nombre_telechargements') + 1)
    recherche.refresh_from_db(fields=['nombre_telechargements'])
    return recherche.nombre_telechargements
