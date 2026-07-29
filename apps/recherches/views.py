"""Vues publiques de présentation des recherches, et tableau de bord."""
from django.contrib import messages
from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import EditeurRequisMixin, GestionnaireRequisMixin

from .forms import FormulaireCategorieRecherche, FormulaireRecherche
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


# ── Tableau de bord : Recherches ──────────────────────────────────────────────


class VueDashboardRecherches(EditeurRequisMixin, ListView):
    template_name = "dashboard/recherches/liste.html"
    context_object_name = "recherches"
    paginate_by = 15

    def get_queryset(self):
        from django.db.models import Q
        qs = Recherche.objects.select_related("categorie").order_by("-date_publication")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(titre__icontains=q) | Q(auteur__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class VueDashboardCreerRecherche(EditeurRequisMixin, CreateView):
    template_name = "dashboard/recherches/formulaire.html"
    form_class = FormulaireRecherche
    success_url = reverse_lazy("recherches:dashboard_recherches")

    def form_valid(self, form):
        messages.success(self.request, "Recherche publiée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création. Corrigez les erreurs ci-dessous.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Nouvelle recherche"
        ctx["bouton_submit"] = "Publier la recherche"
        return ctx


class VueDashboardModifierRecherche(EditeurRequisMixin, UpdateView):
    template_name = "dashboard/recherches/formulaire.html"
    form_class = FormulaireRecherche
    queryset = Recherche.objects.all()
    success_url = reverse_lazy("recherches:dashboard_recherches")

    def form_valid(self, form):
        messages.success(self.request, "Recherche mise à jour avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.titre}"
        ctx["bouton_submit"] = "Enregistrer les modifications"
        return ctx


class VueDashboardSupprimerRecherche(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/recherches/confirmer_suppression.html"
    queryset = Recherche.objects.all()
    success_url = reverse_lazy("recherches:dashboard_recherches")

    def form_valid(self, form):
        messages.success(self.request, "Recherche supprimée avec succès.")
        return super().form_valid(form)


class VueDashboardCategoriesRecherche(GestionnaireRequisMixin, ListView):
    template_name = "dashboard/categories_recherche/liste.html"
    context_object_name = "categories"
    queryset = CategorieRecherche.objects.all()


class VueDashboardCreerCategorieRecherche(GestionnaireRequisMixin, CreateView):
    template_name = "dashboard/categories_recherche/formulaire.html"
    form_class = FormulaireCategorieRecherche
    success_url = reverse_lazy("recherches:dashboard_categories_recherche")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie créée avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Nouvelle catégorie de recherche"
        return ctx


class VueDashboardModifierCategorieRecherche(GestionnaireRequisMixin, UpdateView):
    template_name = "dashboard/categories_recherche/formulaire.html"
    form_class = FormulaireCategorieRecherche
    queryset = CategorieRecherche.objects.all()
    success_url = reverse_lazy("recherches:dashboard_categories_recherche")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie mise à jour !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.nom}"
        return ctx


class VueDashboardSupprimerCategorieRecherche(GestionnaireRequisMixin, DeleteView):
    template_name = "dashboard/categories_recherche/confirmer_suppression.html"
    queryset = CategorieRecherche.objects.all()
    success_url = reverse_lazy("recherches:dashboard_categories_recherche")

    def form_valid(self, form):
        messages.success(self.request, "Catégorie supprimée.")
        return super().form_valid(form)
