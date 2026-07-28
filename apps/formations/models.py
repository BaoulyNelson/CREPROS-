"""Modèles liés aux sessions de formation organisées par le club."""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Formation(models.Model):
    """Session de formation sur les politiques sociales et les droits de l'enfant."""

    class Statut(models.TextChoices):
        A_VENIR = 'a_venir', "À venir"
        EN_COURS = 'en_cours', "En cours"
        TERMINEE = 'terminee', "Terminée"

    titre = models.CharField("Titre", max_length=255)
    slug = models.SlugField("Slug", max_length=280, unique=True, blank=True)
    description = models.TextField("Description")
    duree = models.CharField("Durée", max_length=100, help_text="Exemple : 3 jours, 20 heures")
    date_debut = models.DateField("Date de début")
    date_fin = models.DateField("Date de fin", blank=True, null=True)
    intervenant = models.CharField("Intervenant(e)", max_length=255)
    lieu = models.CharField("Lieu", max_length=255, blank=True)
    image = models.ImageField("Image", upload_to='formations/images/', blank=True, null=True)
    places_disponibles = models.PositiveIntegerField("Places disponibles", default=0)
    inscriptions_ouvertes = models.BooleanField("Inscriptions ouvertes", default=False)
    statut = models.CharField("Statut", max_length=20, choices=Statut.choices, default=Statut.A_VENIR)
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['-date_debut']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)[:270]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('formations:detail', kwargs={'slug': self.slug})


class InscriptionFormation(models.Model):
    """Inscription d'un participant à une formation."""

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='inscriptions')
    nom_complet = models.CharField("Nom complet", max_length=200)
    email = models.EmailField("Email")
    telephone = models.CharField("Téléphone", max_length=20, blank=True)
    organisation = models.CharField("Organisation / Institution", max_length=200, blank=True)
    date_inscription = models.DateTimeField("Inscrit le", auto_now_add=True)

    class Meta:
        verbose_name = "Inscription à une formation"
        verbose_name_plural = "Inscriptions aux formations"
        ordering = ['-date_inscription']
        constraints = [
            models.UniqueConstraint(fields=['formation', 'email'], name='inscription_unique_par_formation')
        ]

    def __str__(self):
        return f"{self.nom_complet} — {self.formation.titre}"
