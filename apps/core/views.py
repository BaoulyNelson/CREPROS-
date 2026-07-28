"""Vues publiques générales : accueil, à propos, pages d'erreur."""

from django.shortcuts import render
from django.views.generic import TemplateView

from apps.comptes.models import MembreEquipe

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
