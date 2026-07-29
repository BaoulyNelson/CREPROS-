# Site institutionnel — centre de Recherche et de Formation sur les Politiques Sociales et les Droits de l'Enfant en Haïti

> **Devise :** « Mieux savoir pour mieux agir. »

Site web institutionnel complet, développé avec **Django 4.2.16**, conçu pour la diffusion de la recherche,
des formations, des actualités, des documents et des événements liés aux politiques sociales et aux droits
de l'enfant en Haïti.

## Sommaire

1. [Stack technique](#stack-technique)
2. [Structure du projet](#structure-du-projet)
3. [Installation](#installation)
4. [Configuration de la base de données](#configuration-de-la-base-de-données)
5. [Données de démonstration](#données-de-démonstration)
6. [Fonctionnalités](#fonctionnalités)
7. [Sécurité](#sécurité)
8. [Déploiement en production](#déploiement-en-production)
9. [Extensions futures](#extensions-futures)

## Stack technique

| Composant            | Technologie                          |
|-----------------------|--------------------------------------|
| Langage               | Python 3.11+                         |
| Framework             | Django 4.2.16                        |
| Base de données       | PostgreSQL (production) / MySQL via PyMySQL (développement, XAMPP) |
| Front-end             | Bootstrap 5, HTML5, CSS3, JavaScript |
| Icônes                | Bootstrap Icons                      |
| Éditeur riche         | django-ckeditor                      |
| API                   | Django REST Framework (base extensible) |
| Fichiers statiques    | WhiteNoise                           |
| Formulaires           | django-crispy-forms + crispy-bootstrap5 |
| Tags                  | django-taggit                        |

## Structure du projet

```
centre_droits_enfant/
├── config/                    # Configuration Django (settings, urls, wsgi, asgi)
├── apps/
│   ├── comptes/                # Authentification, utilisateur personnalisé, tableau de bord, équipe
│   ├── core/                   # Accueil, à propos, paramètres du site, sitemaps
│   ├── recherches/              # Publications de recherche
│   ├── formations/              # Sessions de formation + inscriptions
│   ├── actualites/              # Blog : articles, catégories, tags, commentaires
│   ├── evenements/              # Événements + inscriptions
│   ├── documents_app/           # Bibliothèque documentaire (PDF)
│   ├── galerie/                 # Albums photo + vidéos
│   └── contact/                 # Formulaire de contact
├── templates/                  # Templates globaux (base, navbar, footer, pagination)
├── static/                     # CSS, JS, images
├── media/                      # Fichiers uploadés (images, PDF)
├── requirements.txt
├── .env.example
└── manage.py
```

## Installation

### 1. Cloner le projet et créer un environnement virtuel

```bash
python3 -m venv venv
venv\Scripts\activate
source venv/bin/activate   # Sous Windows : venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Modifier le fichier `.env` avec vos propres valeurs (clé secrète, base de données, emails, réseaux sociaux...).

### 4. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Créer un superutilisateur (facultatif si vous utilisez les données de démonstration)

```bash
python manage.py createsuperuser
```

### 6. Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

Le site est accessible sur `http://127.0.0.1:8000/` et l'administration sur `http://127.0.0.1:8000/admin/`.

## Configuration de la base de données

Le projet prend en charge deux moteurs, sélectionnables via la variable `DB_MOTEUR` dans `.env` :

### PostgreSQL (recommandé en production)

```env
DB_MOTEUR=postgresql
DATABASE_URL=postgres://utilisateur:motdepasse@localhost:5432/centre_droits_enfant
```

### MySQL avec XAMPP (développement local)

1. Démarrer les services **Apache** et **MySQL** depuis le panneau de contrôle XAMPP.
2. Créer une base de données `centre_droits_enfant` via phpMyAdmin (`http://localhost/phpmyadmin`).
3. Configurer `.env` :

```env
DB_MOTEUR=mysql
DB_NOM=centre_droits_enfant
DB_UTILISATEUR=root
DB_MOT_DE_PASSE=
DB_HOTE=127.0.0.1
DB_PORT=3306
```

Le projet utilise **PyMySQL** afin d'éviter les problèmes de compilation liés à `mysqlclient`.

## Données de démonstration

Une commande de gestion personnalisée permet de générer un jeu de données complet (paramètres du site,
recherches, formations, articles, événements, documents, un superutilisateur `admin`) :

```bash
python manage.py generer_donnees_demo
```

Identifiants générés : `admin` / `ChangezMoi123!` — **à changer immédiatement** après la première connexion.

## Fonctionnalités

- **Authentification complète** : inscription, connexion, déconnexion, gestion du profil.
- **Tableau de bord** moderne avec statistiques en temps réel (recherches, formations, articles,
  événements, documents, messages non lus).
- **Pages publiques** : Accueil, À propos, Recherches, Formations, Actualités (blog), Événements,
  Documents, Galerie, Contact.
- **Blog complet** : catégories, tags, recherche, pagination, commentaires modérés, partage social.
- **Bibliothèque documentaire** : téléchargement PDF, catégories, recherche, filtrage, compteur de téléchargements.
- **Inscriptions en ligne** aux formations et événements, avec contrainte d'unicité par email.
- **Formulaire de contact** enregistré en base de données et visible depuis l'administration, avec envoi
  d'un email de notification.
- **Administration Django personnalisée** : en-têtes, regroupement des modèles, filtres, recherche,
  actions personnalisées (publier/dépublier, mettre en avant, marquer comme lu...).
- **SEO** : sitemap.xml, robots.txt, balises meta, Open Graph, URLs lisibles basées sur des slugs.

## Sécurité

- Protection CSRF activée sur tous les formulaires (`{% csrf_token %}`).
- Validation systématique des formulaires côté serveur (Django Forms / ModelForms).
- Protection XSS : échappement automatique des templates Django.
- Protection contre les injections SQL : usage exclusif de l'ORM Django (aucune requête SQL brute).
- Gestion sécurisée des médias : chaque type de fichier est stocké dans un sous-dossier dédié sous `media/`.
- En production (`DEBUG=False`) : `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`,
  HSTS et `X_FRAME_OPTIONS=DENY` sont automatiquement activés.

## Déploiement en production

1. Définir `DEBUG=False` et renseigner `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` dans `.env`.
2. Utiliser PostgreSQL en production (`DB_MOTEUR=postgresql`).
3. Générer une nouvelle `SECRET_KEY` robuste.
4. Servir les fichiers statiques via **WhiteNoise** (déjà configuré) ou un CDN.
5. Lancer l'application avec **Gunicorn** derrière un reverse proxy (Nginx/Apache) :

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

6. Configurer un serveur SMTP réel pour `EMAIL_BACKEND` (actuellement en mode console pour le développement).

## Extensions futures

Le projet a été conçu pour être facilement extensible. Grâce à l'architecture en applications
indépendantes et à la base d'API REST déjà en place (`/api/`), il est possible d'ajouter sans
refonte majeure :

- Un **espace membre** complet avec espace personnel.
- Un système de **newsletter** (via une nouvelle app `newsletter`).
- La gestion des **dons en ligne** (intégration d'une passerelle de paiement).
- Une **application mobile** consommant l'API REST déjà exposée.

## Licence et propriété

Ce projet a été développé sur mesure pour le centre de recherche et de formation sur les politiques
sociales et les droits de l'enfant en Haïti. Tous droits réservés.
