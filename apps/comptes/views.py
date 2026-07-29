"""Vues d'authentification et tableau de bord administratif."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import ConnexionForm, InscriptionForm, ProfilForm
from .models import Utilisateur
from apps.core.mixins import EditeurRequisMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)
from .forms import ConnexionForm, FormulaireMembreEquipe, InscriptionForm, ProfilForm
from .models import MembreEquipe, Utilisateur

class InscriptionView(CreateView):
    """Permet à un visiteur de créer un compte, puis le connecte automatiquement."""

    model = Utilisateur
    form_class = InscriptionForm
    template_name = "comptes/inscription.html"
    success_url = reverse_lazy("comptes:tableau_de_bord")

    def form_valid(self, form):
        reponse = super().form_valid(form)
        # self.object (le nouvel utilisateur) est défini par CreateView.form_valid().
        # On précise le backend car AUTHENTICATION_BACKENDS en contient plusieurs :
        # login() ne peut pas deviner lequel utiliser puisque l'utilisateur n'a
        # pas été authentifié via authenticate() (juste créé en base).
        login(self.request, self.object, backend="apps.comptes.backends.EmailOuUsernameBackend")
        messages.success(
            self.request,
            f"Bienvenue, {self.object.get_full_name() or self.object.username} ! "
            "Votre compte a été créé avec succès.",
        )
        return reponse


class ConnexionView(LoginView):
    """Connexion d'un utilisateur existant."""

    template_name = "comptes/connexion.html"
    authentication_form = ConnexionForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Bienvenue, {form.get_user().get_full_name() or form.get_user().username} !",
        )
        return super().form_valid(form)


class DeconnexionView(LogoutView):
    """Déconnexion de l'utilisateur."""

    next_page = reverse_lazy("core:accueil")


class TableauDeBordView(LoginRequiredMixin, TemplateView):
    """Tableau de bord administratif moderne présentant les statistiques du site."""

    template_name = "comptes/tableau_de_bord.html"
    login_url = reverse_lazy("comptes:connexion")

    def get_context_data(self, **kwargs):
        # Imports locaux pour éviter les dépendances circulaires entre applications.
        from apps.recherches.models import Recherche
        from apps.formations.models import Formation
        from apps.actualites.models import Article, Evenement
        from apps.documents_app.models import Document
        from apps.contact.models import MessageContact
        from django.utils import timezone

        maintenant = timezone.now()

        contexte = super().get_context_data(**kwargs)
        contexte.update(
            {
                "total_recherches": Recherche.objects.count(),
                "total_formations": Formation.objects.count(),
                "total_articles": Article.objects.filter(statut="publie").count(),
                "total_documents": Document.objects.count(),
                "total_evenements_a_venir": Evenement.objects.filter(
                    date_debut__gte=maintenant
                ).count(),
                "messages_non_lus": MessageContact.objects.filter(est_lu=False).count(),
                "derniers_messages": MessageContact.objects.order_by("-date_envoi")[:5],
                "derniers_articles": Article.objects.filter(statut="publie").order_by(
                    "-publie_le"
                )[:5],
                "prochains_evenements": Evenement.objects.filter(
                    date_debut__gte=maintenant
                ).order_by("date_debut")[:5],
            }
        )
        return contexte

class ProfilView(LoginRequiredMixin, UpdateView):
    """Mise à jour du profil de l'utilisateur connecté."""

    model = Utilisateur
    form_class = ProfilForm
    template_name = "comptes/profil.html"
    success_url = reverse_lazy("comptes:profil")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Votre profil a été mis à jour avec succès.")
        return super().form_valid(form)
    

# ── Tableau de bord : Membres de l'équipe ─────────────────────────────────────


class VueDashboardEquipe(EditeurRequisMixin, ListView):
    template_name = "dashboard/equipe/liste.html"
    context_object_name = "membres"
    queryset = MembreEquipe.objects.all()


class VueDashboardCreerMembreEquipe(EditeurRequisMixin, CreateView):
    template_name = "dashboard/equipe/formulaire.html"
    form_class = FormulaireMembreEquipe
    success_url = reverse_lazy("comptes:dashboard_equipe")

    def form_valid(self, form):
        messages.success(self.request, "Membre de l'équipe ajouté avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Nouveau membre de l'équipe"
        ctx["bouton_submit"] = "Ajouter le membre"
        return ctx


class VueDashboardModifierMembreEquipe(EditeurRequisMixin, UpdateView):
    template_name = "dashboard/equipe/formulaire.html"
    form_class = FormulaireMembreEquipe
    queryset = MembreEquipe.objects.all()
    success_url = reverse_lazy("comptes:dashboard_equipe")

    def form_valid(self, form):
        messages.success(self.request, "Membre de l'équipe mis à jour avec succès !")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.nom_complet}"
        ctx["bouton_submit"] = "Enregistrer les modifications"
        return ctx


class VueDashboardSupprimerMembreEquipe(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/equipe/confirmer_suppression.html"
    queryset = MembreEquipe.objects.all()
    success_url = reverse_lazy("comptes:dashboard_equipe")

    def form_valid(self, form):
        messages.success(self.request, "Membre de l'équipe supprimé avec succès.")
        return super().form_valid(form)
