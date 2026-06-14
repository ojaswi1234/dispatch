import os
import urllib.parse
from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEFAULT_DB_URL = 'postgresql://dispatch_user:password@localhost:5432/dispatch_db'
db_url = os.environ.get('DATABASE_URL', DEFAULT_DB_URL)

# Parse postgresql://user:pass@host:port/dbname manually
url = urllib.parse.urlparse(db_url)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': url.path[1:],
        'USER': url.username,
        'PASSWORD': url.password,
        'HOST': url.hostname,
        'PORT': url.port,
    }
}
