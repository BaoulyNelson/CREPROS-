"""Context processors globaux : rendent les paramètres du site disponibles partout."""
from django.conf import settings
from django.core.cache import cache

from .models import ParametresSite
from apps.actualites.models import Categorie, Article


def parametres_site(request):
    """
    Injecte les paramètres institutionnels, les coordonnées du site,
    les catégories de navigation et les breaking news dans le contexte
    de tous les templates (utilisé notamment par le header et le footer).
    """
    parametres = ParametresSite.objects.first()

    # ── Catégories pour le menu de navigation ───────────────────────────────
    categories = cache.get("nav_categories")
    if categories is None:
        categories = list(Categorie.objects.all()[:8])
        cache.set("nav_categories", categories, 300)

    # ── Breaking news ────────────────────────────────────────────────────────
    breaking = cache.get("breaking_news")
    if breaking is None:
        breaking = list(
            Article.objects.filter(
                statut="publie",
                est_breaking=True,
            ).order_by("-publie_le")[:5]
        )
        cache.set("breaking_news", breaking, 60)

    return {
        'parametres_site': parametres,
        'nom_organisation': parametres.nom_organisation if parametres else settings.NOM_ORGANISATION,
        'sigle': parametres.sigle if parametres else settings.SIGLE_ORGANISATION,
        'devise_organisation': parametres.devise if parametres else settings.DEVISE_ORGANISATION,
        'site_telephone': settings.SITE_TELEPHONE,
        'site_email': settings.SITE_EMAIL,
        'site_adresse': settings.SITE_ADRESSE,
        'site_facebook': settings.SITE_FACEBOOK,
        'site_twitter': settings.SITE_TWITTER,
        'site_linkedin': settings.SITE_LINKEDIN,
        'site_instagram': settings.SITE_INSTAGRAM,
        'site_youtube': settings.SITE_YOUTUBE,
        'google_maps_embed_url': settings.GOOGLE_MAPS_EMBED_URL,
        'nav_categories': categories,
        'breaking_news': breaking,
    }