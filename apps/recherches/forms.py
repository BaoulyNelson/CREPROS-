"""Formulaires du tableau de bord pour les recherches théoriques et appliquées."""
from django import forms

from .models import CategorieRecherche, Recherche

_INPUT = "form-control"
_SELECT = "form-select"


class FormulaireRecherche(forms.ModelForm):
    class Meta:
        model = Recherche
        fields = [
            "titre", "auteur", "resume", "contenu", "image", "fichier_pdf",
            "categorie", "date_publication", "est_mise_en_avant",
        ]
        widgets = {
            "titre": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Titre de la recherche"}),
            "auteur": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Auteur(s)"}),
            "resume": forms.Textarea(attrs={"class": _INPUT, "rows": 4}),
            "image": forms.ClearableFileInput(attrs={"class": _INPUT}),
            "fichier_pdf": forms.ClearableFileInput(attrs={"class": _INPUT}),
            "categorie": forms.Select(attrs={"class": _SELECT}),
            "date_publication": forms.DateInput(attrs={"class": _INPUT, "type": "date"}),
            "est_mise_en_avant": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "titre": "Titre *",
            "auteur": "Auteur(s) *",
            "resume": "Résumé *",
            "contenu": "Contenu détaillé",
            "image": "Image de couverture",
            "fichier_pdf": "Fichier PDF *",
            "categorie": "Catégorie",
            "date_publication": "Date de publication *",
            "est_mise_en_avant": "Mettre en avant sur la page d'accueil",
        }


class FormulaireCategorieRecherche(forms.ModelForm):
    class Meta:
        model = CategorieRecherche
        fields = ["nom", "description"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Nom de la catégorie"}),
            "description": forms.Textarea(attrs={"class": _INPUT, "rows": 3}),
        }
        labels = {"nom": "Nom de la catégorie *", "description": "Description"}
