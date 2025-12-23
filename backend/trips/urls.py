from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plans', views.TravelPlanViewSet, basename='travelplan')
router.register(r'wishlists', views.WishlistViewSet, basename='wishlist')

app_name = 'trips'

urlpatterns = [
    path('', include(router.urls)),
    path('recommended/', views.recommended_plans, name='recommended-plans'),
]
