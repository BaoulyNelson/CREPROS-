"""
Commande de gestion Django : génère un jeu de données de démonstration complet
afin de pouvoir présenter le site immédiatement après installation.

Utilisation :
    python manage.py generer_donnees_demo
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = "Génère un jeu de données de démonstration pour l'ensemble du site."

    def handle(self, *args, **options):
        self.creer_parametres_site()
        self.creer_objectifs_et_valeurs()
        self.creer_statistiques()
        self.creer_utilisateur_demo()
        self.creer_recherches()
        self.creer_formations()
        self.creer_articles()
        self.creer_evenements()
        self.creer_documents()
        self.stdout.write(
            self.style.SUCCESS("Données de démonstration générées avec succès.")
        )

    def creer_parametres_site(self):
        from apps.core.models import ParametresSite

        if not ParametresSite.objects.exists():
            ParametresSite.objects.create(
                nom_organisation="centre de Recherche et de Formation sur les Politiques Sociales "
                "et les Droits de l'Enfant",
                sigle="CREPROS",
                devise="Mieux savoir pour mieux agir.",
                histoire="Fondé par un groupe de chercheurs et de praticiens engagés, le centre est né "
                "du constat que les politiques sociales en Haïti nécessitent une base "
                "documentaire solide pour mieux protéger les droits de l'enfant.",
                mission="Contribuer à la recherche sur les politiques sociales et la situation des "
                "droits de l'enfant en Haïti.",
                vision="La sensibilisation par la formation sur les politiques sociales et les "
                "droits de l'enfant.",
                objectif_general="Assurer la diffusion des documents de base sur les politiques "
                "sociales, la protection et les droits de l'enfant.",
                texte_hero="Un centre de recherche et de formation au service des droits de l'enfant en Haïti.",
            )
            self.stdout.write("Paramètres du site créés.")

    def creer_objectifs_et_valeurs(self):
        from apps.core.models import ObjectifSpecifique, ValeurOrganisation

        objectifs = [
            (
                "Recherche théorique et appliquée",
                "Réaliser des recherches sur les politiques sociales "
                "et les droits de l'enfant en Haïti.",
                "bi-search",
            ),
            (
                "Formation continue",
                "Organiser des sessions de formation sur les politiques sociales, "
                "la protection et les droits de l'enfant.",
                "bi-mortarboard",
            ),
            (
                "Diffusion documentaire",
                "Assurer la diffusion des documents de base sur les politiques "
                "sociales et la protection de l'enfant.",
                "bi-journal-richtext",
            ),
        ]
        for ordre, (titre, description, icone) in enumerate(objectifs):
            ObjectifSpecifique.objects.get_or_create(
                titre=titre,
                defaults={
                    "description": description,
                    "icone": icone,
                    "ordre_affichage": ordre,
                },
            )

        valeurs = [
            (
                "Rigueur scientifique",
                "Une approche méthodique et fondée sur des données probantes.",
                "bi-award",
            ),
            (
                "Intégrité",
                "Une conduite éthique et transparente dans toutes nos actions.",
                "bi-shield-check",
            ),
            (
                "Engagement social",
                "Un attachement profond à la protection des enfants haïtiens.",
                "bi-heart",
            ),
        ]
        for ordre, (nom, description, icone) in enumerate(valeurs):
            ValeurOrganisation.objects.get_or_create(
                nom=nom,
                defaults={
                    "description": description,
                    "icone": icone,
                    "ordre_affichage": ordre,
                },
            )
        self.stdout.write("Objectifs spécifiques et valeurs créés.")

    def creer_statistiques(self):
        from apps.core.models import Statistique

        statistiques = [
            ("Recherches publiées", 25, "+", "bi-journal-text"),
            ("Formations organisées", 40, "+", "bi-mortarboard"),
            ("Bénéficiaires formés", 1200, "+", "bi-people"),
            ("Documents disponibles", 60, "+", "bi-file-earmark-pdf"),
        ]
        for ordre, (libelle, valeur, suffixe, icone) in enumerate(statistiques):
            Statistique.objects.get_or_create(
                libelle=libelle,
                defaults={
                    "valeur": valeur,
                    "suffixe": suffixe,
                    "icone": icone,
                    "ordre_affichage": ordre,
                },
            )
        self.stdout.write("Statistiques créées.")

    def creer_utilisateur_demo(self):
        from apps.comptes.models import Utilisateur

        if not Utilisateur.objects.filter(username="admin").exists():
            Utilisateur.objects.create_superuser(
                username="admin",
                email="admin@organisation.org",
                password="ChangezMoi123!",
                first_name="Administrateur",
                last_name="Principal",
                role=Utilisateur.Role.ADMINISTRATEUR,
            )
            self.stdout.write(
                self.style.WARNING(
                    "Superutilisateur créé : admin / ChangezMoi123! (à changer immédiatement en production)"
                )
            )

    def creer_recherches(self):
        from apps.recherches.models import CategorieRecherche, Recherche
        from django.core.files.base import ContentFile

        categorie, _ = CategorieRecherche.objects.get_or_create(
            nom="Politiques sociales",
            defaults={"description": "Études sur les politiques sociales en Haïti."},
        )
        if not Recherche.objects.exists():
            for i in range(1, 4):
                recherche = Recherche(
                    titre=f"Analyse des politiques sociales en Haïti — Volet {i}",
                    auteur="Dr. Jean Baptiste",
                    resume="Cette recherche examine l'impact des politiques sociales sur la protection "
                    "de l'enfance en Haïti.",
                    categorie=categorie,
                    date_publication=timezone.now().date() - timedelta(days=30 * i),
                )
                recherche.fichier_pdf.save(
                    f"recherche-demo-{i}.pdf",
                    ContentFile(b"%PDF-1.4 Document de demonstration"),
                    save=False,
                )
                recherche.save()
        self.stdout.write("Recherches de démonstration créées.")

    def creer_formations(self):
        from apps.formations.models import Formation

        if not Formation.objects.exists():
            for i in range(1, 4):
                Formation.objects.create(
                    titre=f"Formation sur la protection de l'enfant — Session {i}",
                    description="Formation destinée aux travailleurs sociaux et aux éducateurs sur "
                    "les droits fondamentaux de l'enfant.",
                    duree="3 jours",
                    date_debut=timezone.now().date() + timedelta(days=15 * i),
                    intervenant="Me. Claudette Pierre",
                    lieu="Port-au-Prince, Haïti",
                    places_disponibles=30,
                    inscriptions_ouvertes=True,
                )
        self.stdout.write("Formations de démonstration créées.")

    def creer_articles(self):
        from apps.actualites.models import Article, Categorie
        from apps.comptes.models import Utilisateur

        categorie, _ = Categorie.objects.get_or_create(nom="Droits de l'enfant")
        auteur = Utilisateur.objects.filter(is_superuser=True).first()
        if not Article.objects.exists() and auteur:
            for i in range(1, 4):
                Article.objects.create(
                    titre=f"Publication du rapport annuel {2023 + i}",
                    auteur=auteur,
                    categorie=categorie,
                    extrait="Le centre publie son rapport annuel sur la situation des droits de l'enfant en Haïti.",
                    contenu="Contenu détaillé de l'article de démonstration...",
                    statut="publie",
                    publie_le=timezone.now() - timedelta(days=10 * i),
                )
        self.stdout.write("Articles de démonstration créés.")

    def creer_evenements(self):
        from apps.actualites.models import Evenement

        if not Evenement.objects.exists():
            for i in range(1, 4):
                Evenement.objects.create(
                    titre=f"Conférence sur les droits de l'enfant — Édition {i}",
                    lieu="Hôtel Karibe, Port-au-Prince",
                    date_debut=timezone.now() + timedelta(days=20 * i),
                    date_fin=timezone.now() + timedelta(days=20 * i, hours=3),
                    description="Une conférence rassemblant chercheurs, praticiens et décideurs autour "
                    "de la protection de l'enfance en Haïti.",
                )
        self.stdout.write("Événements de démonstration créés.")

    def creer_documents(self):
        from apps.documents_app.models import CategorieDocument, Document
        from django.core.files.base import ContentFile

        categorie, _ = CategorieDocument.objects.get_or_create(nom="Rapports")
        if not Document.objects.exists():
            for i in range(1, 4):
                document = Document(
                    titre=f"Rapport de recherche — Document {i}",
                    description="Document de démonstration téléchargeable.",
                    categorie=categorie,
                    date_publication=timezone.now().date() - timedelta(days=5 * i),
                )
                document.fichier.save(
                    f"document-demo-{i}.pdf",
                    ContentFile(b"%PDF-1.4 Document de demonstration"),
                    save=False,
                )
                document.save()
        self.stdout.write("Documents de démonstration créés.")
