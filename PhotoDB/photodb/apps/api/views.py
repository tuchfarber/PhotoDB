from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from io import BytesIO
from PIL import Image
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
import json

from photodb.apps.photodb.permissions import IsOwnerOrReadOnly
from photodb.apps.photodb.models import Photo, Tag, hash_image
from .serializers import PhotoSerializer, UserSerializer, TagSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

    def shrink_photo(self, image, image_hash, size):
        im = Image.open(image)
        im.thumbnail(size)
        thumb_io = BytesIO()
        content_type = image.content_type
        if content_type == 'image/jpeg':
            pil_type = 'jpeg'
        elif content_type == 'image/png':
            pil_type = 'png'

        im.save(thumb_io, format=pil_type)
        return SimpleUploadedFile(str(image_hash), thumb_io.getvalue(), content_type=content_type)

    def perform_create(self, serializer):
        image = self.request.data.get('image')
        image_hash = hash_image(image)
        photo = Photo.objects.filter(image_hash=image_hash).first()
        
        # Fail if photo already exists in DB
        if photo:
            raise ValidationError('{} already uploaded'.format(str(image)))

        thumb_file = self.shrink_photo(image, image_hash, (250, 250))
        med_file = self.shrink_photo(image, image_hash, (1024, 1024))

        serializer.save(
            owner=self.request.user,
            image_hash=image_hash,
            thumbnail=thumb_file,
            medium=med_file
        )

    def get_queryset(self):
        keyword = self.request.query_params.get('q', None)
        if not keyword:
            return Photo.objects.all()

        # Return any item that doesn't have a tags
        if keyword == 'untagged':
            return Photo.objects.filter(tags__isnull=True)
        
        queryset = Photo.objects.filter(
            Q(tags__name__startswith=keyword)
        ).distinct()

        return queryset

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

class CurrentUserView(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username
        })