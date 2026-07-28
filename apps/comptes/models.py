"""Modèles liés aux comptes utilisateurs et à l'équipe de l'organisation."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Utilisateur(AbstractUser):
    """
    Utilisateur personnalisé de la plateforme.

    Étend le modèle standard de Django afin de pouvoir ajouter des champs
    spécifiques (téléphone, photo de profil, rôle) sans avoir à migrer
    plus tard vers un modèle personnalisé.
    """

    class Role(models.TextChoices):
        ADMINISTRATEUR = 'administrateur', "Administrateur"
        REDACTEUR = 'redacteur', "Rédacteur"
        MEMBRE = 'membre', "Membre"

    telephone = models.CharField("Téléphone", max_length=20, blank=True)
    photo = models.ImageField("Photo de profil", upload_to='comptes/photos/', blank=True, null=True)
    role = models.CharField("Rôle", max_length=20, choices=Role.choices, default=Role.MEMBRE)
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_creation']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def est_administrateur(self):
        return self.role == self.Role.ADMINISTRATEUR or self.is_superuser

    @property
    def peut_ecrire(self):
        """Autorisé à publier des articles : administrateur, rédacteur, ou superuser."""
        return self.role in (self.Role.ADMINISTRATEUR, self.Role.REDACTEUR) or self.is_superuser


class MembreEquipe(models.Model):
    """Membre de l'équipe affiché sur la page 'À propos'."""

    nom_complet = models.CharField("Nom complet", max_length=150)
    fonction = models.CharField("Fonction / Poste", max_length=150)
    biographie = models.TextField("Biographie", blank=True)
    photo = models.ImageField("Photo", upload_to='equipe/')
    email = models.EmailField("Email", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)
    ordre_affichage = models.PositiveIntegerField("Ordre d'affichage", default=0)
    est_actif = models.BooleanField("Actif", default=True)
    date_creation = models.DateTimeField("Créé le", auto_now_add=True)
    date_modification = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['ordre_affichage', 'nom_complet']

    def __str__(self):
        return f"{self.nom_complet} — {self.fonction}"

    def get_absolute_url(self):
        return reverse('core:a_propos') + f'#membre-{self.pk}'