from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views


urlpatterns = [
    path('login/', auth_views.login, {'template_name': 'photodb/login.html'}, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    
    path('<uuid:photo_id>', views.detail, name='detail'),
    path('upload', views.upload, name='upload'),
    path('', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)