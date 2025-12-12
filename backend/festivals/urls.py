from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FestivalViewSet

router = DefaultRouter()
router.register(r'', FestivalViewSet, basename='festival')

urlpatterns = [
    path('', include(router.urls)),
]
