from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.salle_views import SalleViewSet

router = DefaultRouter()
router.register(r'', SalleViewSet, basename='salle')

urlpatterns = [
    path('', include(router.urls)),
]
