from django.contrib.auth.models import User
from rest_framework import serializers


from photodb.apps.photodb.models import Photo, Tag, TagCategory

class PhotoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Photo
        fields = ('id', 'image', 'thumbnail', 'medium', 'year', 'month', 'day', 'tags', 'created_at', 'updated_at', 'owner')

class UserSerializer(serializers.ModelSerializer):
    photos = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'photos')

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'category')

class TagCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TagCategory
        fields = ('name')