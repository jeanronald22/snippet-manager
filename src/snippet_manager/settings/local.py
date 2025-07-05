import dj_database_url

from .base import *
from decouple import config


if config('DATABASE_URL', default=None):
    # Si DATABASE_URL est défini, l'utiliser (PostgreSQL local)
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }
else:
    # Sinon, utiliser SQLite par défaut
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'
ROOT_URLCONF = 'snippet_manager.urls'