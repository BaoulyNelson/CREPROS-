"""Configuration WSGI pour le déploiement en production (Gunicorn, Apache/mod_wsgi, etc.)."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
