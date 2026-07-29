"""Vues publiques de présentation et d'inscription aux formations, et tableau de bord."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from apps.core.mixins import EditeurRequisMixin, GestionnaireRequisMixin

from .forms import FormulaireFormation, InscriptionFormationForm
from .models import Formation, InscriptionFormation


class FormationListView(ListView):
    model = Formation
    template_name = 'formations/liste.html'
    context_object_name = 'formations'
    paginate_by = 9
    queryset = Formation.objects.all()


class FormationDetailView(DetailView):
    model = Formation
    template_name = 'formations/detail.html'
    context_object_name = 'formation'

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte['formulaire_inscription'] = InscriptionFormationForm()
        return contexte


class InscriptionFormationView(FormView):
    """Traite la soumission du formulaire d'inscription à une formation."""

    form_class = InscriptionFormationForm
    template_name = 'formations/detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.formation = get_object_or_404(Formation, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.formation.inscriptions_ouvertes:
            messages.error(self.request, "Les inscriptions pour cette formation ne sont pas ouvertes.")
            return redirect(self.formation.get_absolute_url())
        inscription = form.save(commit=False)
        inscription.formation = self.formation
        inscription.save()
        messages.success(self.request, "Votre inscription a bien été enregistrée. Merci !")
        return redirect(self.formation.get_absolute_url())

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs du formulaire d'inscription.")
        return redirect(self.formation.get_absolute_url())


# ── Tableau de bord : Formations ──────────────────────────────────────────────


class VueDashboardFormations(EditeurRequisMixin, ListView):
    template_name = "dashboard/formations/liste.html"
    context_object_name = "formations"
    queryset = Formation.objects.all()
    paginate_by = 15


class VueDashboardCreerFormation(EditeurRequisMixin, CreateView):
    template_name = "dashboard/formations/formulaire.html"
    form_class = FormulaireFormation
    success_url = reverse_lazy("formations:dashboard_formations")

    def form_valid(self, form):
        messages.success(self.request, "Formation créée avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création. Corrigez les erreurs ci-dessous.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = "Nouvelle formation"
        ctx["bouton_submit"] = "Créer la formation"
        return ctx


class VueDashboardModifierFormation(EditeurRequisMixin, UpdateView):
    template_name = "dashboard/formations/formulaire.html"
    form_class = FormulaireFormation
    queryset = Formation.objects.all()
    success_url = reverse_lazy("formations:dashboard_formations")

    def form_valid(self, form):
        messages.success(self.request, "Formation mise à jour avec succès !")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la modification.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titre_page"] = f"Modifier : {self.object.titre}"
        ctx["bouton_submit"] = "Enregistrer les modifications"
        return ctx


class VueDashboardSupprimerFormation(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/formations/confirmer_suppression.html"
    queryset = Formation.objects.all()
    success_url = reverse_lazy("formations:dashboard_formations")

    def form_valid(self, form):
        messages.success(self.request, "Formation supprimée avec succès.")
        return super().form_valid(form)


# ── Tableau de bord : Inscriptions aux formations ─────────────────────────────


class VueDashboardInscriptions(EditeurRequisMixin, ListView):
    template_name = "dashboard/inscriptions/liste.html"
    context_object_name = "inscriptions"
    paginate_by = 20

    def get_queryset(self):
        qs = InscriptionFormation.objects.select_related("formation").order_by("-date_inscription")
        formation_pk = self.request.GET.get("formation")
        if formation_pk:
            qs = qs.filter(formation_id=formation_pk)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["formations"] = Formation.objects.all()
        ctx["formation_active"] = self.request.GET.get("formation", "")
        return ctx


class VueDashboardSupprimerInscription(EditeurRequisMixin, DeleteView):
    template_name = "dashboard/inscriptions/confirmer_suppression.html"
    queryset = InscriptionFormation.objects.all()
    success_url = reverse_lazy("formations:dashboard_inscriptions")

    def form_valid(self, form):
        messages.success(self.request, "Inscription supprimée avec succès.")
        return super().form_valid(form)
