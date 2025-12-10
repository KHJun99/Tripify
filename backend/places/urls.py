from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'places', views.PlaceViewSet, basename='place')
router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')

app_name = 'places'

urlpatterns = [
    path('', include(router.urls)),
]
