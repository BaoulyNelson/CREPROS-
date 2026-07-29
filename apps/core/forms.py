"""Formulaires du tableau de bord pour le contenu institutionnel général."""
from django import forms

from .models import Partenaire

_INPUT = "form-control"


class FormulairePartenaire(forms.ModelForm):
    class Meta:
        model = Partenaire
        fields = ["nom", "logo", "site_web", "ordre_affichage"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Nom du partenaire"}),
            "logo": forms.ClearableFileInput(attrs={"class": _INPUT}),
            "site_web": forms.URLInput(attrs={"class": _INPUT, "placeholder": "https://..."}),
            "ordre_affichage": forms.NumberInput(attrs={"class": _INPUT}),
        }
        labels = {
            "nom": "Nom du partenaire *",
            "logo": "Logo *",
            "site_web": "Site web",
            "ordre_affichage": "Ordre d'affichage",
        }
