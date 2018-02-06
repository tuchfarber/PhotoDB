from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.validators import ValidationError
import json

from photodb.apps.photodb.permissions import IsOwnerOrReadOnly
from photodb.apps.photodb.models import Photo, Tag, TagCategory, hash_image
from .serializers import PhotoSerializer, UserSerializer, TagSerializer, TagCategorySerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

    def perform_create(self, serializer):
        image = self.request.data.get('image')
        image_hash = hash_image(image)
        photo = Photo.objects.filter(image_hash=image_hash).first()
        # Fail if photo already exists in DB
        if photo:
            raise ValidationError('{} already uploaded'.format(str(image)))
        serializer.save(
            owner=self.request.user,
            image_hash=image_hash
        )

    def get_queryset(self):
        keyword = self.request.query_params.get('q', None)
        if not keyword:
            return Photo.objects.all()

        # Return any item that doesn't have a tags
        if keyword == 'untagged':
            return Photo.objects.filter(tags__isnull=True)
        
        queryset = Photo.objects.filter(
            Q(year__startswith=keyword) |
            Q(month__startswith=keyword) |
            Q(day__startswith=keyword) |
            Q(year__startswith=keyword) |
            Q(tags__name__startswith=keyword)
        ).distinct()

        return queryset

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagCategoryViewSet(viewsets.ModelViewSet):
    queryset = TagCategory.objects.all()
    serializer_class = TagCategorySerializer