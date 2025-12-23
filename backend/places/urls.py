from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'places', views.PlaceViewSet, basename='place')
router.register(r'bookmarks', views.BookmarkViewSet, basename='bookmark')

app_name = 'places'

urlpatterns = [
    # 커스텀 경로를 router보다 먼저 등록 (더 구체적인 경로가 우선)
    path('places/kakao/', views.create_place_from_kakao, name='create_place_from_kakao'),
    path('', include(router.urls)),
]
