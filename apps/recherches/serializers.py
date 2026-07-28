from rest_framework import serializers

from .models import Recherche


class RechercheSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)

    class Meta:
        model = Recherche
        fields = ['id', 'titre', 'slug', 'auteur', 'resume', 'image', 'fichier_pdf',
                  'categorie_nom', 'date_publication']
