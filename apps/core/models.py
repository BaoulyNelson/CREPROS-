"""Modèles de contenu institutionnel général : présentation, valeurs, statistiques."""
from django.core.exceptions import ValidationError
from django.db import models


class ParametresSite(models.Model):
    """
    Modèle singleton contenant les informations institutionnelles modifiables
    depuis l'administration : histoire, mission, vision, objectifs.

    Un seul enregistrement est autorisé (contrainte appliquée dans clean()
    et dans l'administration).
    """

    nom_organisation = models.CharField("Nom de l'organisation", max_length=255)
    sigle = models.CharField("Sigle / Acronyme", max_length=30, blank=True)
    devise = models.CharField("Devise", max_length=255, default="Mieux savoir pour mieux agir.")
    logo = models.ImageField("Logo", upload_to='site/', blank=True, null=True)

    histoire = models.TextField("Histoire de l'organisation", blank=True)
    mission = models.TextField("Mission")
    vision = models.TextField("Vision")
    objectif_general = models.TextField("Objectif général", blank=True)

    image_hero = models.ImageField("Image de la section d'accueil (Hero)", upload_to='site/', blank=True, null=True)
    texte_hero = models.CharField("Texte d'accroche (Hero)", max_length=255, blank=True)
    texte_appel_action = models.CharField("Texte de l'appel à l'action", max_length=255, blank=True,
                                           default="Rejoignez-nous dans la promotion des droits de l'enfant en Haïti")

    date_creation = models.DateTimeField("Créé le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Paramètres du site"
        verbose_name_plural = "Paramètres du site"

    def __str__(self):
        return self.nom_organisation

    def clean(self):
        if not self.pk and ParametresSite.objects.exists():
            raise ValidationError("Un seul enregistrement de paramètres du site est autorisé. "
                                   "Veuillez modifier l'enregistrement existant.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ObjectifSpecifique(models.Model):
    """Objectif spécifique du club, affiché sur la page d'accueil / à propos."""

    titre = models.CharField("Titre", max_length=255)
    description = models.TextField("Description", blank=True)
    icone = models.CharField(
        "Classe icône (Bootstrap Icons)", max_length=60, default='bi-check-circle',
        help_text="Exemple : bi-search, bi-mortarboard, bi-people"
    )
    ordre_affichage = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Objectif spécifique"
        verbose_name_plural = "Objectifs spécifiques"
        ordering = ['ordre_affichage']

    def __str__(self):
        return self.titre


class ValeurOrganisation(models.Model):
    """Valeur institutionnelle (intégrité, rigueur scientifique, etc.)."""

    nom = models.CharField("Nom de la valeur", max_length=100)
    description = models.TextField("Description")
    icone = models.CharField("Classe icône (Bootstrap Icons)", max_length=60, default='bi-star')
    ordre_affichage = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Valeur de l'organisation"
        verbose_name_plural = "Valeurs de l'organisation"
        ordering = ['ordre_affichage']

    def __str__(self):
        return self.nom


class Statistique(models.Model):
    """Chiffre clé affiché dans la section statistiques de la page d'accueil."""

    libelle = models.CharField("Libellé", max_length=150, help_text="Exemple : Recherches publiées")
    valeur = models.PositiveIntegerField("Valeur", help_text="Exemple : 25")
    suffixe = models.CharField("Suffixe", max_length=10, blank=True, help_text="Exemple : +, %")
    icone = models.CharField("Classe icône (Bootstrap Icons)", max_length=60, default='bi-graph-up')
    ordre_affichage = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"
        ordering = ['ordre_affichage']

    def __str__(self):
        return f"{self.libelle} : {self.valeur}{self.suffixe}"


class Partenaire(models.Model):
    """Partenaire ou bailleur de fonds affiché sur le site (logo cliquable)."""

    nom = models.CharField("Nom du partenaire", max_length=150)
    logo = models.ImageField("Logo", upload_to='partenaires/')
    site_web = models.URLField("Site web", blank=True)
    ordre_affichage = models.PositiveIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['ordre_affichage']

    def __str__(self):
        return self.nom
