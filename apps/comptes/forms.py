"""Formulaires d'authentification et de gestion de profil."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import MembreEquipe, Utilisateur

from .models import Utilisateur


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription d'un nouvel utilisateur."""

    email = forms.EmailField(required=True, label="Adresse email")

    class Meta:
        model = Utilisateur
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone', 'password1', 'password2']
        labels = {
            'username': "Nom d'utilisateur",
            'first_name': "Prénom",
            'last_name': "Nom",
            'telephone': "Téléphone",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for champ in self.fields.values():
            champ.widget.attrs.setdefault('class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data['email']
        if Utilisateur.objects.filter(email__iexact=email).exists():
            raise ValidationError("Un compte existe déjà avec cette adresse email.")
        return email


class ConnexionForm(AuthenticationForm):
    """Formulaire de connexion stylisé Bootstrap 5, acceptant nom d'utilisateur ou email."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur ou email"
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Nom d'utilisateur ou email",
        })
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Mot de passe"})


class ProfilForm(forms.ModelForm):
    """Formulaire de mise à jour du profil utilisateur."""

    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'telephone', 'photo']
        labels = {
            'first_name': "Prénom",
            'last_name': "Nom",
            'email': "Email",
            'telephone': "Téléphone",
            'photo': "Photo de profil",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

class FormulaireMembreEquipe(forms.ModelForm):
    """Formulaire du tableau de bord pour créer / modifier un membre de l'équipe."""

    class Meta:
        model = MembreEquipe
        fields = [
            "nom_complet", "fonction", "biographie", "photo",
            "email", "linkedin", "ordre_affichage", "est_actif",
        ]
        widgets = {
            "nom_complet": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom complet"}),
            "fonction": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex : Coordonnateur, Chercheur"}),
            "biographie": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://linkedin.com/in/..."}),
            "ordre_affichage": forms.NumberInput(attrs={"class": "form-control"}),
            "est_actif": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "nom_complet": "Nom complet *",
            "fonction": "Fonction / Poste *",
            "biographie": "Biographie",
            "photo": "Photo *",
            "email": "Email",
            "linkedin": "LinkedIn",
            "ordre_affichage": "Ordre d'affichage",
            "est_actif": "Affiché sur le site",
        }
      
