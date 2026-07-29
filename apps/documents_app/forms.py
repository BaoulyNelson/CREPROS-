"""Formulaires du tableau de bord pour la bibliothèque documentaire."""
from django import forms

from .models import CategorieDocument, Document

_INPUT = "form-control"
_SELECT = "form-select"


class FormulaireDocument(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["titre", "description", "categorie", "fichier", "date_publication"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Titre du document"}),
            "description": forms.Textarea(attrs={"class": _INPUT, "rows": 4}),
            "categorie": forms.Select(attrs={"class": _SELECT}),
            "fichier": forms.ClearableFileInput(attrs={"class": _INPUT}),
            "date_publication": forms.DateInput(attrs={"class": _INPUT, "type": "date"}),
        }
        labels = {
            "titre": "Titre *",
            "description": "Description",
            "categorie": "Catégorie",
            "fichier": "Fichier PDF *",
            "date_publication": "Date de publication *",
        }


class FormulaireCategorieDocument(forms.ModelForm):
    class Meta:
        model = CategorieDocument
        fields = ["nom"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Nom de la catégorie"}),
        }
        labels = {"nom": "Nom de la catégorie *"}
