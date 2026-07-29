"""Mixins de permission partagés par tous les tableaux de bord "maison".

Ces mixins reprennent la logique définie dans apps.actualites.views afin que
chaque module (documents, formations, galerie, recherches, partenaires,
équipe, etc.) applique les mêmes règles d'accès, sans dupliquer le code.

Rôles (apps.comptes.models.Utilisateur.role) :
    - "administrateur" ou superuser -> accès complet (gestion)
    - "redacteur"                   -> peut créer / modifier son propre contenu
    - "membre"                      -> aucun accès au tableau de bord
"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

ROLES_PEUVENT_ECRIRE = {"redacteur", "administrateur"}


def utilisateur_peut_ecrire(user):
    """Un rédacteur ou un administrateur peut créer/modifier des contenus."""
    return user.is_authenticated and (
        user.role in ROLES_PEUVENT_ECRIRE or user.est_administrateur
    )


def utilisateur_peut_gerer(user):
    """Seul un administrateur peut gérer (catégories, partenaires, équipe, etc.)."""
    return user.is_authenticated and user.est_administrateur


class EditeurRequisMixin(LoginRequiredMixin):
    """Accès réservé aux rédacteurs et administrateurs."""

    login_url = "/comptes/connexion/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Connectez-vous pour accéder à cette page.")
            return self.handle_no_permission()
        if not utilisateur_peut_ecrire(request.user):
            raise PermissionDenied("Accès refusé.")
        return super().dispatch(request, *args, **kwargs)


class GestionnaireRequisMixin(LoginRequiredMixin):
    """Accès réservé aux administrateurs."""

    login_url = "/comptes/connexion/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Connectez-vous pour accéder à cette page.")
            return self.handle_no_permission()
        if not utilisateur_peut_gerer(request.user):
            raise PermissionDenied("Accès refusé.")
        return super().dispatch(request, *args, **kwargs)
