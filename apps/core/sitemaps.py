"""Sitemaps SEO du site (accueil, pages statiques, contenus dynamiques)."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PagesStatiquesSitemap(Sitemap):
    """Sitemap des pages statiques principales."""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "core:accueil",
            "core:a_propos",
            "recherches:liste",
            "formations:liste",
            "actualites:liste_articles",
            "actualites:liste_evenements",
            "documents_app:liste",
            "galerie:liste",
            "contact:contact",
        ]

    def location(self, item):
        return reverse(item)


class RecherchesSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        from apps.recherches.models import Recherche

        return Recherche.objects.all()

    def lastmod(self, obj):
        return obj.date_modification


class ArticlesSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        from apps.actualites.models import Article

        return Article.objects.filter(est_publie=True)

    def lastmod(self, obj):
        return obj.date_modification


SITEMAPS = {
    "statiques": PagesStatiquesSitemap,
    "recherches": RecherchesSitemap,
    "articles": ArticlesSitemap,
}
