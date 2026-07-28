from rest_framework import viewsets

from .models import Recherche
from .serializers import RechercheSerializer


class RechercheViewSet(viewsets.ReadOnlyModelViewSet):
    """API publique en lecture seule des recherches."""
    queryset = Recherche.objects.select_related('categorie').all()
    serializer_class = RechercheSerializer
