from .base import *

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'PhotoDB',
        'USER': os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_PASS'],
        'HOST': os.environ['MYSQL_HOST'],   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
DEBUG = False
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(' ')