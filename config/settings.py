"""
Configuration Django du projet — Site institutionnel du centre de recherche
et de formation sur les politiques sociales et les droits de l'enfant en Haïti.

Toutes les valeurs sensibles sont chargées depuis les variables d'environnement
(fichier .env à la racine du projet) via django-environ.
"""

from pathlib import Path
import environ

# ---------------------------------------------------------------------------
# Chemins de base
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Sécurité
# ---------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY", default="django-insecure-changez-moi-en-production")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# ---------------------------------------------------------------------------
# Informations de l'organisation (utilisées dans les templates via context processor)
# ---------------------------------------------------------------------------
NOM_ORGANISATION = env(
    "NOM_ORGANISATION",
    default="centre de Recherche et de Formation sur les Politiques Sociales et les Droits de l'Enfant",
)
SIGLE_ORGANISATION = env("SIGLE_ORGANISATION", default="CREPROS")
DEVISE_ORGANISATION = env(
    "DEVISE_ORGANISATION", default="Mieux savoir pour mieux agir."
)

# ---------------------------------------------------------------------------
# Applications installées
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    "ckeditor",
    "ckeditor_uploader",
    "taggit",
    "django_filters",
]

LOCAL_APPS = [
    "apps.comptes",
    "apps.core",
    "apps.recherches",
    "apps.formations",
    "apps.actualites",
    "apps.documents_app",
    "apps.galerie",
    "apps.contact",
    "apps.comments",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.parametres_site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------
# Base de données
# ---------------------------------------------------------------------------
# Par défaut : PostgreSQL (recommandé en production).
# Pour un développement local avec XAMPP/MySQL, définir DB_MOTEUR=mysql dans .env
# (nécessite PyMySQL, déjà configuré ci-dessous).
import pymysql  # noqa: E402

pymysql.install_as_MySQLdb()

DB_MOTEUR = env("DB_MOTEUR", default="postgresql")  # 'postgresql' ou 'mysql'

if DB_MOTEUR == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env("DB_NOM", default="centre_droits_enfant"),
            "USER": env("DB_UTILISATEUR", default="root"),
            "PASSWORD": env("DB_MOT_DE_PASSE", default=""),
            "HOST": env("DB_HOTE", default="127.0.0.1"),
            "PORT": env("DB_PORT", default="3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
else:
    DATABASES = {
        "default": env.db(
            "DATABASE_URL",
            default="postgres://postgres:postgres@localhost:5432/centre_droits_enfant",
        )
    }

# ---------------------------------------------------------------------------
# Validation des mots de passe
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "comptes.Utilisateur"

# Permet de se connecter avec le nom d'utilisateur OU l'adresse email.
# ModelBackend reste en second recours (ex. pour l'admin, les commandes
# manage.py createsuperuser, etc.).
AUTHENTICATION_BACKENDS = [
    "apps.comptes.backends.EmailOuUsernameBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "comptes:connexion"
LOGIN_REDIRECT_URL = "comptes:tableau_de_bord"
LOGOUT_REDIRECT_URL = "core:accueil"

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "fr"
TIME_ZONE = "America/Port-au-Prince"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Fichiers statiques et médias
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Sécurité additionnelle (production)
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_BROWSER_XSS_FILTER = True

# ---------------------------------------------------------------------------
# Emails (formulaire de contact, notifications)
# ---------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)
CONTACT_EMAIL_DESTINATAIRE = env("CONTACT_EMAIL_DESTINATAIRE", default=EMAIL_HOST_USER)

# ---------------------------------------------------------------------------
# Réseaux sociaux / coordonnées (affichés dans le footer)
# ---------------------------------------------------------------------------
SITE_TELEPHONE = env("SITE_TELEPHONE", default="+509 00 00 0000")
SITE_EMAIL = env("SITE_EMAIL", default="contact@organisation.org")
SITE_ADRESSE = env("SITE_ADRESSE", default="Port-au-Prince, Haïti")
SITE_FACEBOOK = env("SITE_FACEBOOK", default="")
SITE_TWITTER = env("SITE_TWITTER", default="")
SITE_LINKEDIN = env("SITE_LINKEDIN", default="")
SITE_INSTAGRAM = env("SITE_INSTAGRAM", default="")
SITE_YOUTUBE = env("SITE_YOUTUBE", default="")
GOOGLE_MAPS_EMBED_URL = env("GOOGLE_MAPS_EMBED_URL", default="")

# ---------------------------------------------------------------------------
# CKEditor (éditeur riche pour actualités, recherches, formations)
# ---------------------------------------------------------------------------
CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    },
}

# ---------------------------------------------------------------------------
# django-crispy-forms
# ---------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ---------------------------------------------------------------------------
# Django REST Framework (API interne, extensible)
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly"
    ],
}

# ---------------------------------------------------------------------------
# Pagination générale des vues publiques
# ---------------------------------------------------------------------------
ELEMENTS_PAR_PAGE = 9
ARTICLES_PAR_PAGE = env("ARTICLES_PAR_PAGE", default=9, cast=int)
# ---------------------------------------------------------------------------
# Messages (Bootstrap 5 alert classes)
# ---------------------------------------------------------------------------
from django.contrib.messages import constants as messages_constants  # noqa: E402

MESSAGE_TAGS = {
    messages_constants.DEBUG: "secondary",
    messages_constants.INFO: "info",
    messages_constants.SUCCESS: "success",
    messages_constants.WARNING: "warning",
    messages_constants.ERROR: "danger",
}
