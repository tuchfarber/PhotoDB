from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views.generic import View
import json


from .permissions import IsOwnerOrReadOnly

from .models import Photo, Tag

from photodb.apps.api.serializers import PhotoSerializer

def home(request):
    return render(request, 'photodb/home.html', {})

def detail(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    return render(request, 'photodb/detail.html', {"photo_id": photo_id})

def upload(request):
    return render(request, 'photodb/upload.html', {})
