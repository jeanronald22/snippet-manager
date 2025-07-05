
import dj_database_url

from .base import *


DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:postgrest@localhost:5432/snippet_manager',
        conn_max_age=600
    )
}


MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = dj_database_url.config('STATIC_ROOT', default='/opt/render/project/src/staticfiles')
ROOT_URLCONF = 'snippet_manager.urls'
