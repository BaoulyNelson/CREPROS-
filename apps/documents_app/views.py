"""Vues publiques et tableau de bord de la bibliothèque documentaire."""
from django.contrib import messages
from django.db.models import F, Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import EditeurRequisMixin, GestionnaireRequisMixin

from .forms import FormulaireCategorieDocument, FormulaireDocument
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


# ── Tableau de bord : Documents ───────────────────────────────────────────────


class VueDashboardDocuments(EditeurRequisMixin, ListView):
    template_name = "dashboard/documents/liste.html"
    context_object_name = "documents"
    paginate_by = 15

    def get_queryset(self):
        qs = Document.objects.select_related("categorie").order_by("-date_publication")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(titre__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class VueDashboardCreerDocument(EditeurRequisMixin, CreateView):
    template_name = "dashboard/documents/formulaire.html"
    form_class = FormulaireDocument
    success_url = reverse_lazy("documents_app:dashboard_documents")

    def form_valid(self, form):
        messages.success(self.request, "Document ajouté avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de l'ajout. Corrigez les erreurs ci-dessous.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Ajouter un document"
        ctx["bouton_submit"] = "Ajouter le document"
        return ctx


class VueDashboardModifierDocument(EditeurRequisMixin, UpdateView):
    template_name = "dashboard/documents/formulaire.html"
    form_class = FormulaireDocument
    queryset = Document.objects.all()
    success_url = reverse_lazy("documents_app:dashboard_documents")

    def form_valid(self, form):
        messages.success(self.request, "Document mis à jour avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.titre}"
        ctx["bouton_submit"] = "Enregistrer les modifications"
        return ctx


class VueDashboardSupprimerDocument(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/documents/confirmer_suppression.html"
    queryset = Document.objects.all()
    success_url = reverse_lazy("documents_app:dashboard_documents")

    def form_valid(self, form):
        messages.success(self.request, "Document supprimé avec succès.")
        return super().form_valid(form)


class VueDashboardCategoriesDocuments(GestionnaireRequisMixin, ListView):
    template_name = "dashboard/categories_documents/liste.html"
    context_object_name = "categories"
    queryset = CategorieDocument.objects.all()


class VueDashboardCreerCategorieDocument(GestionnaireRequisMixin, CreateView):
    template_name = "dashboard/categories_documents/formulaire.html"
    form_class = FormulaireCategorieDocument
    success_url = reverse_lazy("documents_app:dashboard_categories_documents")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie créée avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Nouvelle catégorie de document"
        return ctx


class VueDashboardModifierCategorieDocument(GestionnaireRequisMixin, UpdateView):
    template_name = "dashboard/categories_documents/formulaire.html"
    form_class = FormulaireCategorieDocument
    queryset = CategorieDocument.objects.all()
    success_url = reverse_lazy("documents_app:dashboard_categories_documents")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie mise à jour !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.nom}"
        return ctx


class VueDashboardSupprimerCategorieDocument(GestionnaireRequisMixin, DeleteView):
    template_name = "dashboard/categories_documents/confirmer_suppression.html"
    queryset = CategorieDocument.objects.all()
    success_url = reverse_lazy("documents_app:dashboard_categories_documents")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie supprimée.")
        return super().form_valid(form)
