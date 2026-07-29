from django import forms

from .models import Formation, InscriptionFormation

_INPUT = "form-control"
_SELECT = "form-select"


class InscriptionFormationForm(forms.ModelForm):
    """Formulaire d'inscription à une session de formation."""

    class Meta:
        model = InscriptionFormation
        fields = ['nom_complet', 'email', 'telephone', 'organisation']
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre adresse email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre numéro de téléphone'}),
            'organisation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre organisation (optionnel)'}),
        }


class FormulaireFormation(forms.ModelForm):
    """Formulaire du tableau de bord pour créer / modifier une formation."""

    class Meta:
        model = Formation
        fields = [
            "titre", "description", "duree", "date_debut", "date_fin",
            "intervenant", "lieu", "image", "places_disponibles",
            "inscriptions_ouvertes", "statut",
        ]
        widgets = {
            "titre": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Titre de la formation"}),
            "description": forms.Textarea(attrs={"class": _INPUT, "rows": 5}),
            "duree": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Ex : 3 jours, 20 heures"}),
            "date_debut": forms.DateInput(attrs={"class": _INPUT, "type": "date"}),
            "date_fin": forms.DateInput(attrs={"class": _INPUT, "type": "date"}),
            "intervenant": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Nom de l'intervenant(e)"}),
            "lieu": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Ex : Amphithéâtre A"}),
            "image": forms.ClearableFileInput(attrs={"class": _INPUT}),
            "places_disponibles": forms.NumberInput(attrs={"class": _INPUT}),
            "inscriptions_ouvertes": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "statut": forms.Select(attrs={"class": _SELECT}),
        }
        labels = {
            "titre": "Titre *",
            "description": "Description *",
            "duree": "Durée *",
            "date_debut": "Date de début *",
            "date_fin": "Date de fin",
            "intervenant": "Intervenant(e) *",
            "lieu": "Lieu",
            "image": "Image",
            "places_disponibles": "Places disponibles",
            "inscriptions_ouvertes": "Inscriptions ouvertes",
            "statut": "Statut",
        }

    def clean(self):
        donnees = super().clean()
        debut = donnees.get("date_debut")
        fin = donnees.get("date_fin")
        if debut and fin and fin < debut:
            self.add_error("date_fin", "La date de fin doit être postérieure ou égale à la date de début.")
        return donnees
