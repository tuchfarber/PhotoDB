from django.core.files.base import ContentFile
from django.db import models
from hashlib import sha1
from io import BytesIO, StringIO
from PIL import Image
from sorl.thumbnail import get_thumbnail
import os.path
import uuid

    
    

def _renamer(id, filename, append=''):
    _, extension = os.path.splitext(filename)
    new_filename = "{}{}{}".format(str(id), append, extension)
    new_path = '/'.join(['photos', new_filename])
    return new_path

def rename_image(instance, filename):
    return _renamer(instance.id, instance.image.file.name, '')

def rename_thumbnail(instance, filename):
    return _renamer(instance.id, instance.image.file.name, '-thumb')

def rename_medium(instance, filename):
    return _renamer(instance.id, instance.image.file.name, '-med')

def hash_image(image):
    file = image.read()
    file_hash = sha1(file).hexdigest()
    return file_hash

class Tag(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return "<Tag {}>".format(self.name)

class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=rename_image)
    medium = models.ImageField(upload_to=rename_medium, null=True)
    thumbnail = models.ImageField(upload_to=rename_thumbnail, null=True)
    image_hash = models.CharField(max_length=40, unique=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return "<Photo {}>".format(self.id) 