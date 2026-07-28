"""Formulaires d'authentification et de gestion de profil."""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

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
    """Formulaire de connexion stylisé Bootstrap 5."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
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
