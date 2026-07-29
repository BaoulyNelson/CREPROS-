"""Vues publiques générales : accueil, à propos, pages d'erreur, tableau de bord."""

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from apps.comptes.models import MembreEquipe

from .forms import FormulairePartenaire
from .mixins import EditeurRequisMixin
from .models import (
    ObjectifSpecifique,
    ParametresSite,
    Partenaire,
    Statistique,
    ValeurOrganisation,
)


class AccueilView(TemplateView):
    """Page d'accueil : hero, présentation, mission/vision, statistiques,
    dernières actualités, prochains événements, derniers documents, appel à l'action."""

    template_name = "core/accueil.html"

    def get_context_data(self, **kwargs):
        from django.utils import timezone
        from apps.actualites.models import Article
        from apps.documents_app.models import Document
        from apps.recherches.models import Recherche

        contexte = super().get_context_data(**kwargs)
        contexte.update(
            {
                "parametres": ParametresSite.objects.first(),
                "objectifs_specifiques": ObjectifSpecifique.objects.all(),
                "statistiques": Statistique.objects.all(),
                "derniers_articles": Article.objects.filter(statut="publie").order_by(
                    "-publie_le"
                )[:3],
                "derniers_documents": Document.objects.order_by("-date_publication")[
                    :4
                ],
                "dernieres_recherches": Recherche.objects.order_by("-date_publication")[
                    :3
                ],
                "partenaires": Partenaire.objects.all(),
            }
        )
        return contexte


class AProposView(TemplateView):
    """Page 'À propos' : histoire, mission, vision, valeurs, équipe."""

    template_name = "core/a_propos.html"

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte.update(
            {
                "parametres": ParametresSite.objects.first(),
                "valeurs": ValeurOrganisation.objects.all(),
                "objectifs_specifiques": ObjectifSpecifique.objects.all(),
                "equipe": MembreEquipe.objects.filter(est_actif=True),
            }
        )
        return contexte


class PolitiqueConfidentialiteView(TemplateView):
    """Page de politique de confidentialité (footer)."""

    template_name = "core/politique_confidentialite.html"


def erreur_404(request, exception=None):
    """Page d'erreur 404 personnalisée."""
    return render(request, "core/404.html", status=404)


def erreur_500(request):
    """Page d'erreur 500 personnalisée."""
    return render(request, "core/500.html", status=500)


# ── Tableau de bord : Partenaires ─────────────────────────────────────────────


class VueDashboardPartenaires(EditeurRequisMixin, ListView):
    template_name = "dashboard/partenaires/liste.html"
    context_object_name = "partenaires"
    queryset = Partenaire.objects.all()


class VueDashboardCreerPartenaire(EditeurRequisMixin, CreateView):
    template_name = "dashboard/partenaires/formulaire.html"
    form_class = FormulairePartenaire
    success_url = reverse_lazy("core:dashboard_partenaires")

    def form_valid(self, form):
        messages.success(self.request, "Partenaire ajouté avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Nouveau partenaire"
        ctx["bouton_submit"] = "Ajouter le partenaire"
        return ctx


class VueDashboardModifierPartenaire(EditeurRequisMixin, UpdateView):
    template_name = "dashboard/partenaires/formulaire.html"
    form_class = FormulairePartenaire
    queryset = Partenaire.objects.all()
    success_url = reverse_lazy("core:dashboard_partenaires")

    def form_valid(self, form):
        messages.success(self.request, "Partenaire mis à jour avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.nom}"
        ctx["bouton_submit"] = "Enregistrer les modifications"
        return ctx


class VueDashboardSupprimerPartenaire(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/partenaires/confirmer_suppression.html"
    queryset = Partenaire.objects.all()
    success_url = reverse_lazy("core:dashboard_partenaires")

    def form_valid(self, form):
        messages.success(self.request, "Partenaire supprimé avec succès.")
        return super().form_valid(form)
