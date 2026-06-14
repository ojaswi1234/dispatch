import os
import urllib.parse
from .base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

db_url = os.environ.get('DATABASE_URL')
if db_url:
    url = urllib.parse.urlparse(db_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
            'CONN_MAX_AGE': 600,
        }
    }
else:
    DATABASES = {}

SECURE_SSL_REDIRECT = False
CORS_ALLOWED_ORIGINS = []
