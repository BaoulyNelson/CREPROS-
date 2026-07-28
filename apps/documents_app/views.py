"""Vues publiques de la bibliothèque documentaire."""
from django.db.models import F, Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import CategorieDocument, Document


class DocumentListView(ListView):
    """Liste paginée des documents, avec recherche et filtrage par catégorie."""

    model = Document
    template_name = 'documents_app/liste.html'
    context_object_name = 'documents'
    paginate_by = 12

    def get_queryset(self):
        queryset = Document.objects.select_related('categorie')
        terme = self.request.GET.get('q')
        categorie_slug = self.request.GET.get('categorie')
        if terme:
            queryset = queryset.filter(Q(titre__icontains=terme) | Q(description__icontains=terme))
        if categorie_slug:
            queryset = queryset.filter(categorie__slug=categorie_slug)
        return queryset

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['categories'] = CategorieDocument.objects.all()
        contexte['terme_recherche'] = self.request.GET.get('q', '')
        contexte['categorie_active'] = self.request.GET.get('categorie', '')
        return contexte


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'documents_app/detail.html'
    context_object_name = 'document'


def telecharger_document(request, slug):
    """Incrémente le compteur de téléchargements et sert le fichier."""
    document = get_object_or_404(Document, slug=slug)
    Document.objects.filter(pk=document.pk).update(nombre_telechargements=F('nombre_telechargements') + 1)
    return FileResponse(document.fichier.open('rb'), as_attachment=True, filename=document.nom_fichier)
