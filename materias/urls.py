from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MateriaViewSet

router = DefaultRouter()
router.register(r'', MateriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
