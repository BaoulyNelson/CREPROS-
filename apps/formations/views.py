"""Vues publiques de présentation et d'inscription aux formations."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from .forms import InscriptionFormationForm
from .models import Formation


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
