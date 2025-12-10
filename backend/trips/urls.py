from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plans', views.TravelPlanViewSet, basename='travelplan')

app_name = 'trips'

urlpatterns = [
    path('', include(router.urls)),
]
