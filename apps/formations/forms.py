from django import forms

from .models import InscriptionFormation


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
