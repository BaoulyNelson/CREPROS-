"""Modèles liés aux recherches théoriques et appliquées publiées par le centre."""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class CategorieRecherche(models.Model):
    """Catégorie thématique d'une recherche (ex. protection de l'enfant, politiques sociales)."""

    nom = models.CharField("Nom", max_length=120, unique=True)
    slug = models.SlugField("Slug", max_length=140, unique=True, blank=True)
    description = models.TextField("Description", blank=True)

    class Meta:
        verbose_name = "Catégorie de recherche"
        verbose_name_plural = "Catégories de recherche"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Recherche(models.Model):
    """Publication de recherche théorique ou appliquée."""

    titre = models.CharField("Titre", max_length=255)
    slug = models.SlugField("Slug", max_length=280, unique=True, blank=True)
    auteur = models.CharField("Auteur(s)", max_length=255)
    resume = models.TextField("Résumé")
    contenu = RichTextUploadingField("Contenu détaillé", blank=True)
    image = models.ImageField(
        "Image de couverture", upload_to="recherches/images/", blank=True, null=True
    )
    fichier_pdf = models.FileField("Fichier PDF", upload_to="recherches/pdf/")
    categorie = models.ForeignKey(
        CategorieRecherche,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recherches",
        verbose_name="Catégorie",
    )
    date_publication = models.DateField("Date de publication")
    nombre_telechargements = models.PositiveIntegerField(
        "Nombre de téléchargements", default=0, editable=False
    )
    est_mise_en_avant = models.BooleanField(
        "Mise en avant sur la page d'accueil", default=False
    )
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Recherche"
        verbose_name_plural = "Recherches"
        ordering = ["-date_publication"]
        indexes = [models.Index(fields=["-date_publication"])]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)[:270]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recherches:detail", kwargs={"slug": self.slug})
