from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
import os
import uuid

from photodb.apps.photodb.models import Photo


class Command(BaseCommand):
    help = 'Imports photos from an directory. Use absolute path'

    def add_arguments(self, parser):
        parser.add_argument('--owner')
        parser.add_argument('import_dir', nargs='+', type=str)

    def handle(self, *args, **options):
        owner = User.objects.get(username=options['owner'])
        for path in options['import_dir']:
            for root, directories, filenames in os.walk(path):
                for filename in filenames:
                    absolute_path = os.path.join(root,filename)
                    photo = Photo(image=File(open(absolute_path, 'rb')), owner=owner)
                    photo.save()