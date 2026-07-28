"""Vues d'authentification et tableau de bord administratif."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import ConnexionForm, InscriptionForm, ProfilForm
from .models import Utilisateur


class InscriptionView(CreateView):
    """Permet à un visiteur de créer un compte."""

    model = Utilisateur
    form_class = InscriptionForm
    template_name = "comptes/inscription.html"
    success_url = reverse_lazy("comptes:connexion")

    def form_valid(self, form):
        reponse = super().form_valid(form)
        messages.success(
            self.request,
            "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.",
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
        from apps.actualites.models import Article
        from apps.documents_app.models import Document
        from apps.contact.models import MessageContact
        from django.utils import timezone

        contexte = super().get_context_data(**kwargs)
        contexte.update(
            {
                "total_recherches": Recherche.objects.count(),
                "total_formations": Formation.objects.count(),
                "total_articles": Article.objects.filter(statut="publie").count(),
                "total_documents": Document.objects.count(),
                "messages_non_lus": MessageContact.objects.filter(est_lu=False).count(),
                "derniers_messages": MessageContact.objects.order_by("-date_envoi")[:5],
                "derniers_articles": Article.objects.filter(statut="publie").order_by(
                    "-publie_le"
                )[:5],
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
