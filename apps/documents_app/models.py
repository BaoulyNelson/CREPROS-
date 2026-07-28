"""Modèles de la bibliothèque documentaire (rapports, guides, textes de loi, etc.)."""
import os

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class CategorieDocument(models.Model):
    """Catégorie d'un document (rapport, texte de loi, guide pratique, etc.)."""

    nom = models.CharField("Nom", max_length=120, unique=True)
    slug = models.SlugField("Slug", max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name = "Catégorie de document"
        verbose_name_plural = "Catégories de documents"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)


class Document(models.Model):
    """Document PDF téléchargeable de la bibliothèque documentaire."""

    titre = models.CharField("Titre", max_length=255)
    slug = models.SlugField("Slug", max_length=280, unique=True, blank=True)
    description = models.TextField("Description", blank=True)
    categorie = models.ForeignKey(
        CategorieDocument, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='documents', verbose_name="Catégorie"
    )
    fichier = models.FileField("Fichier PDF", upload_to='documents/')
    taille_fichier = models.PositiveIntegerField("Taille du fichier (Ko)", default=0, editable=False)
    date_publication = models.DateField("Date de publication")
    nombre_telechargements = models.PositiveIntegerField("Nombre de téléchargements", default=0, editable=False)
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-date_publication']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)[:270]
        if self.fichier:
            try:
                self.taille_fichier = self.fichier.size // 1024
            except (FileNotFoundError, ValueError):
                pass
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('documents_app:detail', kwargs={'slug': self.slug})

    @property
    def nom_fichier(self):
        return os.path.basename(self.fichier.name)
