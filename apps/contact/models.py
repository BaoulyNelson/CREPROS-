"""Modèle des messages soumis via le formulaire de contact public."""
from django.db import models


class MessageContact(models.Model):
    """Message envoyé par un visiteur depuis le formulaire de contact."""

    nom_complet = models.CharField("Nom complet", max_length=200)
    email = models.EmailField("Email")
    telephone = models.CharField("Téléphone", max_length=20, blank=True)
    sujet = models.CharField("Sujet", max_length=255)
    message = models.TextField("Message")
    est_lu = models.BooleanField("Lu", default=False)
    date_envoi = models.DateTimeField("Envoyé le", auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.sujet} — {self.nom_complet}"
