from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    auteur_nom = serializers.CharField(source='auteur.get_full_name', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'titre', 'slug', 'auteur_nom', 'categorie_nom', 'extrait',
                  'image_couverture', 'date_publication']
