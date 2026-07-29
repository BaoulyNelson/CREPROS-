"""
Commande de seed pour peupler la base avec des données de démonstration
pour l'app actualites : catégories, tags, articles.

Usage :
    python manage.py seed_actualites
    python manage.py seed_actualites --nombre 20
    python manage.py seed_actualites --vider
"""
import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from apps.actualites.models import Article, Categorie, Tag

User = get_user_model()


CATEGORIES = [
    {"nom": "Politiques sociales", "couleur": "#e74c3c"},
    {"nom": "Droits de l'enfant", "couleur": "#2ecc71"},
    {"nom": "Éducation", "couleur": "#3498db"},
    {"nom": "Santé publique", "couleur": "#f39c12"},
    {"nom": "Recherche", "couleur": "#9b59b6"},
    {"nom": "Formations", "couleur": "#1abc9c"},
]

TAGS = [
    "Haïti", "UEH", "FASCH", "protection sociale", "petite enfance",
    "vulnérabilité", "communauté", "genre", "gouvernance", "développement",
]

TITRES_ARTICLES = [
    "Lancement d'une nouvelle étude sur la protection de l'enfance en Haïti",
    "Colloque national sur les politiques sociales : les enseignements clés",
    "Renforcement des capacités des travailleurs sociaux dans le Grand Sud",
    "Les droits de l'enfant face aux défis de l'insécurité alimentaire",
    "Partenariat entre le CREPROS et les organisations communautaires locales",
    "Bilan de la campagne de sensibilisation sur la maltraitance infantile",
    "Publication d'un rapport sur l'accès à l'éducation en zones rurales",
    "Formation des acteurs institutionnels sur les droits fondamentaux",
    "Table ronde : quelles politiques publiques pour la petite enfance ?",
    "Résultats préliminaires de la recherche sur la vulnérabilité sociale",
    "Le CREPROS présente ses recommandations aux autorités locales",
    "Journée de réflexion sur la gouvernance et la protection sociale",
]

CONTENU_TEMPLATE = """
<p>Le Centre de Recherche sur la Protection Sociale et les Droits de l'Enfant
(CREPROS) poursuit ses activités de recherche et de sensibilisation autour
des enjeux liés à la protection de l'enfance en Haïti.</p>

<p>Cette initiative s'inscrit dans une démarche continue de renforcement des
capacités locales et de production de connaissances utiles à l'élaboration
de politiques publiques adaptées au contexte haïtien.</p>

<p>Les résultats de ces travaux seront partagés avec les partenaires
institutionnels et communautaires afin de favoriser une meilleure prise en
compte des droits de l'enfant dans les décisions publiques.</p>
"""


class Command(BaseCommand):
    help = "Peuple la base avec des catégories, tags et articles de démonstration."

    def add_arguments(self, parser):
        parser.add_argument(
            "--nombre", type=int, default=12,
            help="Nombre d'articles à créer (défaut : 12)"
        )
        parser.add_argument(
            "--vider", action="store_true",
            help="Supprime tous les articles/catégories/tags existants avant de seeder"
        )

    def handle(self, *args, **options):
        nombre = options["nombre"]
        vider = options["vider"]

        if vider:
            self.stdout.write(self.style.WARNING("Suppression des données existantes..."))
            Article.objects.all().delete()
            Categorie.objects.all().delete()
            Tag.objects.all().delete()

        auteur = self._obtenir_ou_creer_auteur()
        categories = self._creer_categories()
        tags = self._creer_tags()
        self._creer_articles(nombre, auteur, categories, tags)

        self.stdout.write(self.style.SUCCESS(
            f"Seed terminé : {Categorie.objects.count()} catégories, "
            f"{Tag.objects.count()} tags, {Article.objects.count()} articles."
        ))

    def _obtenir_ou_creer_auteur(self):
        auteur = User.objects.filter(is_superuser=True).first()
        if not auteur:
            auteur = User.objects.filter(is_staff=True).first()
        if not auteur:
            self.stdout.write(self.style.WARNING(
                "Aucun superuser trouvé, création d'un compte 'redaction' par défaut."
            ))
            auteur = User.objects.create_user(
                username="redaction",
                email="redaction@crepros.org",
                password="ChangeMoi123!",
                is_staff=True,
            )
        return auteur

    def _creer_categories(self):
        categories = []
        for data in CATEGORIES:
            categorie, cree = Categorie.objects.get_or_create(
                nom=data["nom"],
                defaults={
                    "slug": slugify(data["nom"]),
                    "couleur": data["couleur"],
                    "description": f"Articles liés à la thématique : {data['nom']}.",
                },
            )
            categories.append(categorie)
            if cree:
                self.stdout.write(f"  Catégorie créée : {categorie.nom}")
        return categories

    def _creer_tags(self):
        tags = []
        for nom in TAGS:
            tag, cree = Tag.objects.get_or_create(
                nom=nom, defaults={"slug": slugify(nom)}
            )
            tags.append(tag)
            if cree:
                self.stdout.write(f"  Tag créé : {tag.nom}")
        return tags

    def _creer_articles(self, nombre, auteur, categories, tags):
        statuts = ["publie", "publie", "publie", "en_revision", "brouillon"]

        for i in range(nombre):
            titre = TITRES_ARTICLES[i % len(TITRES_ARTICLES)]
            if i >= len(TITRES_ARTICLES):
                titre = f"{titre} ({i // len(TITRES_ARTICLES) + 1})"

            slug = slugify(titre)
            if Article.objects.filter(slug=slug).exists():
                continue

            statut = random.choice(statuts)
            publie_le = timezone.now() - timezone.timedelta(days=random.randint(0, 90)) \
                if statut == "publie" else None

            article = Article.objects.create(
                titre=titre,
                contenu=CONTENU_TEMPLATE,
                auteur=auteur,
                categorie=random.choice(categories),
                statut=statut,
                est_a_la_une=(i == 0),
                est_breaking=(random.random() < 0.15),
                nombre_vues=random.randint(0, 500),
                publie_le=publie_le,
            )
            article.tags.set(random.sample(tags, k=random.randint(1, 3)))

            self.stdout.write(f"  Article créé : {article.titre}")