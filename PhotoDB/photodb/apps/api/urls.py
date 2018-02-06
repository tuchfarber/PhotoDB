from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import PhotoViewSet, UserViewSet, TagViewSet, TagCategoryViewSet

router = DefaultRouter()
router.register(r'photos', PhotoViewSet)
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'tagcategories', TagCategoryViewSet)

schema_view = get_schema_view(title='PhotoDB API')

urlpatterns = [
    path('', include(router.urls))
]