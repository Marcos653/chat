from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.urls import path
from .views import *
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('auth/', CustomAuthToken.as_view()),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)