"""Context processors globaux : rendent les paramètres du site disponibles partout."""
from django.conf import settings

from .models import ParametresSite


def parametres_site(request):
    """
    Injecte les paramètres institutionnels et les coordonnées du site
    dans le contexte de tous les templates (utilisé notamment par le footer
    et le header).
    """
    parametres = ParametresSite.objects.first()
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
    }
