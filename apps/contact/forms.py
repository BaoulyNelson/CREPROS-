from django import forms

from .models import MessageContact


class MessageContactForm(forms.ModelForm):
    """Formulaire public de contact."""

    class Meta:
        model = MessageContact
        fields = ['nom_complet', 'email', 'telephone', 'sujet', 'message']
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre adresse email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre numéro (optionnel)'}),
            'sujet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet de votre message'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Votre message'}),
        }
