"""Formulaires du tableau de bord pour la galerie photos et vidéos."""
from django import forms

from .models import Album, Photo, Video

_INPUT = "form-control"


class FormulaireAlbum(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["titre", "description"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Titre de l'album"}),
            "description": forms.Textarea(attrs={"class": _INPUT, "rows": 4}),
        }
        labels = {"titre": "Titre *", "description": "Description"}


class FormulairePhoto(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "legende", "ordre_affichage"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": _INPUT}),
            "legende": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Légende (optionnel)"}),
            "ordre_affichage": forms.NumberInput(attrs={"class": _INPUT}),
        }
        labels = {"image": "Image *", "legende": "Légende", "ordre_affichage": "Ordre d'affichage"}


class FormulaireVideo(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["titre", "url_video", "description", "image_apercu"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": _INPUT, "placeholder": "Titre de la vidéo"}),
            "url_video": forms.URLInput(attrs={"class": _INPUT, "placeholder": "https://www.youtube.com/watch?v=..."}),
            "description": forms.Textarea(attrs={"class": _INPUT, "rows": 3}),
            "image_apercu": forms.ClearableFileInput(attrs={"class": _INPUT}),
        }
        labels = {
            "titre": "Titre *",
            "url_video": "URL de la vidéo (YouTube / Vimeo) *",
            "description": "Description",
            "image_apercu": "Image d'aperçu",
        }
