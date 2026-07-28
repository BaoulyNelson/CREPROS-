"""Modèles de la galerie photos et vidéos."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Album(models.Model):
    """Album photo regroupant plusieurs images (ex. un événement)."""

    titre = models.CharField("Titre", max_length=255)
    slug = models.SlugField("Slug", max_length=280, unique=True, blank=True)
    description = models.TextField("Description", blank=True)
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Album photo"
        verbose_name_plural = "Albums photo"
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)[:270]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('galerie:detail', kwargs={'slug': self.slug})

    @property
    def image_couverture(self):
        premiere = self.photos.first()
        return premiere.image if premiere else None


class Photo(models.Model):
    """Photo appartenant à un album."""

    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField("Image", upload_to='galerie/photos/')
    legende = models.CharField("Légende", max_length=255, blank=True)
    ordre_affichage = models.PositiveIntegerField("Ordre d'affichage", default=0)
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        ordering = ['ordre_affichage', 'date_creation']

    def __str__(self):
        return self.legende or f"Photo #{self.pk} — {self.album.titre}"


class Video(models.Model):
    """Vidéo hébergée en externe (YouTube, Vimeo) intégrée dans la galerie."""

    titre = models.CharField("Titre", max_length=255)
    url_video = models.URLField("URL de la vidéo (YouTube / Vimeo)")
    description = models.TextField("Description", blank=True)
    image_apercu = models.ImageField("Image d'aperçu", upload_to='galerie/videos/', blank=True, null=True)
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre