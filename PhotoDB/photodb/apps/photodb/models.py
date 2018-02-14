from django.core.files.base import ContentFile
from django.db import models
from hashlib import sha1
from io import BytesIO, StringIO
from PIL import Image
from sorl.thumbnail import get_thumbnail
import os.path
import uuid

    
    

def _renamer(instance, filename, is_thumbnail):
    _, extension = os.path.splitext(filename)
    thumb_ident = '-thumb' if is_thumbnail else ''
    new_filename = "{}{}{}".format(str(instance.id), thumb_ident, extension)
    new_path = '/'.join(['photos', new_filename])
    return new_path

def rename_image(instance, filename):
    return _renamer(instance, filename, False)

def rename_thumbnail(instance, filename):
    return _renamer(instance, filename, True)

def hash_image(image):
    file = image.read()
    file_hash = sha1(file).hexdigest()
    return file_hash

class TagCategory(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __str__(self):
        return "<TagCategory {}>".format(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=128, primary_key=True)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "<Tag {}>".format(self.name)

class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=rename_image)
    thumbnail = models.ImageField(upload_to=rename_thumbnail, null=True)
    image_hash = models.CharField(max_length=40, unique=True)
    year = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    month = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    day = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return "<Photo {}>".format(self.id) 