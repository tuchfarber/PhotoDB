from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DEBUG = True
STATIC_ROOT = os.path.join(BASE_DIR, '/static')
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(' ')
CORS_ORIGIN_WHITELIST = (
    'localhost',
    'localhost:8080'
)
SESSION_COOKIE_DOMAIN = 'localhost'